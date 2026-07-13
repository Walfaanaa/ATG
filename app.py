import streamlit as st
import pandas as pd

EXCEL_URL = "https://github.com/Walfaanaa/ATG/tree/main/ATG.xlsx"

df = pd.read_excel(EXCEL_URL)

st.title("EGSA Monthly Payment System")

st.dataframe(df)
