import streamlit as st
import pandas as pd
import psycopg2

from auth_helpers import (
    ROLE_OWNER,
    ROLE_ADMIN,
    ROLE_EMPLOYEE,
    get_db_connection,
    password_hash,
)

# Verify the signed-in user directly against Supabase.
user = st.session_state.get("user")

if not user:
    st.error("Please sign in first.")
    st.stop()

connection = get_db_connection()

try:
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT user_id, username
        FROM app_users
        WHERE user_id = %s
          AND role = 'OWNER'
          AND is_active = TRUE
        """,
        (user["user_id"],),
    )
    verified_owner = cursor.fetchone()
finally:
    connection.close()

if not verified_owner:
    st.error("Access denied. Only an active Owner can access this page.")
    st.stop()


# Owner Management interface
st.title("Owner Management")
st.caption("Create accounts and manage Admin and Employee access.")

create_tab, manage_tab = st.tabs(
    ["Create Account", "Manage Accounts"]
)

# CREATE ACCOUNT
with create_tab:
    with st.form("create_user_form", clear_on_submit=True):
        account_username = st.text_input(
            "New username",
            max_chars=80
        )
        account_password = st.text_input(
            "Temporary password (minimum 12 characters)",
            type="password"
        )
        account_role = st.selectbox(
            "Role",
            [ROLE_ADMIN, ROLE_EMPLOYEE]
        )

        create_account = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

    if create_account:
        if not account_username.strip() or len(account_password) < 12:
            st.error(
                "Enter a username and a password of at least 12 characters."
            )
        else:
            connection = get_db_connection()

            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO app_users
                        (username, password_hash, role, is_active)
                    VALUES (%s, %s, %s, TRUE)
                    """,
                    (
                        account_username.strip(),
                        password_hash(account_password),
                        account_role,
                    ),
                )
                connection.commit()
                st.success("Account created successfully.")

            except psycopg2.IntegrityError:
                connection.rollback()
                st.error("That username already exists.")

            except Exception as e:
                connection.rollback()
                st.error(f"Could not create account: {e}")

            finally:
                connection.close()


# MANAGE ACCOUNTS
with manage_tab:
    connection = get_db_connection()

    try:
        users_df = pd.read_sql_query(
            """
            SELECT user_id, username, role, is_active, created_at
            FROM app_users
            ORDER BY user_id
            """,
            connection,
        )
    finally:
        connection.close()

    st.dataframe(
        users_df,
        use_container_width=True,
        hide_index=True
    )

    manageable = users_df[
        users_df["role"] != ROLE_OWNER
    ]

    if manageable.empty:
        st.info("No Admin or Employee accounts are available.")
    else:
        chosen_user_id = st.selectbox(
            "Choose account",
            manageable["user_id"].astype(int).tolist(),
            key="manage_user_id",
        )

        chosen_user = manageable.loc[
            manageable["user_id"] == chosen_user_id
        ].iloc[0]

        col1, col2 = st.columns(2)

        new_role = col1.selectbox(
            "Change role",
            [ROLE_ADMIN, ROLE_EMPLOYEE],
            index=(
                0 if chosen_user["role"] == ROLE_ADMIN else 1
            ),
            key="manage_role",
        )

        desired_active = col2.selectbox(
            "Account status",
            ["Active", "Disabled"],
            index=(
                0 if bool(chosen_user["is_active"]) else 1
            ),
            key="manage_status",
        )

        if st.button(
            "Save Account Changes",
            use_container_width=True
        ):
            connection = get_db_connection()

            try:
                cursor = connection.cursor()

                # Recheck Owner permissions before changing accounts.
                cursor.execute(
                    """
                    SELECT 1
                    FROM app_users
                    WHERE user_id = %s
                      AND role = 'OWNER'
                      AND is_active = TRUE
                    """,
                    (user["user_id"],),
                )

                if not cursor.fetchone():
                    st.error("Access denied.")
                    st.stop()

                cursor.execute(
                    """
                    UPDATE app_users
                    SET role = %s, is_active = %s
                    WHERE user_id = %s
                      AND role <> 'OWNER'
                    """,
                    (
                        new_role,
                        desired_active == "Active",
                        int(chosen_user_id),
                    ),
                )

                connection.commit()
                st.success("Account updated successfully.")
                st.rerun()

            except Exception as e:
                connection.rollback()
                st.error(f"Could not update account: {e}")

            finally:
                connection.close()