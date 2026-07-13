import streamlit as st
import pandas as pd

EXCEL_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/ATG.xlsx"

df = pd.read_excel(EXCEL_URL, engine="openpyxl")

st.title("EGSA Monthly Payment System")
st.dataframe(df)
