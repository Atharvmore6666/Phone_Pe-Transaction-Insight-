# streamlit_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from phone_pe import (
    parse_aggregated_transaction, parse_aggregated_user, parse_aggregated_insurance,
    parse_map_user, parse_map_transaction, parse_map_insurance,
    parse_top_user, parse_top_transaction, parse_top_insurance
)

st.set_page_config(layout="wide", page_title="📊 PhonePe Dashboard")

st.title("📱 PhonePe Transaction Insights")

# Load data
df1 = parse_aggregated_transaction()
df2 = parse_aggregated_user()
df3 = parse_aggregated_insurance()
df4 = parse_map_user()
df5 = parse_map_transaction()
df6 = parse_map_insurance()
df7 = parse_top_user()
df8 = parse_top_transaction()
df9 = parse_top_insurance()

menu = st.sidebar.radio("📌 Select Section", [
    "Overview",
    "Transaction Trends",
    "User Insights",
    "Insurance Trends",
    "Top Districts"
])

if menu == "Overview":
    st.header("📊 Data Overview")
    with st.expander("Aggregated Transactions (df1)"):
        st.dataframe(df1.head())
    with st.expander("Aggregated Users (df2)"):
        st.dataframe(df2.head())
    with st.expander("Aggregated Insurance (df3)"):
        st.dataframe(df3.head())
    st.success("Use the sidebar to explore trends and insights!")

elif menu == "Transaction Trends":
    st.header("📈 Transaction Type Trends Over Years")
    grouped = df1.groupby(['Year', 'Transaction_type'])['Amount'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=grouped, x='Year', y='Amount', hue='Transaction_type', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif menu == "User Insights":
    st.header("📱 Top Mobile Brands by Registered Users")
    brand_summary = df2.groupby('Brand')['Count'].sum().sort_values(ascending=False).head(10).reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=brand_summary, x='Brand', y='Count', palette='viridis', ax=ax)
    st.pyplot(fig)

    st.subheader("📍 User Engagement by State")
    df4["Engagement_Ratio"] = df4["AppOpens"] / df4["RegisteredUsers"]
    top_states = df4.groupby("State")["Engagement_Ratio"].mean().sort_values(ascending=False).head(10).reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_states, x="Engagement_Ratio", y="State", palette="summer", ax=ax2)
    st.pyplot(fig2)

elif menu == "Insurance Trends":
    st.header("🛡️ Insurance Amount by State")
    insurance_df = df3.groupby('State')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=insurance_df, x='State', y='Amount', palette='magma', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif menu == "Top Districts":
    st.header("🏙️ Top 10 Districts by Transaction Amount")
    top_districts = df8.groupby('District')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_districts, x='District', y='Amount', palette='plasma', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.markdown("---")
st.caption("📍 Project by Atharva More | Data from PhonePe Pulse GitHub")
