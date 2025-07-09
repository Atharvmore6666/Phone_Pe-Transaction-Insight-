"""
PhonePe Data Visualization and Exploration Dashboard

This Streamlit application provides comprehensive data visualization and analysis
for PhonePe transaction data including insurance, transactions, and user analytics.

Author: Atharva More
Date: 2024
"""

import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image
import os
from config import DB_CONFIG
from utils import (
    Transaction_amount_count_Y,
    Transaction_amount_count_Y_Q,
    Aggre_Tran_Transaction_type,
    Aggre_user_plot_1,
    Aggre_user_plot_2,
    Aggre_user_plot_3,
    Map_insur_District,
    map_user_plot_1,
    map_user_plot_2,
    map_user_plot_3,
    Top_insurance_plot_1,
    top_user_plot_1,
    top_user_plot_2,
    top_chart_transaction_amount,
    top_chart_transaction_count,
    top_chart_registered_user,
    top_chart_appopens,
    top_chart_registered_users
)

# Page Configuration
st.set_page_config(
    page_title="PhonePe Data Visualization",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #5f27cd;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #341f97;
        margin: 1rem 0;
    }
    .feature-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DataLoader:
    """Class to handle database connections and data loading"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect_to_database()
    
    def connect_to_database(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            st.success("Database connected successfully!")
        except Exception as e:
            st.error(f"Database connection failed: {str(e)}")
    
    def load_data(self, table_name, columns):
        """Load data from specified table"""
        try:
            query = f"SELECT * FROM {table_name}"
            self.cursor.execute(query)
            self.connection.commit()
            data = self.cursor.fetchall()
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            st.error(f"Error loading data from {table_name}: {str(e)}")
            return pd.DataFrame()
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

@st.cache_data
def load_all_data():
    """Load all required datasets"""
    loader = DataLoader()
    
    # Define table schemas
    tables_config = {
        'aggregated_insurance': ["States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"],
        'aggregated_transaction': ["States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"],
        'aggregated_user': ["States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"],
        'map_insurance': ["States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"],
        'map_transaction': ["States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"],
        'map_user': ["States", "Years", "Quarter", "District", "RegisteredUser", "AppOpens"],
        'top_insurance': ["States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"],
        'top_transaction': ["States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"],
        'top_user': ["States", "Years", "Quarter", "Pincodes", "RegisteredUsers"]
    }
    
    # Load all datasets
    datasets = {}
    for table_name, columns in tables_config.items():
        datasets[table_name] = loader.load_data(table_name, columns)
    
    loader.close_connection()
    return datasets

def render_home_page():
    """Render the home page"""
    st.markdown('<h1 class="main-title">📱 PHONEPE DATA VISUALIZATION AND EXPLORATION</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h2 class="section-header">PHONEPE</h2>', unsafe_allow_html=True)
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("""
        PhonePe is an Indian digital payments and financial technology company that has revolutionized 
        the way people make transactions in India.
        """)
        
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.write("**🌟 KEY FEATURES:**")
        st.write("• **Credit & Debit card linking**")
        st.write("• **Bank Balance check**")
        st.write("• **Money Storage**")
        st.write("• **PIN Authorization**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <a href="https://www.phonepe.com/app-download/" target="_blank">
            <button style="background-color: #5f27cd; color: white; padding: 10px 20px; 
                           border: none; border-radius: 5px; cursor: pointer;">
                📱 DOWNLOAD THE APP NOW
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        # Use a placeholder image or load from assets
        try:
            st.image("assets/phonepe_logo.jpg", width=600)
        except:
            st.info("Add PhonePe logo image to assets/phonepe_logo.jpg")
    
    # Additional features section
    col3, col4 = st.columns(2)
    
    with col3:
        try:
            st.image("assets/phonepe_features.jpg", width=600)
        except:
            st.info("Add features image to assets/phonepe_features.jpg")
    
    with col4:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.write("**💳 Easy Transactions**")
        st.write("**📱 One App For All Your Payments**")
        st.write("**🏦 Your Bank Account Is All You Need**")
        st.write("**💰 Multiple Payment Modes**")
        st.write("**🏪 PhonePe Merchants**")
        st.write("**🔄 Multiple Ways To Pay**")
        st.write("**📊 1. Direct Transfer & More**")
        st.write("**📷 2. QR Code**")
        st.write("**🎁 Earn Great Rewards**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Bottom section
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.write("**💡 Key Advantages:**")
        st.write("• **No Wallet Top-Up Required**")
        st.write("• **Pay Directly From Any Bank To Any Bank A/C**")
        st.write("• **Instantly & Free**")
        st.write("• **Secure & Reliable**")
        st.write("• **24/7 Customer Support**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        try:
            st.image("assets/phonepe_benefits.jpg", width=600)
        except:
            st.info("Add benefits image to assets/phonepe_benefits.jpg")

def render_data_exploration(datasets):
    """Render the data exploration page"""
    st.markdown('<h2 class="section-header">📊 DATA EXPLORATION</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Aggregated Analysis", "🗺️ Map Analysis", "🏆 Top Analysis"])
    
    with tab1:
        render_aggregated_analysis(datasets)
    
    with tab2:
        render_map_analysis(datasets)
    
    with tab3:
        render_top_analysis(datasets)

def render_aggregated_analysis(datasets):
    """Render aggregated analysis section"""
    method = st.radio("Select The Method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])
    
    if method == "Insurance Analysis":
        df = datasets['aggregated_insurance']
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", int(df["Years"].min()), int(df["Years"].max()), int(df["Years"].min()))
            
            tac_Y = Transaction_amount_count_Y(df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", int(tac_Y["Quarter"].min()), int(tac_Y["Quarter"].max()), int(tac_Y["Quarter"].min()))
            
            Transaction_amount_count_Y_Q(tac_Y, quarters)
    
    elif method == "Transaction Analysis":
        df = datasets['aggregated_transaction']
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", int(df["Years"].min()), int(df["Years"].max()), int(df["Years"].min()))
            
            Aggre_tran_tac_Y = Transaction_amount_count_Y(df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())
            
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", int(Aggre_tran_tac_Y["Quarter"].min()), int(Aggre_tran_tac_Y["Quarter"].max()), int(Aggre_tran_tac_Y["Quarter"].min()))
            
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["States"].unique())
            
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)
    
    elif method == "User Analysis":
        df = datasets['aggregated_user']
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", int(df["Years"].min()), int(df["Years"].max()), int(df["Years"].min()))
            
            Aggre_user_Y = Aggre_user_plot_1(df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter", int(Aggre_user_Y["Quarter"].min()), int(Aggre_user_Y["Quarter"].max()), int(Aggre_user_Y["Quarter"].min()))
            
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())
            
            Aggre_user_plot_3(Aggre_user_Y_Q, states)

def render_map_analysis(datasets):
    """Render map analysis section"""
    method_2 = st.radio("Select The Method", ["Map Insurance", "Map Transaction", "Map User"])
    
    if method_2 == "Map Insurance":
        df = datasets['map_insurance']
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_mi", int(df["Years"].min()), int(df["Years"].max()), int(df["Years"].min()))
            
            map_insur_tac_Y = Transaction_amount_count_Y(df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mi", map_insur_tac_Y["States"].unique())
            
            Map_insur_District(map_insur_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_mi", int(map_insur_tac_Y["Quarter"].min()), int(map_insur_tac_Y["Quarter"].max()), int(map_insur_tac_Y["Quarter"].min()))
            
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty", map_insur_tac_Y_Q["States"].unique())
            
            Map_insur_District(map_insur_tac_Y_Q, states)
    
    elif method_2 == "Map Transaction":
        df = datasets['map_transaction']
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year", int(df["Years"].min()), int(df["Years"].max()), int(df["Years"].min()))
            
            map_tran_tac_Y = Transaction_amount_count_Y(df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mi", map_tran_tac_Y["States"].unique())
            
            Map_insur_District(map_tran_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_mt", int(map_tran_tac_Y["Quarter"].min()), int(map_tran_tac_Y["Quarter"].max()), int(map_tran_tac_Y["Quarter"].min()))
            
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_Ty", map_tran_tac_Y_Q["States"].unique())
            
            Map_insur_District(map_tran_tac_Y_Q, states)
    
    elif method_2 == "Map User":
        df = datasets['map_user']
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_mu", int(df["Years"].min()), int(df["Years"].max()), int(df["Years"].min()))
            
            map_user_Y = map_user_plot_1(df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_mu", int(map_user_Y["Quarter"].min()), int(map_user_Y["Quarter"].max()), int(map_user_Y["Quarter"].min()))
            
            map_user_Y_Q = map_user_plot_2(map_user_Y, quarters)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_mu", map_user_Y_Q["States"].unique())
            
            map_user_plot_3(map_user_Y_Q, states)

def render_top_analysis(datasets):
    """Render top analysis section"""
    method_3 = st.radio("Select The Method", ["Top Insurance", "Top Transaction", "Top User"])
    
    if method_3 == "Top Insurance":
        df = datasets['top_insurance']
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_ti", int(df["Years"].min()), int(df["Years"].max()), int(df["Years"].min()))
            
            top_insur_tac_Y = Transaction_amount_count_Y(df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_ti", top_insur_tac_Y["States"].unique())
            
            Top_insurance_plot_1(top_insur_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_mu", int(top_insur_tac_Y["Quarter"].min()), int(top_insur_tac_Y["Quarter"].max()), int(top_insur_tac_Y["Quarter"].min()))
            
            top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)
    
    elif method_3 == "Top Transaction":
        df = datasets['top_transaction']
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_tt", int(df["Years"].min()), int(df["Years"].max()), int(df["Years"].min()))
            
            top_tran_tac_Y = Transaction_amount_count_Y(df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_tt", top_tran_tac_Y["States"].unique())
            
            Top_insurance_plot_1(top_tran_tac_Y, states)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select The Quarter_tt", int(top_tran_tac_Y["Quarter"].min()), int(top_tran_tac_Y["Quarter"].max()), int(top_tran_tac_Y["Quarter"].min()))
            
            top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)
    
    elif method_3 == "Top User":
        df = datasets['top_user']
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select The Year_tu", int(df["Years"].min()), int(df["Years"].max()), int(df["Years"].min()))
            
            top_user_Y = top_user_plot_1(df, years)
            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State_tu", top_user_Y["States"].unique())
            
            top_user_plot_2(top_user_Y, states)

def render_top_charts(datasets):
    """Render top charts page"""
    st.markdown('<h2 class="section-header">🏆 TOP CHARTS</h2>', unsafe_allow_html=True)
    
    questions = [
        "1. Transaction Amount and Count of Aggregated Insurance",
        "2. Transaction Amount and Count of Map Insurance",
        "3. Transaction Amount and Count of Top Insurance",
        "4. Transaction Amount and Count of Aggregated Transaction",
        "5. Transaction Amount and Count of Map Transaction",
        "6. Transaction Amount and Count of Top Transaction",
        "7. Transaction Count of Aggregated User",
        "8. Registered users of Map User",
        "9. App opens of Map User",
        "10. Registered users of Top User"
    ]
    
    question = st.selectbox("Select the Question", questions)
    
    # Map questions to table names
    table_mapping = {
        "1. Transaction Amount and Count of Aggregated Insurance": "aggregated_insurance",
        "2. Transaction Amount and Count of Map Insurance": "map_insurance",
        "3. Transaction Amount and Count of Top Insurance": "top_insurance",
        "4. Transaction Amount and Count of Aggregated Transaction": "aggregated_transaction",
        "5. Transaction Amount and Count of Map Transaction": "map_transaction",
        "6. Transaction Amount and Count of Top Transaction": "top_transaction",
        "7. Transaction Count of Aggregated User": "aggregated_user"
    }
    
    if question in table_mapping:
        table_name = table_mapping[question]
        if question == "7. Transaction Count of Aggregated User":
            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count(table_name)
        else:
            st.subheader("TRANSACTION AMOUNT")
            top_chart_transaction_amount(table_name)
            st.subheader("TRANSACTION COUNT")
            top_chart_transaction_count(table_name)
    
    elif question == "8. Registered users of Map User":
        df = datasets['map_user']
        if not df.empty:
            states = st.selectbox("Select the State", df["States"].unique())
            st.subheader("REGISTERED USERS")
            top_chart_registered_user("map_user", states)
    
    elif question == "9. App opens of Map User":
        df = datasets['map_user']
        if not df.empty:
            states = st.selectbox("Select the State", df["States"].unique())
            st.subheader("APPOPENS")
            top_chart_appopens("map_user", states)
    
    elif question == "10. Registered users of Top User":
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")

def main():
    """Main application function"""
    # Sidebar navigation
    with st.sidebar:
        st.image("assets/phonepe_logo.png", width=200) if os.path.exists("assets/phonepe_logo.png") else None
        
        select = option_menu(
            "Main Menu",
            ["🏠 HOME", "📊 DATA EXPLORATION", "🏆 TOP CHARTS"],
            icons=['house', 'graph-up', 'trophy'],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#5f27cd"},
            }
        )
    
    # Load data
    if select != "🏠 HOME":
        with st.spinner("Loading data..."):
            datasets = load_all_data()
    
    # Route to appropriate page
    if select == "🏠 HOME":
        render_home_page()
    elif select == "📊 DATA EXPLORATION":
        render_data_exploration(datasets)
    elif select == "🏆 TOP CHARTS":
        render_top_charts(datasets)
    
    # Footer
    st.markdown("""
    ---
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>PhonePe Data Visualization Dashboard | Built with ❤️ using Streamlit</p>
        <p>© 2024 - Data Analytics Project</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
