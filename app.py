import streamlit as st

st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

pages = [
    st.Page(
        "dashboard.py",
        title="Dashboard",
        default=True
    )
]

user = st.session_state.get("user")

if user and user.get("role") == "OWNER":
    pages.append(
        st.Page(
            "owner_management.py",
            title="Owner Management"
        )
    )

navigation = st.navigation(pages, position="sidebar")
navigation.run()