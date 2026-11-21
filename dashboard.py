import streamlit as st
import mysql.connector
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


# =========================================================
# PREMIUM CSS
# =========================================================

# =========================================================
# MODERN SAAS - PROFESSIONAL BUSINESS DASHBOARD CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
    --bg:#F5F7FB;
    --white:#FFFFFF;
    --text:#172B4D;
    --muted:#64748B;
    --blue:#2563EB;
    --blue-dark:#1D4ED8;
    --blue-light:#EFF6FF;
    --border:#E5EAF1;
    --green:#16A34A;
}

html, body, [class*="css"], .stApp{
    font-family:'Inter',sans-serif;
    color:var(--text);
}

.stApp{
    background:var(--bg);
}

/* Main layout */
.block-container{
    max-width:1600px;
    padding:2rem 2.5rem 3rem;
}

/* Hide default Streamlit branding */
#MainMenu, footer,{
    visibility:hidden;
}
/* Streamlit Header Visibility Fix */
header[data-testid="stHeader"] {
    background-color: #FFFFFF !important;
    visibility: visible !important;
}

header[data-testid="stHeader"] * {
    color: #172B4D !important;
}
/* Main heading */
.main-title {
    font-size: clamp(24px, 2.5vw, 32px);
    font-weight: 800;
    line-height: 1.4;
    letter-spacing: -0.5px;
    padding-top: 8px;
}
    color:#172B4D;
    margin-bottom:7px;
}

.sub-title{
    font-size:14px;
    font-weight:400;
    color:#64748B;
}

/* Section headings */
.section-title{
    position:relative;
    display:flex;
    align-items:center;
    gap:10px;
    font-size:21px;
    font-weight:700;
    color:#172B4D;
    letter-spacing:-.4px;
    margin:35px 0 20px;
    padding-bottom:13px;
    border-bottom:1px solid var(--border);
}

.section-title:after{
    content:"";
    position:absolute;
    left:0;
    bottom:-1px;
    width:48px;
    height:3px;
    border-radius:3px;
    background:var(--blue);
}

/* Dividers */
hr{
    border:0!important;
    height:1px!important;
    margin:26px 0!important;
    background:var(--border)!important;
}

/* KPI cards */
div[data-testid="metric-container"]{
    position:relative;
    min-height:115px;
    padding:20px!important;
    background:#FFFFFF!important;
    border:1px solid var(--border)!important;
    border-radius:12px!important;
    box-shadow:0 2px 7px rgba(15,23,42,.035);
    transition:all .2s ease;
}

div[data-testid="metric-container"]:before{
    content:"";
    position:absolute;
    left:0;
    top:15px;
    bottom:15px;
    width:4px;
    background:var(--blue);
    border-radius:0 4px 4px 0;
}

div[data-testid="metric-container"]:hover{
    border-color:#BFDBFE!important;
    box-shadow:0 5px 16px rgba(37,99,235,.08);
    transform:translateY(-2px);
}

div[data-testid="metric-container"] label,
div[data-testid="stMetricLabel"]{
    color:#64748B!important;
    font-size:11px!important;
    font-weight:650!important;
    text-transform:uppercase;
    letter-spacing:.55px;
}

div[data-testid="stMetricValue"]{
    color:#172B4D!important;
    font-size:26px!important;
    font-weight:750!important;
    letter-spacing:-.7px;
    margin-top:7px;
}

div[data-testid="stMetricDelta"]{
    font-size:11px!important;
}

/* Buttons */
.stButton>button,
.stDownloadButton>button,
.stFormSubmitButton>button{
    min-height:42px;
    border:1px solid var(--blue)!important;
    border-radius:8px!important;
    background:var(--blue)!important;
    color:#FFFFFF!important;
    font-size:13px!important;
    font-weight:650!important;
    box-shadow:none!important;
    transition:background .2s ease;
}

.stButton>button:hover,
.stDownloadButton>button:hover,
.stFormSubmitButton>button:hover{
    background:var(--blue-dark)!important;
    border-color:var(--blue-dark)!important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#FFFFFF!important;
    border-right:1px solid var(--border);
}

section[data-testid="stSidebar"] > div{
    padding:1.5rem 1rem 2rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:#172B4D!important;
    font-weight:700!important;
}

section[data-testid="stSidebar"] label{
    color:#475569!important;
    font-size:12px!important;
    font-weight:600!important;
}

/* Sidebar navigation */
section[data-testid="stSidebar"] [data-testid="stPageLink"]{
    border-radius:8px;
    padding:7px 10px;
}

section[data-testid="stSidebar"] [data-testid="stPageLink"]:hover{
    background:var(--blue-light);
}

/* Inputs */
[data-baseweb="input"] > div,
[data-baseweb="select"] > div{
    background:#FFFFFF!important;
    border:1px solid #CBD5E1!important;
    border-radius:8px!important;
    min-height:40px;
}

[data-baseweb="input"] > div:focus-within,
[data-baseweb="select"] > div:focus-within{
    border-color:var(--blue)!important;
    box-shadow:0 0 0 1px var(--blue)!important;
}

[data-baseweb="input"] input,
[data-baseweb="select"] input{
    color:#172B4D!important;
}

/* Date picker */
div[data-testid="stDateInput"] input{
    background:#FFFFFF!important;
    border:1px solid #CBD5E1!important;
    border-radius:8px!important;
    color:#172B4D!important;
}

/* Forms */
div[data-testid="stForm"]{
    background:#FFFFFF;
    border:1px solid var(--border);
    border-radius:12px;
    padding:20px;
}

/* Tabs */
button[data-baseweb="tab"]{
    color:#64748B!important;
    font-weight:600!important;
}

button[data-baseweb="tab"][aria-selected="true"]{
    color:var(--blue)!important;
    border-bottom-color:var(--blue)!important;
}

/* Alerts and status */
div[data-testid="stAlert"]{
    background:#FFFFFF!important;
    border:1px solid var(--border)!important;
    border-radius:10px!important;
    box-shadow:none!important;
}

/* Chart containers */
div[data-testid="stPlotlyChart"]{
    background:#FFFFFF;
    border:1px solid var(--border);
    border-radius:12px;
    padding:10px;
    box-shadow:0 2px 8px rgba(15,23,42,.035);
}

/* Dataframes */
div[data-testid="stDataFrame"]{
    background:#FFFFFF!important;
    border:1px solid var(--border)!important;
    border-radius:10px!important;
    overflow:hidden!important;
    box-shadow:0 2px 8px rgba(15,23,42,.035);
}

/* Data tables */
div[data-testid="stTable"]{
    background:#FFFFFF;
    border:1px solid var(--border);
    border-radius:10px;
    overflow:hidden;
}

/* Dropdown menus */
[data-baseweb="popover"],
[data-baseweb="menu"]{
    background:#FFFFFF!important;
    border:1px solid var(--border)!important;
    border-radius:8px!important;
}

[data-baseweb="menu"] li{
    color:#172B4D!important;
}

[data-baseweb="menu"] li:hover{
    background:var(--blue-light)!important;
}

/* Captions */
[data-testid="stCaptionContainer"],
.stCaption{
    color:#64748B!important;
    font-size:12px!important;
}

/* Footer */
.dashboard-footer{
    margin-top:35px;
    padding:24px;
    text-align:center;
    color:#64748B;
    font-size:12px;
    line-height:1.8;
    background:#FFFFFF;
    border:1px solid var(--border);
    border-radius:12px;
}

.dashboard-footer b{
    color:#172B4D;
}

/* Scrollbar */
::-webkit-scrollbar{
    width:8px;
    height:8px;
}

::-webkit-scrollbar-track{
    background:#F1F5F9;
}

::-webkit-scrollbar-thumb{
    background:#CBD5E1;
    border-radius:8px;
}

/* Responsive */
@media(max-width:1100px){
    .block-container{
        padding-left:1.25rem;
        padding-right:1.25rem;
    }
}

@media(max-width:760px){
    .block-container{
        padding:1rem .8rem 2rem;
    }

    .section-title{
        font-size:19px;
        margin-top:28px;
    }

    div[data-testid="metric-container"]{
        min-height:100px;
        padding:15px!important;
    }

    div[data-testid="stMetricValue"]{
        font-size:22px!important;
    }
}
/* =====================================================
   VISIBILITY FIX - INPUTS, LABELS AND KPI TEXT
===================================================== */

/* General dashboard text */
.stApp,
.stApp p,
.stApp label,
.stApp .stMarkdown,
.stApp [data-testid="stWidgetLabel"] p {
    color: #172B4D !important;
}

/* Username and password input fields */
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
    caret-color: #2563EB !important;
}

/* Input placeholder text */
[data-baseweb="input"] input::placeholder {
    color: #94A3B8 !important;
    -webkit-text-fill-color: #94A3B8 !important;
}

/* Username and password labels */
div[data-testid="stWidgetLabel"] p,
div[data-testid="stTextInput"] label {
    color: #172B4D !important;
    font-weight: 600 !important;
}

/* KPI headings */
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p {
    color: #475569 !important;
    font-weight: 700 !important;
}

/* KPI numbers */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] div {
    color: #172B4D !important;
    -webkit-text-fill-color: #172B4D !important;
}

/* KPI supporting text */
div[data-testid="stMetricDelta"] {
    color: #64748B !important;
}

/* Selectbox and date input text */
[data-baseweb="select"] *,
div[data-testid="stDateInput"] input {
    color: #172B4D !important;
}

/* Login form background */
div[data-testid="stForm"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E5EAF1 !important;
}
/* Login form background */
div[data-testid="stForm"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E5EAF1 !important;
}
/* =====================================================
   PLOTLY CHART TEXT VISIBILITY FIX
===================================================== */

.js-plotly-plot .infolayer text,
.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text,
.js-plotly-plot .gtitle,
.js-plotly-plot .legendtext,
.js-plotly-plot .g-xtitle text,
.js-plotly-plot .g-ytitle text,
.js-plotly-plot .slicetext {
    fill: #172B4D !important;
    color: #172B4D !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)


from auth_helpers import (
    ROLE_OWNER,
    ROLE_ADMIN,
    ROLE_EMPLOYEE,
    ALLOWED_ROLES,
    get_db_connection,
    password_hash,
    password_matches,
    initialise_auth,
    authenticate,
    require_role,
)

try:
    auth_ready, auth_message = initialise_auth()
except Exception as auth_error:
    st.error(
        "Authentication/database setup failed. "
        "Check the PostgreSQL secrets and database permissions."
    )
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
# MYSQL CONNECTION
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
        template="plotly_white",
        title="Monthly Sales & Profit"
    )

    fig_monthly.update_layout(

        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",

        font=dict(color="#243247", family="Inter", size=12),

        legend_title="",

        height=430,

        margin=dict(l=20, r=20, t=60, b=20),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="rgba(148,163,184,.25)",
            font=dict(color="#243247", family="Inter", size=12)
        ),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#e5e7eb", zeroline=False)
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

        template="plotly_white",

        title="Daily Sales"

    )

    fig_daily.update_layout(

        paper_bgcolor="#FFFFFF",

        plot_bgcolor="#FFFFFF",

        font_color="#172B4D",

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
        template="plotly_white",
        title="Sales by Category"
    )

    fig_category.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig_category.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#172B4D", family="Inter", size=12),
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
        text_auto=".2s",
        template="plotly_white",
        title="Sales by Region"
    )
    fig_region.update_traces(
    marker_color="#3B82F6"
)

    fig_region.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#172B4D", family="Inter", size=12),
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
    text_auto=".2s",
    template="plotly_white",
    title="Best Selling Products"
    
)
fig_top_products.update_traces(
    marker_color="#3B82F6"
)

fig_top_products.update_layout(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    font_color="#172B4D",
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
        template="plotly_white",
        text_auto=".2s",
        title="Salesperson Performance"
    )
    fig_salesperson.update_traces(
    marker_color="#3B82F6"
)

    fig_salesperson.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#172B4D", family="Inter", size=12),
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
        template="plotly_white",
        text_auto=".2s",
        title="Product Performance"
    )
    fig_product.update_traces(
    marker_color="#3B82F6"
)

    fig_product.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#172B4D", family="Inter", size=12),
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
    text_auto=".2s",
    template="plotly_white",
    title="Profit by Product"
)
fig_profit.update_traces(
    marker_color="#3B82F6"
)

fig_profit.update_layout(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    font_color="#172B4D",
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
<b>Python • Streamlit • Supabase PostgreSQL • Pandas • Plotly</b>

<br><br>

© 2026 Group Project

</div>
    """,
    unsafe_allow_html=True
)