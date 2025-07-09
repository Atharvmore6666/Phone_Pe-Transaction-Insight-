import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide", page_title="📊 Enhanced PhonePe Dashboard")
st.title("📱 PhonePe Transaction Insights - Interactive Dashboard")

# Load CSVs
df1 = pd.read_csv("aggregated_transaction.csv")
df2 = pd.read_csv("aggregated_user.csv")
df3 = pd.read_csv("aggregated_insurance.csv")
df4 = pd.read_csv("map_user.csv")
df5 = pd.read_csv("map_transaction.csv")
df6 = pd.read_csv("map_insurance.csv")
df7 = pd.read_csv("top_user.csv")
df8 = pd.read_csv("top_transaction.csv")
df9 = pd.read_csv("top_insurance.csv")

# 🔧 Sidebar Filters
st.sidebar.header("🔧 Filters")
years = sorted(df1["Year"].dropna().unique())
states = sorted(df1["State"].dropna().unique())
txn_types = df1["Transaction_type"].dropna().unique()

selected_year = st.sidebar.slider("Select Year", min_value=int(min(years)), max_value=int(max(years)), value=int(max(years)))
selected_state = st.sidebar.selectbox("Select State", ["All"] + states)
selected_txn_types = st.sidebar.multiselect("Select Transaction Types", txn_types, default=list(txn_types))

# 🧹 Apply Filters
filtered_df1 = df1[df1["Year"] == selected_year]
if selected_state != "All":
    filtered_df1 = filtered_df1[filtered_df1["State"] == selected_state]
filtered_df1 = filtered_df1[filtered_df1["Transaction_type"].isin(selected_txn_types)]

# Sidebar menu
menu = st.sidebar.radio("📌 Select Section", [
    "Overview",
    "Transaction Trends",
    "User Insights",
    "Insurance Trends",
    "Top Districts",
    "State-Level Map"
])

# Overview
if menu == "Overview":
    st.header("📊 Dataset Preview")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Filtered Aggregated Transactions")
        st.dataframe(filtered_df1.head())
    with col2:
        st.subheader("Aggregated Users")
        st.dataframe(df2[df2["Year"] == selected_year].head())
    st.success("Data loaded from CSVs successfully!")

# Transaction Trends
elif menu == "Transaction Trends":
    st.header("📈 Transaction Amount by Type")
    fig = px.bar(filtered_df1, x="Transaction_type", y="Amount", color="Transaction_type",
                 title=f"Transaction Types in {selected_year}", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# User Insights
elif menu == "User Insights":
    st.header("📱 User Behavior Insights")
    top_brands = df2[df2["Year"] == selected_year].groupby('Brand')['Count'].sum().nlargest(5).reset_index()
    fig1 = px.pie(top_brands, names='Brand', values='Count', title="Top Mobile Brands")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("User Engagement Ratio by State")
    df4['Engagement_Ratio'] = df4['AppOpens'] / df4['RegisteredUsers']
    engagement_state = df4[df4['Year'] == selected_year]
    fig2 = px.bar(engagement_state, x='State', y='Engagement_Ratio', color='Engagement_Ratio', title=f"Engagement Ratio by State - {selected_year}")
    st.plotly_chart(fig2, use_container_width=True)

# Insurance Trends
elif menu == "Insurance Trends":
    st.header("🛡️ Insurance Transaction Overview")
    filtered_df3 = df3[df3["Year"] == selected_year]
    if selected_state != "All":
        filtered_df3 = filtered_df3[filtered_df3["State"] == selected_state]
    insurance_summary = filtered_df3.groupby("State")["Amount"].sum().nlargest(10).reset_index()
    fig = px.bar(insurance_summary, x="State", y="Amount", title="Top 10 States by Insurance Amount", color="Amount", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# Top Districts
elif menu == "Top Districts":
    st.header("🏙️ Top Districts by Transaction")
    metric = st.radio("Metric", ["Amount", "Count"])
    filtered_df8 = df8[df8["Year"] == selected_year]
    if selected_state != "All":
        filtered_df8 = filtered_df8[filtered_df8["State"] == selected_state]
    district_summary = filtered_df8.groupby("District")[metric].sum().nlargest(10).reset_index()
    fig = px.bar(district_summary, x="District", y=metric, color=metric, title=f"Top 10 Districts by {metric} in {selected_state if selected_state != 'All' else 'All States'}")
    st.plotly_chart(fig, use_container_width=True)

# Map Visualization
elif menu == "State-Level Map":
    st.header("🗺️ State-Level Transaction Heatmap")
    map_data = filtered_df1.groupby("State")["Amount"].sum().reset_index()
    state_coords = pd.read_csv("https://raw.githubusercontent.com/ronit-kumar-india/indian-states-geojson/main/indian_states_centroid.csv")
    merged = pd.merge(map_data, state_coords, on="State", how="left")
    fig = px.scatter_mapbox(merged, lat="Latitude", lon="Longitude", hover_name="State", size="Amount",
                            size_max=60, zoom=3, mapbox_style="carto-positron",
                            color="Amount", color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📍 Created by Atharva More | Data: PhonePe Pulse | Power BI Style Filters")



