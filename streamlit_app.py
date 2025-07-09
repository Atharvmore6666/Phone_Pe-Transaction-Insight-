import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 PhonePe Pulse Dashboard", layout="wide")
st.title("📱 PhonePe Pulse Visualization")

# Load CSVs
df_tr = pd.read_csv("aggregated_transaction.csv")
df_us = pd.read_csv("aggregated_user.csv")
df_ins = pd.read_csv("aggregated_insurance.csv")
df_map_tr = pd.read_csv("map_transaction.csv")
df_map_us = pd.read_csv("map_user.csv")
df_map_ins = pd.read_csv("map_insurance.csv")
df_top_tr = pd.read_csv("top_transaction.csv")
df_top_us = pd.read_csv("top_user.csv")
df_top_ins = pd.read_csv("top_insurance.csv")

# Sidebar filters
st.sidebar.header("🔎 Filters")
page = st.sidebar.radio("Navigate", ["Aggregated", "Map", "Top Leaders", "Users", "Insurance"])
year = st.sidebar.selectbox("Select Year", sorted(df_tr['Year'].unique()))
quarter = st.sidebar.selectbox("Select Quarter", ["All"] + sorted(df_tr['Quarter'].unique()))
state = st.sidebar.selectbox("Select State", ["All"] + sorted(df_tr['State'].unique()))
txn_type = st.sidebar.selectbox("Select Transaction Type", ["All"] + sorted(df_tr['Transaction_type'].unique()))

# Function to filter DataFrame
def filter_df(df):
    df = df[df['Year'] == year]
    if quarter != "All":
        df = df[df['Quarter'] == quarter]
    if state != "All":
        df = df[df['State'] == state]
    return df

# Aggregated Page
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

# Map Page
elif page == "Map":
    st.subheader("🗺️ Map-Based Visualizations")
    df_map = filter_df(df_map_tr)
    if not df_map.empty:
        if 'Latitude' in df_map.columns and 'Longitude' in df_map.columns:
            st.plotly_chart(px.scatter_mapbox(df_map, lat="Latitude", lon="Longitude", size="Amount", color="Amount",
                                              mapbox_style="carto-positron", zoom=3, hover_name="District",
                                              title="District-wise Transaction Amount"), use_container_width=True)
        else:
            st.warning("Map data must include Latitude and Longitude columns.")
    else:
        st.warning("No data available for selected filters.")

# Top Leaders Page
elif page == "Top Leaders":
    st.subheader("🥇 Top Performing Districts")
    df_top = filter_df(df_top_tr)
    if not df_top.empty:
        top_districts = df_top.groupby("District")['Amount'].sum().nlargest(10).reset_index()
        st.plotly_chart(px.bar(top_districts, x="District", y="Amount", color="Amount",
                               title="Top 10 Districts by Transaction Amount"), use_container_width=True)
    else:
        st.warning("No top district data available for selected filters.")

# Users Page
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
        if not df_map_user.empty and 'Latitude' in df_map_user.columns and 'Longitude' in df_map_user.columns:
            st.plotly_chart(px.scatter_mapbox(df_map_user, lat="Latitude", lon="Longitude", size="Count", color="Count",
                                              mapbox_style="open-street-map", zoom=3, hover_name="District",
                                              title="District-wise App Opens"), use_container_width=True)
    else:
        st.warning("No user data available for selected filters.")

# Insurance Page
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
        if not df_map_ins_f.empty and 'Latitude' in df_map_ins_f.columns and 'Longitude' in df_map_ins_f.columns:
            st.plotly_chart(px.scatter_mapbox(df_map_ins_f, lat="Latitude", lon="Longitude", size="Amount", color="Amount",
                                              mapbox_style="carto-positron", zoom=3, hover_name="District",
                                              title="District-wise Insurance Collection"), use_container_width=True)
    else:
        st.warning("No insurance data available for selected filters.")

st.markdown("---")
st.caption("📍 Dashboard inspired by Kaleeswari | Customized by Atharva | Data: PhonePe Pulse")

