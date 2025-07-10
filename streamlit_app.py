import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="📊 PhonePe Pulse Dashboard", page_icon="ICN.png", layout="wide")

st.image("Pulseimg.jpg", use_container_width=True)
st.markdown("<h1 style='text-align: center; color: #8338ec;'>📱 PhonePe Pulse Visualization</h1>", unsafe_allow_html=True)

# Load data
df_tr = pd.read_csv("aggregated_transaction.csv")
df_us = pd.read_csv("aggregated_user.csv")
df_ins = pd.read_csv("aggregated_insurance.csv")
df_map_tr = pd.read_csv("map_transaction.csv")
df_map_us = pd.read_csv("map_user.csv")
df_map_ins = pd.read_csv("map_insurance.csv")
df_top_tr = pd.read_csv("top_transaction.csv")
df_top_us = pd.read_csv("top_user.csv")
df_top_ins = pd.read_csv("top_insurance.csv")

with open("india_states.geojson.txt", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Fix mismatched state names from CSV to GeoJSON using manual mapping
state_name_fix = {
    "andaman-&-nicobar-islands": "Andaman & Nicobar",
    "dadra-&-nagar-haveli-&-daman-&-diu": "Dadra and Nagar Haveli and Daman and Diu",
    "jammu-&-kashmir": "Jammu & Kashmir",
    "andhra-pradesh": "Andhra Pradesh",
    "arunachal-pradesh": "Arunachal Pradesh",
    "himachal-pradesh": "Himachal Pradesh",
    "madhya-pradesh": "Madhya Pradesh",
    "uttar-pradesh": "Uttar Pradesh",
    "tamil-nadu": "Tamil Nadu",
    "west-bengal": "West Bengal"
}

# Sidebar
st.sidebar.header("🔎 Filters")
page = st.sidebar.radio("Navigate", ["Aggregated", "Map", "Top Leaders", "Users", "Insurance"])
year = st.sidebar.selectbox("Select Year", sorted(df_tr['Year'].unique()))
quarter = st.sidebar.selectbox("Select Quarter", ["All"] + sorted(df_tr['Quarter'].unique()))
state = st.sidebar.selectbox("Select State", ["All"] + sorted(df_tr['State'].unique()))
txn_type = st.sidebar.selectbox("Select Transaction Type", ["All"] + sorted(df_tr['Transaction_type'].unique()))

def filter_df(df):
    df = df[df['Year'] == year]
    if quarter != "All":
        df = df[df['Quarter'] == quarter]
    if state != "All":
        df = df[df['State'] == state]
    return df

# Aggregated View
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

# Map View
elif page == "Map":
    st.subheader("🗺️ State-Wise Transaction Heatmap")
    df_map = filter_df(df_map_tr)
    if not df_map.empty:
        state_summary = df_map.groupby("State")[["Count", "Amount"]].sum().reset_index()
        state_summary.columns = ["State", "Total_Transactions", "Total_Amount"]

        # Apply name fixes
        state_summary["State"] = state_summary["State"].apply(lambda x: state_name_fix.get(x.lower(), x))

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
        fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},
                          geo=dict(bgcolor="rgba(0,0,0,0)"),
                          paper_bgcolor="#0e1117",
                          font_color="#f0f0f0")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No map data available for selected filters.")

# Top Leaders
elif page == "Top Leaders":
    st.subheader("🥇 Top Performing Districts")
    df_top = filter_df(df_top_tr)
    if not df_top.empty:
        top_districts = df_top.groupby("District")["Amount"].sum().nlargest(10).reset_index()
        st.plotly_chart(px.bar(top_districts, x="District", y="Amount", color="Amount",
                               title="Top 10 Districts by Transaction Amount"), use_container_width=True)
    else:
        st.warning("No data available.")

# Users View
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
        if not df_map_user.empty and {'Latitude', 'Longitude'}.issubset(df_map_user.columns):
            df_map_user = df_map_user.dropna(subset=["Latitude", "Longitude", "Count"])
            df_map_user["Latitude"] = pd.to_numeric(df_map_user["Latitude"], errors="coerce")
            df_map_user["Longitude"] = pd.to_numeric(df_map_user["Longitude"], errors="coerce")
            df_map_user = df_map_user.dropna(subset=["Latitude", "Longitude"])

            if not df_map_user.empty:
                st.plotly_chart(px.scatter_mapbox(df_map_user, lat="Latitude", lon="Longitude", size="Count", color="Count",
                                                  mapbox_style="open-street-map", zoom=3, hover_name="District",
                                                  title="District-wise App Opens"), use_container_width=True)
            else:
                st.warning("No valid map data.")
    else:
        st.warning("No user data available.")

# Insurance View
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
        if not df_map_ins_f.empty and {'Latitude', 'Longitude'}.issubset(df_map_ins_f.columns):
            df_map_ins_f = df_map_ins_f.dropna(subset=["Latitude", "Longitude", "Amount"])
            df_map_ins_f["Latitude"] = pd.to_numeric(df_map_ins_f["Latitude"], errors="coerce")
            df_map_ins_f["Longitude"] = pd.to_numeric(df_map_ins_f["Longitude"], errors="coerce")
            df_map_ins_f = df_map_ins_f.dropna(subset=["Latitude", "Longitude"])

            if not df_map_ins_f.empty:
                st.plotly_chart(px.scatter_mapbox(df_map_ins_f, lat="Latitude", lon="Longitude", size="Amount", color="Amount",
                                                  mapbox_style="carto-positron", zoom=3, hover_name="District",
                                                  title="District-wise Insurance Collection"), use_container_width=True)
            else:
                st.warning("No valid location data for insurance.")
    else:
        st.warning("No insurance data available.")

st.markdown("---")
st.caption("📍 Dashboard by Atharva | Data: PhonePe Pulse")
