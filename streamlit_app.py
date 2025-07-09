import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="📊 PhonePe Dashboard")
st.title("📱 PhonePe Transaction Insights")

# ✅ Load all pre-saved CSVs (from GitHub repo)
df1 = pd.read_csv("aggregated_transaction.csv")
df2 = pd.read_csv("aggregated_user.csv")
df3 = pd.read_csv("aggregated_insurance.csv")
df4 = pd.read_csv("map_user.csv")
df5 = pd.read_csv("map_transaction.csv")
df6 = pd.read_csv("map_insurance.csv")
df7 = pd.read_csv("top_user.csv")
df8 = pd.read_csv("top_transaction.csv")
df9 = pd.read_csv("top_insurance.csv")

# 🔘 Sidebar Menu
menu = st.sidebar.radio("📌 Select Section", [
    "Overview",
    "Transaction Trends",
    "User Insights",
    "Insurance Trends",
    "Top Districts"
])

# 📊 Overview Section
if menu == "Overview":
    st.header("📊 Dataset Preview")
    with st.expander("Aggregated Transactions"):
        st.dataframe(df1.head())
    with st.expander("Aggregated Users"):
        st.dataframe(df2.head())
    with st.expander("Aggregated Insurance"):
        st.dataframe(df3.head())
    st.success("CSV data loaded successfully from GitHub!")

# 📈 Transaction Trends
elif menu == "Transaction Trends":
    st.header("📈 Transaction Type Trends Over Years")
    grouped = df1.groupby(['Year', 'Transaction_type'])['Amount'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=grouped, x='Year', y='Amount', hue='Transaction_type', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 📱 User Insights
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

# 🛡️ Insurance Trends
elif menu == "Insurance Trends":
    st.header("🛡️ Insurance Amount by State")
    insurance_df = df3.groupby('State')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=insurance_df, x='State', y='Amount', palette='magma', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# 🏙️ Top Districts by Transaction
elif menu == "Top Districts":
    st.header("🏙️ Top 10 Districts by Transaction Amount")
    top_districts = df8.groupby('District')['Amount'].sum().sort_values(ascending=False).head(10).reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_districts, x='District', y='Amount', palette='plasma', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("📍 Built by Atharva More | Data from PhonePe Pulse GitHub")


