import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, date
import hashlib
import hmac
import secrets as pysecrets

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PREMIUM CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
    --bg-1:#050816;
    --bg-2:#0B1120;
    --bg-3:#111827;
    --panel:rgba(15,23,42,.62);
    --panel-strong:rgba(17,24,39,.82);
    --border:rgba(148,163,184,.14);
    --text:#F8FAFC;
    --muted:#94A3B8;
    --blue:#3B82F6;
    --cyan:#22D3EE;
    --violet:#8B5CF6;
    --green:#34D399;
}

html, body, [class*="css"], .stApp{
    font-family:'Inter',sans-serif;
}

.stApp{
    min-height:100vh;
    background:
        radial-gradient(circle at 8% 0%, rgba(59,130,246,.18), transparent 30%),
        radial-gradient(circle at 92% 8%, rgba(139,92,246,.16), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(34,211,238,.08), transparent 32%),
        linear-gradient(135deg,var(--bg-1) 0%,var(--bg-2) 48%,var(--bg-3) 100%);
    background-attachment:fixed;
}

.stApp:before{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    background:linear-gradient(120deg,rgba(255,255,255,.018),transparent 35%,rgba(255,255,255,.012));
    z-index:0;
}

#MainMenu, footer, header{visibility:hidden;}

.block-container{
    position:relative;
    z-index:1;
    max-width:1600px;
    padding:2rem 2.5rem 3.5rem;
}

.main-title{
    font-size:clamp(30px,3vw,46px);
    line-height:1.08;
    font-weight:800;
    letter-spacing:-1.8px;
    color:var(--text);
    margin:0 0 6px;
    text-shadow:0 8px 30px rgba(0,0,0,.25);
}

.sub-title{
    color:var(--muted);
    font-size:15px;
    font-weight:500;
    letter-spacing:.15px;
}

.section-title{
    position:relative;
    display:flex;
    align-items:center;
    gap:10px;
    font-size:25px;
    line-height:1.2;
    font-weight:750;
    color:var(--text);
    letter-spacing:-.5px;
    margin:42px 0 20px;
    padding-bottom:14px;
    border-bottom:1px solid var(--border);
}

.section-title:after{
    content:"";
    position:absolute;
    left:0;
    bottom:-1px;
    width:68px;
    height:2px;
    border-radius:999px;
    background:linear-gradient(90deg,var(--blue),var(--violet),transparent);
}

hr{
    border:0!important;
    height:1px!important;
    margin:30px 0!important;
    background:linear-gradient(90deg,transparent,var(--border),transparent)!important;
}

/* Glass surfaces used by Streamlit status/alert components */
div[data-testid="stAlert"],
div[data-testid="stStatusWidget"],
.stAlert{
    background:var(--panel)!important;
    border:1px solid var(--border)!important;
    border-radius:18px!important;
    backdrop-filter:blur(18px);
    -webkit-backdrop-filter:blur(18px);
    box-shadow:0 16px 45px rgba(0,0,0,.18);
}

/* KPI cards */
div[data-testid="metric-container"]{
    position:relative;
    overflow:hidden;
    min-height:126px;
    padding:22px 22px 20px!important;
    border:1px solid rgba(148,163,184,.15)!important;
    border-radius:20px!important;
    background:
        linear-gradient(145deg,rgba(30,41,59,.76),rgba(15,23,42,.56))!important;
    box-shadow:
        0 18px 45px rgba(0,0,0,.22),
        inset 0 1px 0 rgba(255,255,255,.035)!important;
    backdrop-filter:blur(20px);
    -webkit-backdrop-filter:blur(20px);
    transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease;
}
div[data-testid="metric-container"]:before{
    content:"";
    position:absolute;
    top:0;
    left:0;
    right:0;
    height:3px;
    background:linear-gradient(90deg,var(--blue),var(--cyan),var(--violet));
}
div[data-testid="metric-container"]:after{
    content:"";
    position:absolute;
    width:74px;
    height:74px;
    right:-28px;
    top:-30px;
    border-radius:50%;
    background:radial-gradient(circle,rgba(59,130,246,.16),transparent 68%);
}
div[data-testid="metric-container"]:hover{
    transform:translateY(-5px);
    border-color:rgba(96,165,250,.32)!important;
    box-shadow:0 24px 55px rgba(0,0,0,.30),0 0 0 1px rgba(59,130,246,.05);
}
div[data-testid="metric-container"] label,
div[data-testid="stMetricLabel"]{
    color:#A8B4C7!important;
    font-size:12px!important;
    font-weight:650!important;
    text-transform:uppercase;
    letter-spacing:.75px;
}
div[data-testid="stMetricValue"]{
    color:#F8FAFC!important;
    font-size:29px!important;
    font-weight:800!important;
    letter-spacing:-1px;
    margin-top:5px;
}
div[data-testid="stMetricDelta"]{
    font-size:11px!important;
}

/* Header online/date controls */
div[data-testid="stVerticalBlock"] .stCaption{
    color:var(--muted);
}

/* Buttons */
.stButton>button, .stDownloadButton>button{
    width:100%;
    min-height:46px;
    border:1px solid rgba(96,165,250,.25)!important;
    border-radius:14px!important;
    background:linear-gradient(135deg,#2563EB,#4F46E5)!important;
    color:white!important;
    font-weight:700!important;
    letter-spacing:.1px;
    box-shadow:0 10px 28px rgba(37,99,235,.25);
    transition:transform .2s ease,box-shadow .2s ease,filter .2s ease;
}
.stButton>button:hover, .stDownloadButton>button:hover{
    transform:translateY(-2px);
    filter:brightness(1.08);
    box-shadow:0 16px 34px rgba(37,99,235,.34);
}
.stButton>button:active, .stDownloadButton>button:active{
    transform:translateY(0);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:
        linear-gradient(180deg,rgba(5,8,22,.97),rgba(11,17,32,.96))!important;
    border-right:1px solid rgba(148,163,184,.11);
}
section[data-testid="stSidebar"] > div{
    padding:1.6rem 1.15rem 2rem;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:#F8FAFC!important;
    letter-spacing:-.5px;
}
section[data-testid="stSidebar"] label{
    color:#CBD5E1!important;
    font-size:12px!important;
    font-weight:650!important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="input"] > div{
    background:rgba(30,41,59,.62)!important;
    border:1px solid rgba(148,163,184,.14)!important;
    border-radius:12px!important;
    min-height:44px;
    color:#F8FAFC!important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div:hover,
section[data-testid="stSidebar"] [data-baseweb="input"] > div:hover{
    border-color:rgba(96,165,250,.4)!important;
}
section[data-testid="stSidebar"] [data-testid="stDateInput"] > div{
    color:#F8FAFC!important;
}

/* Plotly/chart blocks */
div[data-testid="stPlotlyChart"]{
    overflow:hidden;
    padding:8px;
    border:1px solid rgba(148,163,184,.12);
    border-radius:22px;
    background:rgba(15,23,42,.48);
    box-shadow:0 18px 50px rgba(0,0,0,.20),inset 0 1px 0 rgba(255,255,255,.025);
    backdrop-filter:blur(16px);
    -webkit-backdrop-filter:blur(16px);
    transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease;
}
div[data-testid="stPlotlyChart"]:hover{
    transform:translateY(-3px);
    border-color:rgba(96,165,250,.22);
    box-shadow:0 25px 60px rgba(0,0,0,.27);
}

/* Dataframe */
div[data-testid="stDataFrame"]{
    overflow:hidden!important;
    border:1px solid rgba(148,163,184,.14)!important;
    border-radius:20px!important;
    background:rgba(15,23,42,.58)!important;
    box-shadow:0 18px 50px rgba(0,0,0,.22);
    backdrop-filter:blur(14px);
}
div[data-testid="stDataFrame"] iframe{
    border-radius:20px!important;
}

/* Inputs and generic Streamlit controls */
[data-baseweb="popover"]{
    background:#111827!important;
    border:1px solid var(--border)!important;
    border-radius:14px!important;
}
[data-baseweb="menu"]{
    background:#111827!important;
}
[data-baseweb="menu"] li{
    color:#E2E8F0!important;
}
[data-baseweb="menu"] li:hover{
    background:#1E293B!important;
}

/* Footer */
.dashboard-footer{
    margin-top:34px;
    padding:28px 24px;
    text-align:center;
    color:#94A3B8;
    font-size:13px;
    line-height:1.7;
    border:1px solid rgba(148,163,184,.13);
    border-radius:22px;
    background:rgba(15,23,42,.55);
    box-shadow:0 18px 50px rgba(0,0,0,.20);
    backdrop-filter:blur(18px);
}
.dashboard-footer b{
    color:#E2E8F0;
}

/* Scrollbar */
::-webkit-scrollbar{width:9px;height:9px;}
::-webkit-scrollbar-track{background:#080D19;}
::-webkit-scrollbar-thumb{
    background:linear-gradient(180deg,#334155,#1E293B);
    border-radius:999px;
    border:2px solid #080D19;
}
::-webkit-scrollbar-thumb:hover{background:#475569;}

/* Responsive */
@media (max-width:1100px){
    .block-container{padding-left:1.25rem;padding-right:1.25rem;}
    .main-title{font-size:34px;}
}
@media (max-width:760px){
    .block-container{padding:1.2rem .8rem 2.5rem;}
    .section-title{font-size:21px;margin-top:30px;}
    div[data-testid="metric-container"]{min-height:112px;padding:18px!important;}
    div[data-testid="stMetricValue"]{font-size:24px!important;}
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# AUTHENTICATION + DATABASE HELPERS
# =========================================================

ROLE_OWNER = "OWNER"
ROLE_ADMIN = "ADMIN"
ROLE_EMPLOYEE = "EMPLOYEE"
ALLOWED_ROLES = (ROLE_OWNER, ROLE_ADMIN, ROLE_EMPLOYEE)


def get_db_connection():
    """Open a fresh Supabase PostgreSQL connection using Streamlit secrets."""
    cfg = st.secrets["postgres"]
    return psycopg2.connect(
        host=cfg["host"],
        port=int(cfg.get("port", 5432)),
        user=cfg["user"],
        password=cfg["password"],
        dbname=cfg.get("database", "postgres"),
        connect_timeout=10,
        sslmode="require",
    )


def password_hash(password, salt=None):
    salt = salt or pysecrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), 310000)
    return f"pbkdf2_sha256$310000${salt}${digest.hex()}"


def password_matches(password, stored):
    try:
        algorithm, iterations, salt, expected = stored.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), int(iterations)).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def initialise_auth():
    """Create the app account table and bootstrap the first Owner from secrets."""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_users (
                user_id BIGSERIAL PRIMARY KEY,
                username VARCHAR(80) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('OWNER','ADMIN','EMPLOYEE')),
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        cursor.execute("SELECT COUNT(*) FROM app_users WHERE role = 'OWNER'")
        owner_exists = cursor.fetchone()[0] > 0
        if not owner_exists:
            auth_cfg = st.secrets.get("auth", {})
            bootstrap_username = str(auth_cfg.get("owner_username", "")).strip()
            bootstrap_password = str(auth_cfg.get("owner_password", ""))
            if not bootstrap_username or len(bootstrap_password) < 12:
                return (False, "No Owner account exists yet. Add [auth] owner_username and a strong owner_password (at least 12 characters) to .streamlit/secrets.toml, then restart the app. Do not share or commit this file.")
            cursor.execute(
                "INSERT INTO app_users (username, password_hash, role, is_active) VALUES (%s, %s, 'OWNER', TRUE)",
                (bootstrap_username, password_hash(bootstrap_password)),
            )
            connection.commit()
        return (True, "")
    finally:
        connection.close()


def authenticate(username, password):
    connection = get_db_connection()
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT user_id, username, password_hash, role, is_active FROM app_users WHERE username = %s",
            (username.strip(),),
        )
        user = cursor.fetchone()
        if user and user["is_active"] and password_matches(password, user["password_hash"]):
            return {"user_id": user["user_id"], "username": user["username"], "role": user["role"]}
        return None
    finally:
        connection.close()


def require_role(*roles):
    """UI guard; every write handler also checks the role before running SQL."""
    user = st.session_state.get("user")
    return bool(user and user.get("role") in roles)


try:
    auth_ready, auth_message = initialise_auth()
except Exception as auth_error:
    st.error("Authentication/database setup failed. Check the Supabase PostgreSQL secrets and database permissions.")
    st.caption(str(auth_error))
    st.stop()

if not auth_ready:
    st.warning(auth_message)
    st.stop()

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.markdown("<div class='main-title'>Sales Performance Dashboard</div><div class='sub-title'>Sign in to continue</div>", unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        username_input = st.text_input("Username", max_chars=80)
        password_input = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", use_container_width=True)
    if submitted:
        try:
            user = authenticate(username_input, password_input)
            if user:
                st.session_state.user = user
                st.rerun()
            st.error("Invalid username or password, or this account is disabled.")
        except Exception:
            st.error("Login failed because the database could not be reached. Check the database connection settings.")
    st.stop()

current_user = st.session_state.user
with st.sidebar:
    st.markdown("### Signed in")
    st.write(f"**{current_user['username']}**")
    st.caption(f"Role: {current_user['role']}")
    if st.button("Sign out", use_container_width=True):
        st.session_state.user = None
        st.rerun()

# =========================================================
# HEADER
# =========================================================

today = datetime.today().strftime("%d %b %Y")

left, right = st.columns([5,1])

with left:

    st.markdown(f"""
    <div class="main-title">
    📊 Sales Performance Dashboard
    </div>

    <div class="sub-title">
    Business Intelligence • Sales Analytics • Executive Overview
    </div>
    """, unsafe_allow_html=True)

with right:

    st.success("🟢 Online")
    st.caption(today)

st.divider()

# =========================================================
# REFRESH BUTTON
# =========================================================

refresh_col1, refresh_col2 = st.columns([1,5])

with refresh_col1:
    if st.button("🔄 Refresh"):
        st.rerun()

with refresh_col2:
    st.caption("Refresh dashboard after database updates.")

# =========================================================
# PART 1 ENDS HERE
# =========================================================
# =========================================================
# SUPABASE POSTGRESQL CONNECTION
# =========================================================

@st.cache_data(ttl=300)
def load_data():

    connection = get_db_connection()

    query = """
        SELECT
            sale_id,
            sale_date,
            product_name,
            category,
            region,
            salesperson,
            quantity,
            unit_price,
            cost_price,
            total_sales,
            total_profit
        FROM sales
        ORDER BY sale_date
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df


try:

    df = load_data()

except Exception as e:

    st.error(f"❌ Database Connection Failed\n\n{e}")

    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

if df.empty:

    st.warning("No sales data available.")

    st.stop()

df["sale_date"] = pd.to_datetime(df["sale_date"])

numeric_columns = [
    "quantity",
    "unit_price",
    "cost_price",
    "total_sales",
    "total_profit"
]

for col in numeric_columns:

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    ).fillna(0)


# =========================================================
# DATABASE STATUS
# =========================================================

left,right = st.columns([3,2])

with left:

    st.success(
        f"✅ Connected Successfully | "
        f"{len(df):,} Sales Records Loaded"
    )

with right:

    st.info(
        f"📅 Data Range\n"
        f"{df.sale_date.min().strftime('%d %b %Y')} → "
        f"{df.sale_date.max().strftime('%d %b %Y')}"
    )


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.title("🔎 Dashboard Filters")

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["category"].unique())
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["region"].unique())
)

salesperson = st.sidebar.selectbox(
    "Salesperson",
    ["All"] + sorted(df["salesperson"].unique())
)

date_range = st.sidebar.date_input(
    "Date Range",
    (
        df.sale_date.min().date(),
        df.sale_date.max().date()
    )
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if category != "All":

    filtered_df = filtered_df[
        filtered_df["category"] == category
    ]

if region != "All":

    filtered_df = filtered_df[
        filtered_df["region"] == region
    ]

if salesperson != "All":

    filtered_df = filtered_df[
        filtered_df["salesperson"] == salesperson
    ]

if len(date_range) == 2:

    start = pd.to_datetime(date_range[0])

    end = (
        pd.to_datetime(date_range[1])
        + pd.Timedelta(days=1)
    )

    filtered_df = filtered_df[
        (filtered_df["sale_date"] >= start)
        &
        (filtered_df["sale_date"] < end)
    ]


# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠ No records found for selected filters."
    )

    st.stop()


# =========================================================
# FILTER SUMMARY
# =========================================================

st.caption(

    f"Showing **{len(filtered_df):,}** records "
    f"from **{filtered_df.sale_date.min().strftime('%d %b %Y')}** "
    f"to **{filtered_df.sale_date.max().strftime('%d %b %Y')}**"

)

# =========================================================
# PART 2 ENDS HERE
# =========================================================
# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["total_sales"].sum()

total_profit = filtered_df["total_profit"].sum()

total_orders = filtered_df["sale_id"].nunique()

total_quantity = filtered_df["quantity"].sum()

average_order = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales > 0
    else 0
)

# =========================================================
# EXECUTIVE KPI DASHBOARD
# =========================================================

st.markdown(
    """
    <div class="section-title">
    📊 Executive Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:

    st.metric(
        label="💰 Total Sales",
        value=f"₹ {total_sales:,.0f}"
    )

with kpi2:

    st.metric(
        label="📈 Total Profit",
        value=f"₹ {total_profit:,.0f}"
    )

with kpi3:

    st.metric(
        label="🧾 Total Orders",
        value=f"{total_orders:,}"
    )

with kpi4:

    st.metric(
        label="📦 Quantity Sold",
        value=f"{total_quantity:,}"
    )

st.write("")

kpi5, kpi6 = st.columns(2)

with kpi5:

    st.metric(
        label="💵 Average Order Value",
        value=f"₹ {average_order:,.2f}"
    )

with kpi6:

    st.metric(
        label="📊 Profit Margin",
        value=f"{profit_margin:.2f}%"
    )

st.divider()

# =========================================================
# QUICK BUSINESS SUMMARY
# =========================================================

summary1, summary2, summary3 = st.columns(3)

with summary1:

    st.info(
        f"""
### 💰 Revenue

**₹ {total_sales:,.0f}**

Overall sales generated
"""
    )

with summary2:

    st.success(
        f"""
### 📈 Profit

**₹ {total_profit:,.0f}**

Overall business profit
"""
    )

with summary3:

    st.warning(
        f"""
### 📊 Margin

**{profit_margin:.2f}%**

Current profit margin
"""
    )

# =========================================================
# END OF PART 3
# =========================================================
# =========================================================
# SALES TRENDS
# =========================================================

st.markdown(
    """
    <div class="section-title">
    📈 Sales Trends
    </div>
    """,
    unsafe_allow_html=True
)

trend_col1, trend_col2 = st.columns(2)

# =========================================================
# MONTHLY SALES & PROFIT
# =========================================================

with trend_col1:

    monthly_df = (
        filtered_df
        .groupby(
            filtered_df["sale_date"].dt.to_period("M")
        )[["total_sales", "total_profit"]]
        .sum()
        .reset_index()
    )

    monthly_df["sale_date"] = (
        monthly_df["sale_date"]
        .astype(str)
    )

    fig_monthly = px.line(
        monthly_df,
        x="sale_date",
        y=["total_sales", "total_profit"],
        markers=True,
        template="plotly_dark",
        title="Monthly Sales & Profit"
    )

    fig_monthly.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(color="#E2E8F0", family="Inter", size=12),

        legend_title="",

        height=430,

        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(
            bgcolor="#111827",
            bordercolor="rgba(148,163,184,.25)",
            font=dict(color="#F8FAFC", family="Inter", size=12)
        ),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,.08)", zeroline=False)
    )

    fig_monthly.update_traces(
        line=dict(width=4),
        marker=dict(size=8)
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

# =========================================================
# DAILY SALES
# =========================================================

with trend_col2:

    daily_df = (
        filtered_df
        .groupby("sale_date")["total_sales"]
        .sum()
        .reset_index()
    )

    fig_daily = px.area(

        daily_df,

        x="sale_date",

        y="total_sales",

        template="plotly_dark",

        title="Daily Sales"

    )

    fig_daily.update_layout(

        paper_bgcolor="#0F172A",

        plot_bgcolor="#0F172A",

        font_color="white",

        height=430,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )

    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )

st.divider()

# =========================================================
# SALES OVERVIEW
# =========================================================

overview1, overview2, overview3 = st.columns(3)

with overview1:

    st.success(
        f"""
### 📈 Monthly Revenue

₹ {monthly_df['total_sales'].max():,.0f}
"""
    )

with overview2:

    st.info(
        f"""
### 💹 Monthly Profit

₹ {monthly_df['total_profit'].max():,.0f}
"""
    )

with overview3:

    st.warning(
        f"""
### 📅 Active Days

{filtered_df['sale_date'].nunique()}
"""
    )

# =========================================================
# END OF PART 4
# =========================================================
# =========================================================
# SALES ANALYSIS
# =========================================================

st.markdown(
    """
    <div class="section-title">
    📊 Sales Analysis
    </div>
    """,
    unsafe_allow_html=True
)

analysis_col1, analysis_col2 = st.columns(2)

# =========================================================
# SALES BY CATEGORY
# =========================================================

with analysis_col1:

    category_df = (
        filtered_df
        .groupby("category", as_index=False)["total_sales"]
        .sum()
        .sort_values("total_sales", ascending=False)
    )

    fig_category = px.pie(
        category_df,
        values="total_sales",
        names="category",
        hole=0.60,
        template="plotly_dark",
        title="Sales by Category"
    )

    fig_category.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig_category.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0", family="Inter", size=12),
        height=430,
        showlegend=False,
        hoverlabel=dict(bgcolor="#111827", bordercolor="rgba(148,163,184,.25)",
                         font=dict(color="#F8FAFC", family="Inter", size=12))
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

# =========================================================
# SALES BY REGION
# =========================================================

with analysis_col2:

    region_df = (
        filtered_df
        .groupby("region", as_index=False)["total_sales"]
        .sum()
        .sort_values("total_sales", ascending=False)
    )

    fig_region = px.bar(
        region_df,
        x="region",
        y="total_sales",
        color="total_sales",
        text_auto=".2s",
        template="plotly_dark",
        title="Sales by Region"
    )

    fig_region.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0", family="Inter", size=12),
        xaxis_title="Region",
        yaxis_title="Sales",
        height=430,
        coloraxis_showscale=False,
        hoverlabel=dict(bgcolor="#111827", bordercolor="rgba(148,163,184,.25)",
                         font=dict(color="#F8FAFC", family="Inter", size=12)),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,.08)", zeroline=False)
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

st.divider()

# =========================================================
# TOP 5 PRODUCTS
# =========================================================

st.markdown(
    """
    <div class="section-title">
    🏆 Top 5 Products by Sales
    </div>
    """,
    unsafe_allow_html=True
)

top_products = (
    filtered_df
    .groupby("product_name", as_index=False)["total_sales"]
    .sum()
    .sort_values("total_sales", ascending=False)
    .head(5)
)

fig_top_products = px.bar(
    top_products,
    x="total_sales",
    y="product_name",
    orientation="h",
    color="total_sales",
    text_auto=".2s",
    template="plotly_dark",
    title="Best Selling Products"
)

fig_top_products.update_layout(
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font_color="white",
    xaxis_title="Sales",
    yaxis_title="Product",
    height=450,
    coloraxis_showscale=False,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(
    fig_top_products,
    use_container_width=True
)

st.divider()

# =========================================================
# QUICK PRODUCT INSIGHTS
# =========================================================

best_product = top_products.iloc[0]

insight1, insight2 = st.columns(2)

with insight1:

    st.success(
        f"""
### 🥇 Best Selling Product

**{best_product['product_name']}**

Sales: **₹ {best_product['total_sales']:,.0f}**
"""
    )

with insight2:

    st.info(
        f"""
### 📦 Products Analysed

**{filtered_df['product_name'].nunique()}**

Unique products in current filters.
"""
    )

# =========================================================
# END OF PART 5
# =========================================================
# =========================================================
# PERFORMANCE ANALYTICS
# =========================================================

st.markdown(
    """
    <div class="section-title">
    🚀 Performance Analytics
    </div>
    """,
    unsafe_allow_html=True
)

performance_col1, performance_col2 = st.columns(2)

# =========================================================
# SALESPERSON PERFORMANCE
# =========================================================

with performance_col1:

    salesperson_df = (
        filtered_df
        .groupby("salesperson", as_index=False)["total_sales"]
        .sum()
        .sort_values("total_sales", ascending=False)
    )

    fig_salesperson = px.bar(
        salesperson_df,
        x="salesperson",
        y="total_sales",
        color="total_sales",
        template="plotly_dark",
        text_auto=".2s",
        title="Salesperson Performance"
    )

    fig_salesperson.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0", family="Inter", size=12),
        coloraxis_showscale=False,
        height=430,
        xaxis_title="Salesperson",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_salesperson,
        use_container_width=True
    )

# =========================================================
# PRODUCT PERFORMANCE
# =========================================================

with performance_col2:

    product_df = (
        filtered_df
        .groupby("product_name", as_index=False)["total_sales"]
        .sum()
        .sort_values("total_sales", ascending=False)
    )

    fig_product = px.bar(
        product_df,
        x="product_name",
        y="total_sales",
        color="total_sales",
        template="plotly_dark",
        text_auto=".2s",
        title="Product Performance"
    )

    fig_product.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0", family="Inter", size=12),
        coloraxis_showscale=False,
        height=430,
        xaxis_title="Product",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True
    )

st.divider()

# =========================================================
# PROFIT ANALYSIS
# =========================================================

st.markdown(
    """
    <div class="section-title">
    💹 Profit Analysis
    </div>
    """,
    unsafe_allow_html=True
)

profit_df = (
    filtered_df
    .groupby("product_name", as_index=False)["total_profit"]
    .sum()
    .sort_values("total_profit", ascending=False)
)

fig_profit = px.bar(
    profit_df,
    x="product_name",
    y="total_profit",
    color="total_profit",
    text_auto=".2s",
    template="plotly_dark",
    title="Profit by Product"
)

fig_profit.update_layout(
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font_color="white",
    coloraxis_showscale=False,
    height=450,
    xaxis_title="Product",
    yaxis_title="Profit"
)

st.plotly_chart(
    fig_profit,
    use_container_width=True
)

st.divider()

# =========================================================
# PERFORMANCE SUMMARY
# =========================================================

top_salesperson = salesperson_df.iloc[0]
top_profit_product = profit_df.iloc[0]

summary1, summary2 = st.columns(2)

with summary1:

    st.success(
        f"""
### 🏆 Best Salesperson

**{top_salesperson['salesperson']}**

Total Sales

**₹ {top_salesperson['total_sales']:,.0f}**
"""
    )

with summary2:

    st.info(
        f"""
### 💰 Most Profitable Product

**{top_profit_product['product_name']}**

Profit

**₹ {top_profit_product['total_profit']:,.0f}**
"""
    )

# =========================================================
# END OF PART 6
# =========================================================
# =========================================================
# SALES RECORD MANAGEMENT (OWNER + EMPLOYEE)
# =========================================================

st.markdown("<div class='section-title'>🛠️ Sales Record Management</div>", unsafe_allow_html=True)
if require_role(ROLE_OWNER, ROLE_EMPLOYEE):
    add_tab, edit_tab, delete_tab = st.tabs(["Add sale", "Edit sale", "Delete sale"])

    with add_tab:
        with st.form("add_sale_form", clear_on_submit=True):
            a1, a2, a3 = st.columns(3)
            new_date = a1.date_input("Sale date", value=date.today(), key="add_date")
            new_product = a2.text_input("Product name", max_chars=100, key="add_product")
            new_category = a3.text_input("Category", max_chars=50, key="add_category")
            a4, a5, a6 = st.columns(3)
            new_region = a4.text_input("Region", max_chars=50, key="add_region")
            new_salesperson = a5.text_input("Salesperson", max_chars=100, key="add_salesperson")
            new_quantity = a6.number_input("Quantity", min_value=1, step=1, value=1, key="add_quantity")
            a7, a8 = st.columns(2)
            new_unit_price = a7.number_input("Unit price", min_value=0.0, step=1.0, format="%.2f", key="add_unit_price")
            new_cost_price = a8.number_input("Cost price", min_value=0.0, step=1.0, format="%.2f", key="add_cost_price")
            add_submit = st.form_submit_button("Add sales record", use_container_width=True)
        if add_submit:
            if not require_role(ROLE_OWNER, ROLE_EMPLOYEE):
                st.error("You do not have permission to add sales.")
            elif not new_product.strip():
                st.error("Product name is required.")
            else:
                connection = get_db_connection()
                try:
                    cursor = connection.cursor()
                    total_sales_value = round(new_quantity * new_unit_price, 2)
                    total_profit_value = round(new_quantity * (new_unit_price - new_cost_price), 2)
                    cursor.execute("""INSERT INTO sales
                        (sale_date, product_name, category, region, salesperson, quantity, unit_price, cost_price, total_sales, total_profit)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (new_date, new_product.strip(), new_category.strip() or None, new_region.strip() or None,
                         new_salesperson.strip() or None, int(new_quantity), new_unit_price, new_cost_price,
                         total_sales_value, total_profit_value))
                    connection.commit()
                    load_data.clear()
                    st.success("Sales record added.")
                    st.rerun()
                except Exception as e:
                    connection.rollback()
                    st.error(f"Could not add sales record: {e}")
                finally:
                    connection.close()

    with edit_tab:
        sale_ids = sorted(int(x) for x in df["sale_id"].dropna().tolist())
        if sale_ids:
            selected_edit_id = st.selectbox("Select sale ID to edit", sale_ids, key="edit_sale_id")
            old_row = df.loc[df["sale_id"] == selected_edit_id].iloc[0]
            with st.form("edit_sale_form"):
                e1, e2, e3 = st.columns(3)
                edit_date = e1.date_input("Sale date", value=pd.to_datetime(old_row["sale_date"]).date(), key="edit_date")
                edit_product = e2.text_input("Product name", value=str(old_row["product_name"]), max_chars=100, key="edit_product")
                edit_category = e3.text_input("Category", value="" if pd.isna(old_row["category"]) else str(old_row["category"]), max_chars=50, key="edit_category")
                e4, e5, e6 = st.columns(3)
                edit_region = e4.text_input("Region", value="" if pd.isna(old_row["region"]) else str(old_row["region"]), max_chars=50, key="edit_region")
                edit_salesperson = e5.text_input("Salesperson", value="" if pd.isna(old_row["salesperson"]) else str(old_row["salesperson"]), max_chars=100, key="edit_salesperson")
                edit_quantity = e6.number_input("Quantity", min_value=1, step=1, value=max(1, int(old_row["quantity"])), key="edit_quantity")
                e7, e8 = st.columns(2)
                edit_unit_price = e7.number_input("Unit price", min_value=0.0, step=1.0, value=float(old_row["unit_price"]), format="%.2f", key="edit_unit_price")
                edit_cost_price = e8.number_input("Cost price", min_value=0.0, step=1.0, value=float(old_row["cost_price"]), format="%.2f", key="edit_cost_price")
                edit_submit = st.form_submit_button("Save changes", use_container_width=True)
            if edit_submit:
                if not require_role(ROLE_OWNER, ROLE_EMPLOYEE):
                    st.error("You do not have permission to edit sales.")
                elif not edit_product.strip():
                    st.error("Product name is required.")
                else:
                    connection = get_db_connection()
                    try:
                        cursor = connection.cursor()
                        total_sales_value = round(edit_quantity * edit_unit_price, 2)
                        total_profit_value = round(edit_quantity * (edit_unit_price - edit_cost_price), 2)
                        cursor.execute("""UPDATE sales SET sale_date=%s, product_name=%s, category=%s, region=%s,
                            salesperson=%s, quantity=%s, unit_price=%s, cost_price=%s, total_sales=%s, total_profit=%s
                            WHERE sale_id=%s""",
                            (edit_date, edit_product.strip(), edit_category.strip() or None, edit_region.strip() or None,
                             edit_salesperson.strip() or None, int(edit_quantity), edit_unit_price, edit_cost_price,
                             total_sales_value, total_profit_value, int(selected_edit_id)))
                        connection.commit()
                        load_data.clear()
                        st.success("Sales record updated.")
                        st.rerun()
                    except Exception as e:
                        connection.rollback()
                        st.error(f"Could not update sales record: {e}")
                    finally:
                        connection.close()
        else:
            st.info("No sales records are available to edit.")

    with delete_tab:
        sale_ids_to_delete = sorted(int(x) for x in df["sale_id"].dropna().tolist())
        if sale_ids_to_delete:
            delete_id = st.selectbox("Select sale ID to delete", sale_ids_to_delete, key="delete_sale_id")
            st.warning("Deleting a record is permanent. Confirm the selected sale ID before proceeding.")
            confirm_delete = st.checkbox("I confirm that I want to delete this sales record.")
            if st.button("Delete selected sale", type="primary", disabled=not confirm_delete):
                if not require_role(ROLE_OWNER, ROLE_EMPLOYEE):
                    st.error("You do not have permission to delete sales.")
                else:
                    connection = get_db_connection()
                    try:
                        cursor = connection.cursor()
                        cursor.execute("DELETE FROM sales WHERE sale_id = %s", (int(delete_id),))
                        connection.commit()
                        load_data.clear()
                        st.success("Sales record deleted.")
                        st.rerun()
                    except Exception as e:
                        connection.rollback()
                        st.error(f"Could not delete sales record: {e}")
                    finally:
                        connection.close()
else:
    st.info("Your Admin role is read-only. You can view and export dashboard data, but cannot change sales records.")


# =========================================================
# OWNER USER AND ROLE MANAGEMENT
# =========================================================

if require_role(ROLE_OWNER):
    st.markdown("<div class='section-title'>👥 User and Role Management</div>", unsafe_allow_html=True)
    create_user_tab, manage_user_tab = st.tabs(["Create account", "Manage accounts"])
    with create_user_tab:
        with st.form("create_user_form", clear_on_submit=True):
            account_username = st.text_input("New username", max_chars=80)
            account_password = st.text_input("Temporary password (minimum 12 characters)", type="password")
            account_role = st.selectbox("Role", [ROLE_ADMIN, ROLE_EMPLOYEE])
            create_account = st.form_submit_button("Create account", use_container_width=True)
        if create_account:
            if not require_role(ROLE_OWNER):
                st.error("Only the Owner can create accounts.")
            elif not account_username.strip() or len(account_password) < 12:
                st.error("Enter a username and a password of at least 12 characters.")
            else:
                connection = get_db_connection()
                try:
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO app_users (username, password_hash, role, is_active) VALUES (%s,%s,%s,TRUE)",
                                   (account_username.strip(), password_hash(account_password), account_role))
                    connection.commit()
                    st.success(f"Account created for {account_username.strip()} with role {account_role}.")
                except psycopg2.IntegrityError:
                    connection.rollback()
                    st.error("That username already exists.")
                except Exception as e:
                    connection.rollback()
                    st.error(f"Could not create account: {e}")
                finally:
                    connection.close()
    with manage_user_tab:
        connection = get_db_connection()
        try:
            users_df = pd.read_sql("SELECT user_id, username, role, is_active, created_at FROM app_users ORDER BY user_id", connection)
        finally:
            connection.close()
        st.dataframe(users_df, use_container_width=True, hide_index=True)
        manageable = users_df[users_df["role"] != ROLE_OWNER]
        if not manageable.empty:
            chosen_user_id = st.selectbox("Choose account", manageable["user_id"].astype(int).tolist(), key="manage_user_id")
            chosen_user = manageable.loc[manageable["user_id"] == chosen_user_id].iloc[0]
            m1, m2 = st.columns(2)
            new_role = m1.selectbox("Change role", [ROLE_ADMIN, ROLE_EMPLOYEE], index=0 if chosen_user["role"] == ROLE_ADMIN else 1, key="manage_role")
            desired_active = m2.selectbox("Account status", ["Active", "Disabled"], index=0 if int(chosen_user["is_active"]) else 1, key="manage_status")
            if st.button("Save account changes", use_container_width=True):
                if not require_role(ROLE_OWNER):
                    st.error("Only the Owner can manage accounts.")
                else:
                    connection = get_db_connection()
                    try:
                        cursor = connection.cursor()
                        cursor.execute("UPDATE app_users SET role=%s, is_active=%s WHERE user_id=%s AND role <> 'OWNER'",
                                       (new_role, desired_active == "Active", int(chosen_user_id)))
                        connection.commit()
                        st.success("Account updated.")
                        st.rerun()
                    except Exception as e:
                        connection.rollback()
                        st.error(f"Could not update account: {e}")
                    finally:
                        connection.close()

st.divider()

# =========================================================
# SALES DATA
# =========================================================

st.markdown(
    """
    <div class="section-title">
    📋 Sales Data
    </div>
    """,
    unsafe_allow_html=True
)

display_df = filtered_df.copy()

display_df["sale_date"] = (
    display_df["sale_date"]
    .dt.strftime("%d-%m-%Y")
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=500
)

st.divider()

# =========================================================
# DOWNLOAD REPORT
# =========================================================

st.markdown(
    """
    <div class="section-title">
    📥 Export Dashboard Data
    </div>
    """,
    unsafe_allow_html=True
)

download_col1, download_col2 = st.columns([1,2])

with download_col1:

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        data=csv,
        file_name="sales_dashboard_report.csv",
        mime="text/csv",
        use_container_width=True
    )

with download_col2:

    st.info(
        """
Download the filtered dataset currently visible on the dashboard.
The exported CSV includes all active filters.
"""
    )

st.divider()

# =========================================================
# DASHBOARD SUMMARY
# =========================================================

st.markdown(
    """
    <div class="section-title">
    📌 Dashboard Summary
    </div>
    """,
    unsafe_allow_html=True
)

summary1, summary2, summary3 = st.columns(3)

with summary1:
    st.success(
        f"""
### 📦 Records

**{len(filtered_df):,}**

Sales Records
"""
    )

with summary2:
    st.info(
        f"""
### 📅 Date Range

**{filtered_df['sale_date'].min().strftime('%d %b %Y')}**

to

**{filtered_df['sale_date'].max().strftime('%d %b %Y')}**
"""
    )

with summary3:
    st.warning(
        f"""
### 📈 Categories

**{filtered_df['category'].nunique()}**

Business Categories
"""
    )

st.divider()

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="dashboard-footer">

<b>Sales Performance Dashboard</b><br><br>

Developed using
<b>Python • Streamlit • PostgreSQL • Pandas • Plotly</b>

<br><br>

© 2026 Group Project

</div>
    """,
    unsafe_allow_html=True
)
