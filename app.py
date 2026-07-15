import streamlit as st
import pandas as pd
import plotly.express as px


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

html, body, div, span, p, label{
    color:black !important;
    font-size:18px !important;
}

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


[data-testid="stMetricLabel"]{
    font-size:20px !important;
    font-weight:bold !important;
}

[data-testid="stMetricValue"]{
    font-size:35px !important;
    font-weight:bold !important;
}


[data-testid="stDataFrame"] th{
    font-size:18px !important;
    font-weight:bold;
}

[data-testid="stDataFrame"] td{
    font-size:17px !important;
}


section[data-testid="stSidebar"]{
    background:#F5F5F5;
}


</style>
""", unsafe_allow_html=True)



# ======================================================
# LOGO
# ======================================================

LOGO_URL = "https://raw.githubusercontent.com/Walfaanaa/AL/main/AO.jpg"


col1,col2,col3 = st.columns([1,2,1])

with col2:
    st.image(
        LOGO_URL,
        width=260
    )


st.markdown("""
<h1>
Sirna To'annaa Buusii Waliigalaa Afoosha Ollaa
</h1>
""",
unsafe_allow_html=True)



# ======================================================
# LOAD EXCEL
# ======================================================

EXCEL_FILE = "AOL.xlsx"


@st.cache_data
def load_data():

    df = pd.read_excel(
        EXCEL_FILE,
        engine="openpyxl"
    )

    return df



try:

    df = load_data()


except Exception as e:

    st.error("Unable to load Excel file")
    st.write(e)
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
# CHECK COLUMNS
# ======================================================

required_columns = [

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

    c for c in required_columns
    if c not in df.columns

]


if missing:

    st.error("Missing Excel columns")

    st.write(missing)

    st.stop()



# ======================================================
# DATA CLEANING
# ======================================================


df["business_date"] = pd.to_datetime(
    df["business_date"],
    errors="coerce"
)



money_columns = [

    "monthly_payment",
    "additional_payment",
    "total_payment",
    "loan"

]


for c in money_columns:

    df[c] = pd.to_numeric(
        df[c],
        errors="coerce"
    ).fillna(0)



# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.header("⚙️ Filter")


names = [

    "All"

] + sorted(
    df["full_name"]
    .dropna()
    .unique()
    .tolist()
)


selected_name = st.sidebar.selectbox(
    "Member",
    names
)



if selected_name != "All":

    df_view = df[
        df["full_name"] == selected_name
    ]

else:

    df_view = df.copy()



# ======================================================
# KPI METRICS
# ======================================================


total_loan = df_view["loan"].sum()

monthly = df_view["monthly_payment"].sum()

additional = df_view["additional_payment"].sum()

total_payment = df_view["total_payment"].sum()



c1,c2,c3,c4 = st.columns(4)


with c1:
    st.metric(
        "💰 Total Loan",
        f"{total_loan:,.2f}"
    )


with c2:
    st.metric(
        "📅 Monthly Payment",
        f"{monthly:,.2f}"
    )


with c3:
    st.metric(
        "➕ Additional Payment",
        f"{additional:,.2f}"
    )


with c4:
    st.metric(
        "✅ Total Payment",
        f"{total_payment:,.2f}"
    )



# ======================================================
# CHARTS
# ======================================================


st.subheader("Payment Summary")


chart_df = pd.DataFrame({

    "Type":[
        "Monthly Payment",
        "Additional Payment",
        "Total Payment"
    ],

    "Amount":[
        monthly,
        additional,
        total_payment
    ]

})


fig = px.bar(

    chart_df,
    x="Type",
    y="Amount",
    text="Amount"

)


fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ======================================================
# DATA TABLE
# ======================================================


st.subheader("Member Payment Details")


st.dataframe(

    df_view,

    use_container_width=True,

    height=500

)


# ======================================================
# DOWNLOAD
# ======================================================

from io import BytesIO


buffer = BytesIO()

with pd.ExcelWriter(
    buffer,
    engine="openpyxl"
) as writer:

    df_view.to_excel(
        writer,
        index=False,
        sheet_name="ATG_Report"
    )


buffer.seek(0)


st.download_button(

    label="⬇️ Download Report",

    data=buffer,

    file_name="ATG_Report.xlsx",

    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)
