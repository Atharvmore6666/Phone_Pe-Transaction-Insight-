import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests

st.set_page_config(page_title="📊 PhonePe Pulse Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: #8338ec;'>📱 PhonePe Pulse Visualization</h1>", unsafe_allow_html=True)

# Logo or banner image
st.image("Pulseimg.jpg", use_column_width=True)  # Place logo/banner image in app folder or upload

# Load Data
df_tr = pd.read_csv("aggregated_transaction.csv")
df_us = pd.read_csv("aggregated_user.csv")
df_ins = pd.read_csv("aggregated_insurance.csv")
df_map_tr = pd.read_csv("map_transaction.csv")
df_map_us = pd.read_csv("map_user.csv")
df_map_ins = pd.read_csv("map_insurance.csv")
df_top_tr = pd.read_csv("top_transaction.csv")
df_top_us = pd.read_csv("top_user.csv")
df_top_ins = pd.read_csv("top_insurance.csv")

# Load GeoJSON
with open("india_states.geojson.txt", "r") as f:
    geojson = json.load(f)

# State mapping
state_name_map = {
    "andaman & nicobar islands": "Andaman & Nicobar",
    "andhra pradesh": "Andhra Pradesh",
    "arunachal pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chandigarh": "Chandigarh",
    "chhattisgarh": "Chhattisgarh",
    "dadra & nagar haveli and daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
    "delhi": "Delhi",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal pradesh": "Himachal Pradesh",
    "jammu & kashmir": "Jammu & Kashmir",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "ladakh": "Ladakh",
    "lakshadweep": "Lakshadweep",
    "madhya pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "puducherry": "Puducherry",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand",
    "west bengal": "West Bengal"
}

# Sidebar
st.sidebar.header("🔎 Filters")
page = st.sidebar.radio("Navigate", ["Aggregated", "Map", "Top Leaders", "Users", "Insurance"])
year = st.sidebar.selectbox("Select Year", sorted(df_tr['Year'].unique()))
quarter = st.sidebar.selectbox("Select Quarter", ["All"] + sorted(df_tr['Quarter'].unique()))
state = st.sidebar.selectbox("Select State", ["All"] + sorted(df_tr['State'].unique()))
txn_type = st.sidebar.selectbox("Select Transaction Type", ["All"] + sorted(df_tr['Transaction_type'].unique()))

# Filter logic
def filter_df(df):
    df = df[df['Year'] == year]
    if quarter != "All":
        df = df[df['Quarter'] == quarter]
    if state != "All":
        df = df[df['State'] == state]
    return df

# Aggregated Tab
if page == "Aggregated":
    st.subheader("📊 Aggregated Insights")
    df_f = filter_df(df_tr)
    if txn_type != "All":
        df_f = df_f[df_f['Transaction_type'] == txn_type]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", f"{df_f['Count'].sum():,.0f}")
    col2.metric("Total Amount (₹)", f"₹{df_f['Amount'].sum()/1e7:.2f} Cr")
    col3.metric("Transaction Types", f"{df_f['Transaction_type'].nunique()}")

    st.plotly_chart(px.bar(df_f, x="Transaction_type", y="Amount", color="Transaction_type",
                           title="Transaction Amount by Type"), use_container_width=True)

    df_user = filter_df(df_us)
    if not df_user.empty:
        st.plotly_chart(px.pie(df_user, names='Brand', values='Count', title="User Brand Share"), use_container_width=True)

# Map Tab
elif page == "Map":
    st.subheader("🗺️ State-Wise Transaction Heatmap")

    df_map = filter_df(df_map_tr)
    if not df_map.empty:
        state_summary = df_map.groupby("State")[["Count", "Amount"]].sum().reset_index()
        state_summary.columns = ["State", "Total_Transactions", "Total_Amount"]
        state_summary["State"] = state_summary["State"].str.lower().map(state_name_map)
        state_summary = state_summary.dropna(subset=["State"])

        fig = px.choropleth(
            state_summary,
            geojson=geojson,
            featureidkey="properties.ST_NM",
            locations="State",
            color="Total_Transactions",
            color_continuous_scale="plasma",
            title="📍 State-wise Total Transactions",
            hover_name="State",
            labels={"Total_Transactions": "Total Transactions"}
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            margin={"r":0,"t":30,"l":0,"b":0},
            geo=dict(bgcolor="rgba(0,0,0,0)"),
            paper_bgcolor="#0e1117",
            font_color="#f0f0f0"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No map data available for selected filters.")

# Top Districts Tab
elif page == "Top Leaders":
    st.subheader("🥇 Top Performing Districts")
    df_top = filter_df(df_top_tr)
    if not df_top.empty:
        top_districts = df_top.groupby("District")["Amount"].sum().nlargest(10).reset_index()
        st.plotly_chart(px.bar(top_districts, x="District", y="Amount", color="Amount",
                               title="Top 10 Districts by Transaction Amount"), use_container_width=True)
    else:
        st.warning("No data available.")

# Users Tab
elif page == "Users":
    st.subheader("📱 User Insights")
    df_user = filter_df(df_us)
    if not df_user.empty:
        total_users = df_user['Count'].sum()
        top_brand = df_user.groupby('Brand')['Count'].sum().idxmax()
        st.metric("Total Users", f"{total_users:,.0f}")
        st.metric("Most Used Brand", top_brand)

        st.plotly_chart(px.bar(df_user, x="Brand", y="Count", color="Brand", title="User Brand Distribution"), use_container_width=True)

        df_map_user = filter_df(df_map_us)
        if not df_map_user.empty:
            st.plotly_chart(px.scatter_mapbox(df_map_user, lat="Latitude", lon="Longitude", size="Count", color="Count",
                                              mapbox_style="open-street-map", zoom=3, hover_name="District",
                                              title="District-wise App Opens"), use_container_width=True)
    else:
        st.warning("No user data available for selected filters.")

# Insurance Tab
elif page == "Insurance":
    st.subheader("🛡️ Insurance Trends")
    df_ins_f = filter_df(df_ins)
    if not df_ins_f.empty:
        total_ins = df_ins_f['Amount'].sum()
        st.metric("Total Premium Collected", f"₹{total_ins/1e7:.2f} Cr")

        fig_line = px.line(df_ins_f.groupby('Quarter')["Amount"].sum().reset_index(),
                           x="Quarter", y="Amount", markers=True, title="Insurance Premium by Quarter")
        st.plotly_chart(fig_line, use_container_width=True)

        df_map_ins_f = filter_df(df_map_ins)
        if not df_map_ins_f.empty:
            st.plotly_chart(px.scatter_mapbox(df_map_ins_f, lat="Latitude", lon="Longitude", size="Amount", color="Amount",
                                              mapbox_style="carto-positron", zoom=3, hover_name="District",
                                              title="District-wise Insurance Collection"), use_container_width=True)
    else:
        st.warning("No insurance data available.")

st.markdown("---")
st.caption("📍 Dashboard by Atharva | Data: PhonePe Pulse")
