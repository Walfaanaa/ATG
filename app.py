import streamlit as st
import pandas as pd

EXCEL_URL = "https://raw.githubusercontent.com/Walfaanaa/ATG/main/ATG.xlsx"

df = pd.read_excel(EXCEL_URL, engine="openpyxl")

st.title("Sirna To`annaa Buusii Ji`aa fi Dabalataa Afoosha Tokkummaa Gaalessaa")
st.dataframe(df)
