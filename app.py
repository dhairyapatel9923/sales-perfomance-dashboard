import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# DASHBOARD PAGE
pages = [
    st.Page(
        "dashboard.py",
        title="Dashboard",
        default=True
    )
]

# OWNER MANAGEMENT PAGE
user = st.session_state.get("user")

if user and isinstance(user, dict) and str(user.get("role", "")).upper() == "OWNER":
    pages.append(
        st.Page(
            "owner_management.py",
            title="Owner Management"
        )
    )

# NAVIGATION
navigation = st.navigation(
    pages,
    position="sidebar"
)

navigation.run()