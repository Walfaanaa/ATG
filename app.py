import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="ATG Management System",
    layout="wide"
)

# ==========================
# STYLE
# ==========================
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: white;
}

/* Make all text black */
html, body, p, span, div, label {
    color: black !important;
}

/* Markdown text */
[data-testid="stMarkdownContainer"] {
    color: black !important;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: black !important;
    font-weight: bold;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #006400 !important;
    font-weight: bold;
}

/* DataFrame */
[data-testid="stDataFrame"] {
    color: black !important;
}

/* Tables */
table {
    color: black !important;
}

/* Subheaders */
h2, h3 {
    color: #006400 !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# LOGO
# ==========================
LOGO_URL = "https://raw.githubusercontent.com/Walfaanaa/ATG/main/ATG.jpg"

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(LOGO_URL, width=300)

st.markdown(
    "<h1 style='text-align:center; color:#006400;'>Sirna to`annaa Buusii Afoosha Tokkummaa Gaalessaa</h1>",
    unsafe_allow_html=True
)

# ==========================
# SETTINGS
# ==========================
MONTHLY_PAYMENT = 200
PENALTY = MONTHLY_PAYMENT * 0.5

# ==========================
# EXCEL FILE
# ==========================
EXCEL_URL = "https://raw.githubusercontent.com/Walfaanaa/ATG/main/ATG.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_URL, engine="openpyxl")

try:
    df = load_data()
except Exception as e:
    st.error("Unable to load the Excel file.")
    st.error(e)
    st.stop()

# ==========================
# CLEAN COLUMN NAMES
# ==========================
df.columns = (
    df.columns.str.strip()
              .str.lower()
              .str.replace(" ", "_")
              .str.replace("`", "")
)

required = [
    "lakk",
    "maqaa",
    "guyyaa_buusi",
    "buusii_jiaa",
    "buusii_dabalataa",
    "guyyaa_xummuraa",
    "amma_adabbii"
]

missing = [c for c in required if c not in df.columns]

if missing:
    st.error("Missing columns:")
    st.write(missing)
    st.write("Columns found:")
    st.write(df.columns.tolist())
    st.stop()

# ==========================
# DATA CLEANING
# ==========================
df["buusii_jiaa"] = pd.to_numeric(
    df["buusii_jiaa"],
    errors="coerce"
).fillna(0)

df["buusii_dabalataa"] = pd.to_numeric(
    df["buusii_dabalataa"],
    errors="coerce"
).fillna(0)

# Penalty
df["Penalty"] = df["buusii_jiaa"].apply(
    lambda x: PENALTY if x < MONTHLY_PAYMENT else 0
)

# ==========================
# KPI
# ==========================
total_members = len(df)

paid_members = (df["buusii_jiaa"] >= MONTHLY_PAYMENT).sum()

unpaid_members = (df["buusii_jiaa"] < MONTHLY_PAYMENT).sum()

total_collected = df["buusii_jiaa"].sum()

total_penalty = df["Penalty"].sum()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("👥 Baay`na Miseensotaa", total_members)
c2.metric("✅ Baay`na Miseensota Kanfalanii", paid_members)
c3.metric("Baay`na Miseensota Adabamanii", unpaid_members)
c4.metric("Waliigala Maallaqa guuramee", f"{total_collected:,.0f} ETB")
c5.metric("Waliigala maallaqa adabbiirraa argamee", f"{total_penalty:,.0f} ETB")

st.divider()

# ==========================
# NON-PAID MEMBERS
# ==========================
st.subheader("Miseensota Buusii Ji`a Kanaa hin kanfaliin.")

non_paid = df[df["buusii_jiaa"] < MONTHLY_PAYMENT].copy()

non_paid["Remaining"] = MONTHLY_PAYMENT - non_paid["buusii_jiaa"]

st.dataframe(
    non_paid[
        [
            "lakk",
            "maqaa",
            "buusii_jiaa",
            "Remaining",
            "Penalty"
        ]
    ],
    use_container_width=True
)

st.divider()

# ==========================
# FULL DATA
# ==========================
st.subheader("📄 All Members")

st.dataframe(df, use_container_width=True)
