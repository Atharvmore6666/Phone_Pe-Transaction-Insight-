# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="PhonePe Dashboard", layout="wide")
st.title("📱 PhonePe Pulse Dashboard")

# 📥 Load data
df_tr = pd.read_csv("aggregated_transaction.csv")
df_us = pd.read_csv("aggregated_user.csv")
df_ins = pd.read_csv("aggregated_insurance.csv")
df_map_tr = pd.read_csv("map_transaction.csv")
df_map_us = pd.read_csv("map_user.csv")
df_map_ins = pd.read_csv("map_insurance.csv")
df_top_tr = pd.read_csv("top_transaction.csv")
df_top_us = pd.read_csv("top_user.csv")
df_top_ins = pd.read_csv("top_insurance.csv")

# 🛠 Sidebar - navigation and filters
st.sidebar.header("Navigation")
page = st.sidebar.radio("", ["Transactions", "Users", "Insurance"])

st.sidebar.header("Filters")
year_opt = sorted(df_tr["Year"].unique())
quarter_opt = sorted(df_tr["Quarter"].unique())
state_opt = sorted(df_tr["State"].unique())
txn_opt = sorted(df_tr["Transaction_type"].unique())

year = st.sidebar.selectbox("Year", year_opt, index=len(year_opt)-1)
quarter = st.sidebar.selectbox("Quarter", ["All"] + quarter_opt)
state = st.sidebar.selectbox("State", ["All"] + state_opt)
txn_type = st.sidebar.selectbox("Transaction Type", ["All"] + txn_opt)

# 🔄 Filter function
def apply_filters(df, cols):
    df_f = df[df["Year"] == year]
    if "Quarter" in cols and quarter != "All":
        df_f = df_f[df_f["Quarter"] == quarter]
    if "State" in cols and state != "All":
        df_f = df_f[df_f["State"] == state]
    if "Transaction_type" in cols and txn_type != "All":
        df_f = df_f[df_f["Transaction_type"] == txn_type]
    return df_f

# 📊 Transactions Page
if page == "Transactions":
    st.header("💰 Transaction Trends")
    df = apply_filters(df_tr, ["Year","Quarter","State","Transaction_type"])
    if df.empty:
        st.warning("No data for the selected filters.")
    else:
        fig = px.bar(df, x="Quarter", y="Amount", color="Transaction_type", barmode="group",
                     title="Transaction Amount by Quarter")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📍 Top States by Volume")
    grouped = df.groupby("State")["Amount"].sum().reset_index().nlargest(10, "Amount")
    st.plotly_chart(px.bar(grouped, x="State", y="Amount", title="Top 10 States"))

    st.subheader("🏙️ District Transaction Map")
    map_df = apply_filters(df_map_tr, ["Year","Quarter","State"])
    if not map_df.empty:
        fig = px.scatter_mapbox(map_df, lat="Latitude", lon="Longitude", size="Amount", hover_name="District",
                                color="Amount", zoom=4, height=400, mapbox_style="carto-positron")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No district data available.")

# 👤 Users Page
elif page == "Users":
    st.header("📱 User Insights")
    df = apply_filters(df_us, ["Year","Quarter","State"])
    if df.empty:
        st.warning("No data for the selected filters.")
    else:
        fig = px.pie(df.groupby("Brand")["Count"].sum().reset_index(), names="Brand", values="Count",
                     title="Brand-wise User Distribution")
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Heatmap of App Opens")
        heat = df_map_us if state=="All" else df_map_us[df_map_us["State"]==state]
        st.plotly_chart(px.choropleth(heat.groupby("State")["Count"].sum().reset_index(),
                                     locations="State", locationmode="country names", color="Count",
                                     title="App Opens by State"), use_container_width=True)

# 🛡 Insurance Page
elif page == "Insurance":
    st.header("🛡️ Insurance Trends")
    df = apply_filters(df_ins, ["Year","Quarter","State"])
    if df.empty:
        st.warning("No data for the selected filters.")
    else:
        fig = px.line(df.groupby("Quarter")["Amount"].sum().reset_index(), x="Quarter", y="Amount",
                      title="Insurance Amount by Quarter")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top Districts")
        topd = apply_filters(df_top_ins, ["Year","Quarter","State"])
        st.table(topd.nlargest(10, "Amount")[["District","Amount"]])




