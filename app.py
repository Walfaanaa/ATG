import streamlit as st
import pandas as pd

MONTHLY_PAYMENT = 200
PENALTY = MONTHLY_PAYMENT * 0.5

df = pd.read_excel("ATG.xlsx")

df["buusii_jiaa"] = df["buusii_jiaa"].fillna(0)

# KPIs
total_members = len(df)

paid_members = (df["buusii_jiaa"] >= MONTHLY_PAYMENT).sum()

unpaid_members = (df["buusii_jiaa"] < MONTHLY_PAYMENT).sum()

total_collected = df["buusii_jiaa"].sum()

total_penalty = unpaid_members * PENALTY

# Add penalty column
df["Penalty"] = df["buusii_jiaa"].apply(
    lambda x: PENALTY if x < MONTHLY_PAYMENT else 0
)

# Members who didn't pay
non_paid = df[df["buusii_jiaa"] < MONTHLY_PAYMENT]
