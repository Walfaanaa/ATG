import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AL Management System",
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
""",
unsafe_allow_html=True)



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


st.markdown(
"""
<h1>
Sirna To'annaa Buusii Waliigalaa Afoosha Ollaa
</h1>
""",
unsafe_allow_html=True
)



# ======================================================
# LOAD EXCEL
# ======================================================

EXCEL_FILE = "AO.xlsx"



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
# REQUIRED COLUMNS
# ======================================================

required_columns = [

    "business_date",
    "id_no",
    "full_name",
    "phone_no",
    "monthly_payment",
    "additional_payment",
    "total_payment",
    "loan",
    "incrued_cost"

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
    "loan",
    "incrued_cost"

]


for c in money_columns:

    df[c] = pd.to_numeric(
        df[c],
        errors="coerce"
    ).fillna(0)



# ======================================================
# SIDEBAR FILTER
# ======================================================

st.sidebar.header("⚙️ Filter")


member_list = [

    "All"

] + sorted(

    df["full_name"]
    .dropna()
    .unique()
    .tolist()

)



selected_member = st.sidebar.selectbox(
    "Select Member",
    member_list
)



if selected_member != "All":

    df_view = df[
        df["full_name"] == selected_member
    ]

else:

    df_view = df.copy()



# ======================================================
# KPI METRICS
# ======================================================

# Payments made by member with ID 1001
payment_1001 = df_view.loc[
    df_view["id_no"] == 1001,
    "monthly_payment"
].sum()

# Current account balance for member 1001
current_account_balance = payment_1001

# Total Loan after deducting payments of member 1001
total_loan = df_view["loan"].sum() 

monthly = df_view["monthly_payment"].sum() - payment_1001

additional = df_view["additional_payment"].sum()

total_payment = df_view["total_payment"].sum() - payment_1001+df_view["incrued_cost"].sum()


total_incrued_cost = df_view["incrued_cost"].sum()

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "💰 Total Loan",
        f"{total_loan:,.2f}"
    )

with col2:
    st.metric(
        "📅 Monthly Payment",
        f"{monthly:,.2f}"
    )

with col3:
    st.metric(
        "➕ Additional Payment",
        f"{additional:,.2f}"
    )

with col4:
    st.metric(
        "✅ Total Capital of AO",
        f"{total_payment:,.2f}"
    )

with col5:
    st.metric(
        "💵 Incurred Cost",
        f"{total_incrued_cost:,.2f}"
    )

with col6:
    st.metric(
        "🏦 Current Account Balance",
        f"{current_account_balance:,.2f}"
    )
    

# ======================================================
# BAR CHART
# ======================================================

st.subheader("Payment Summary")



chart_df = pd.DataFrame({

    "Type":[
        "Monthly Payment",
        "Additional Payment",
        "Total Capital of AO",
        "Total Incrued Cost Of AO",
        "Currect Balance Of AO"
    ],


    "Amount":[
        monthly,
        additional,
        total_payment,
        total_incrued_cost,
        current_account_balance
    ]

})



fig = px.bar(

    chart_df,

    x="Type",

    y="Amount",

    text="Amount",

    color="Type",

    color_discrete_map={

        "Monthly Payment":"green",

        "Additional Payment":"yellow",

        "Total Capital of AO":"violet",
        
        "Total Incrued Cost Of AO":"red",
        
        "Currect Balance Of AO":"blue"

    }

)



fig.update_traces(

    texttemplate="%{text:,.0f}",

    textposition="outside"

)



fig.update_layout(

    showlegend=False,

    xaxis_title="Payment Type",

    yaxis_title="Amount"

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
# DOWNLOAD EXCEL
# ======================================================


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
