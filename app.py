import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="ATG Management System",
    page_icon="💰",
    layout="wide"
)

# ======================================================
# STYLE
# ======================================================
st.markdown("""
<style>

.stApp{
    background:white;
}

/* General text */
html, body, div, span, p, label{
    color:black !important;
    font-size:18px !important;
}

/* Headers */
h1{
    text-align:center;
    color:#006400;
    font-size:42px !important;
    font-weight:bold;
}

h2,h3{
    color:#006400;
    font-weight:bold;
}

/* Metrics */
[data-testid="stMetricLabel"]{
    font-size:20px !important;
    font-weight:bold !important;
}

[data-testid="stMetricValue"]{
    font-size:36px !important;
    font-weight:bold !important;
}

/* DataFrame */
[data-testid="stDataFrame"] th{
    font-size:18px !important;
    font-weight:bold;
    text-align:center;
}

[data-testid="stDataFrame"] td{
    font-size:17px !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#F5F5F5;
}

</style>
""", unsafe_allow_html=True)

# LOGO

LOGO_URL = "https://github.com/Walfaanaa/AL/tree/main/AO.jpg"

c1,c2,c3 = st.columns([1,2,1])

with c2:
    st.image(LOGO_URL,width=260)

st.markdown("""
<h1>
Sirna To'annaa Buusii Waliigalaa Afoosha Ollaa
</h1>
""",unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.header("⚙️ Settings")

source = st.sidebar.radio(
    "Choose Data Source",
    [
        "MySQL",
        "Excel"
    ]
)

# ======================================================
# MYSQL SETTINGS
# ======================================================

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "your_password"
MYSQL_DATABASE = "your_database"
MYSQL_TABLE = "ao"

# ======================================================
# EXCEL SETTINGS
# ======================================================

EXCEL_URL = "https://raw.githubusercontent.com/Walfaanaa/AL/main/AOL.xlsx"

# ======================================================
# LOAD MYSQL
# ======================================================

@st.cache_data(show_spinner=False)
def load_mysql():

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    query = f"""
    SELECT
        business_date,
        Id_no,
        Full_name,
        Phone_no,
        Monthly_payment,
        Additional_payment,
        Total_payment,
        loan
    FROM {MYSQL_TABLE}
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

# ======================================================
# LOAD EXCEL
# ======================================================

@st.cache_data(show_spinner=False)
def load_excel():

    return pd.read_excel(
        EXCEL_URL,
        engine="openpyxl"
    )

# ======================================================
# LOAD DATA
# ======================================================

try:

    if source=="MySQL":
        df=load_mysql()

    else:
        df=load_excel()

except Exception as e:

    st.error("Unable to load data.")
    st.exception(e)
    st.stop()

# ======================================================
# CLEAN COLUMN NAMES
# ======================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

# ======================================================
# REQUIRED COLUMNS
# ======================================================

required = [
    "business_date",
    "id_no",
    "full_name",
    "phone_no",
    "monthly_payment",
    "additional_payment",
    "total_payment",
    "loan"
]

missing = [
    c
    for c in required
    if c not in df.columns
]

if missing:

    st.error("Missing columns")

    st.write(missing)

    st.stop()

# ======================================================
# DATA TYPES
# ======================================================

df["business_date"] = pd.to_datetime(
    df["business_date"],
    errors="coerce"
)

numeric = [
    "monthly_payment",
    "additional_payment",
    "total_payment",
    "loan"
]

for c in numeric:

    df[c] = (
        pd.to_numeric(
            df[c],
            errors="coerce"
        )
        .fillna(0)
    )
