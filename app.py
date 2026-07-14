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

.stApp {
    background-color: white;
}

/* General text */
html, body, p, span, div, label {
    color: black !important;
    font-size: 18px !important;
}

/* Markdown */
[data-testid="stMarkdownContainer"] {
    color: black !important;
    font-size: 18px !important;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: black !important;
    font-weight: bold !important;
    font-size: 22px !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: black !important;
    font-weight: 900 !important;
    font-size: 40px !important;
}

/* Metric delta */
[data-testid="stMetricDelta"] {
    font-size: 18px !important;
    font-weight: bold !important;
}

/* Headers */
h1 {
    font-size: 40px !important;
}

h2, h3 {
    color: #006400 !important;
    font-size: 28px !important;
    font-weight: bold !important;
}

/* Filter labels */
.stSelectbox label,
.stDateInput label {
    font-size: 20px !important;
    font-weight: bold !important;
    color: black !important;
}

/* ===== DATAFRAME ===== */

/* Header */
[data-testid="stDataFrame"] th {
    font-size: 22px !important;
    font-weight: bold !important;
    color: black !important;
    text-align: center !important;
}

/* Cells */
[data-testid="stDataFrame"] td {
    font-size: 20px !important;
    color: black !important;
}

/* Row height */
[data-testid="stDataFrame"] tbody tr {
    height: 48px !important;
}

</style>
""", unsafe_allow_html=True)
# ==========================
# LOGO
# ==========================
LOGO_URL = "https://raw.githubusercontent.com/Walfaanaa/ATG/main/Screenshot_20260714-124309.jpg"

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(LOGO_URL, width=300)


st.markdown(
    "<h1 style='text-align:center; color:#006400;'>Sirna To`annaa Buusii Waliigalaa Afoosha Ollaa</h1>",
    unsafe_allow_html=True
)

# ==========================
# SETTINGS
# ==========================
MONTHLY_PAYMENT = 200
PENALTY = MONTHLY_PAYMENT * 0.25
# ==========================
# LOAD EXCEL
# ==========================
EXCEL_URL = "https://raw.githubusercontent.com/Walfaanaa/ATG/main/ATG.xlsx"
@st.cache_data
def load_data():
    return pd.read_excel(
        EXCEL_URL,
        engine="openpyxl"
    )


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
    df.columns
    .str.strip()
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


missing = [
    c for c in required
    if c not in df.columns
]


if missing:
    st.error("Missing columns:")
    st.write(missing)
    st.write(df.columns.tolist())
    st.stop()


# ==========================
# DATA CLEANING
# ==========================

df["guyyaa_buusi"] = pd.to_datetime(
    df["guyyaa_buusi"],
    errors="coerce"
)


df["buusii_jiaa"] = pd.to_numeric(
    df["buusii_jiaa"],
    errors="coerce"
).fillna(0)


df["buusii_dabalataa"] = pd.to_numeric(
    df["buusii_dabalataa"],
    errors="coerce"
).fillna(0)


# ==========================
# PENALTY CALCULATION
# ==========================

df["Penalty"] = 0

df.loc[
    df["buusii_jiaa"] < MONTHLY_PAYMENT,
    "Penalty"
] = PENALTY

# ==========================
# FILTER
# ==========================

st.markdown("### Filteera")

f1, f2 = st.columns(2)


with f1:

    selected_id = st.selectbox(
        "Lakk (ID)",
        ["All"] +
        sorted(
            df["lakk"].astype(str).unique().tolist()
        )
    )


with f2:

    selected_date = st.date_input(
        "Guyyaa Buusi",
        value=df["guyyaa_buusi"].max().date()
    )
# ==========================
# DATE FILTER DATA
# ==========================

filtered_df = df.copy()


if selected_id != "All":

    filtered_df = filtered_df[
        filtered_df["lakk"].astype(str) == selected_id
    ]


filtered_df = filtered_df[
    filtered_df["guyyaa_buusi"].dt.date == selected_date
]
# ==========================
# UNPAID CALCULATION
# ==========================

unpaid_df = df.copy()


if selected_id != "All":

    unpaid_df = unpaid_df[
        unpaid_df["lakk"].astype(str) == selected_id
    ]


unpaid_df = unpaid_df[
    unpaid_df["buusii_jiaa"] < MONTHLY_PAYMENT
].copy()
unpaid_members = len(unpaid_df)
unpaid_amount = (
    MONTHLY_PAYMENT -
    unpaid_df["buusii_jiaa"]
).sum()

# ==========================
# KPI
# ==========================

total_members = len(filtered_df)+unpaid_members


paid_members = (
    filtered_df["buusii_jiaa"] >= MONTHLY_PAYMENT
).sum()
total_collected = filtered_df["buusii_jiaa"].sum()
# Correct penalty calculation
total_penalty = len(unpaid_df) * PENALTY

# ==========================
# KPI DISPLAY
# ==========================
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "👥 Baay`ina Miseensotaa",
    total_members
)
c2.metric(
    "✅ Baay`ina Miseensota Kanfalanii",
    paid_members
)

c3.metric(
    "❌ Baay`ina Miseensota Adabamanii",
    unpaid_members,
    delta=f"{unpaid_members} Miseenstota ji`a kana osoo hin kanfaliin hafan",
    delta_color="inverse"   # Red when positive
)
c4.metric(
    "Waliigala Maallaqa guuramee",
    f"{total_collected:,.0f} ETB"
)
c5.metric(
    "Waliigala maallaqa adabbiirraa argamee",
    f"{total_penalty:,.0f} ETB"
)
c6.metric(
    "💸 Maallaqa Hin Kaffalamne",
    f"{unpaid_amount:,.0f} ETB"
)
st.divider()

# ==========================
# NON PAID MEMBERS
# ==========================
st.subheader(
    "Miseensota Buusii Ji`a Kanaa hin kanfaliin."
)
non_paid = unpaid_df.copy()
non_paid["Remaining"] = (
    MONTHLY_PAYMENT -
    non_paid["buusii_jiaa"]
)
non_paid["Penalty"] = PENALTY
non_paid["Total_Due"] = (
    non_paid["Remaining"] +
    non_paid["Penalty"]
)
st.dataframe(
    non_paid[
        [
            "lakk",
            "maqaa",
            "buusii_jiaa",
            "Remaining",
            "Penalty",
           "Total_Due"]],
    use_container_width=True,
    height=150
)
# ==========================
# FULL DATA
# ==========================
st.subheader("Tarree Miseensoota Waliigalaa")
st.dataframe(
    filtered_df,
    use_container_width=True
)
