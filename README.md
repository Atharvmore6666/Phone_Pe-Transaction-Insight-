# 📱 PhonePe Transaction Insights Dashboard

![PhonePe Logo](./ICN.png)

## 🚀 Project Overview

This project delivers a data-driven analysis of **PhonePe Pulse** transaction data across India using **Python**, **SQL**, and **Streamlit**. It provides insights into transaction trends, user behavior, insurance growth, and engagement intensity at the **state**, **district**, and **device** levels.

A fully interactive **Streamlit dashboard** allows users to explore the data visually and draw meaningful insights.

---

## 📊 Key Features

- 📈 **Aggregated Insights**: View total transactions, amount, and transaction types over selected timeframes and locations.
- 🗺️ **State-wise Maps**: Visualize transaction density across Indian states and districts.
- 🥇 **Top Performers**: Identify top 10 districts by transaction amount.
- 📱 **Device Analytics**: See which smartphone brands dominate usage.
- 🛡️ **Insurance Insights**: Analyze insurance premium collection across India.
- 🔄 **Streamlit Dashboard**: Real-time data filtering and visualizations using Plotly.

---

## 🧠 Business Use Cases

- 🎯 Customer Segmentation
- 🔍 Fraud Detection
- 🌍 Geographical Targeting
- 💳 Payment Method Analysis
- 📈 Insurance Product Strategy
- 📲 User Retention Strategy
- 🧪 Product Development Insights

---

## 🛠️ Tools & Technologies

- **Python**, **Pandas**, **Matplotlib**, **Seaborn**
- **SQLAlchemy** for in-memory querying
- **Streamlit** for dashboard UI
- **Plotly Express** for interactive charts
- **GeoJSON** for mapping
- Data Source: [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse)

---

## 📂 Folder Structure

```
📁 root/
│
├── 📄 streamlit_app.py            # Streamlit Dashboard App
├── 📄 phone_pe.py                 # Data Extraction + SQL Analysis (Colab)
├── 📄 PhonePe_Insights_Report.pdf # Final Report
├── 📄 Phone Pe.docx               # Business Documentation
├── 📁 data/                       # Cleaned CSV files (generated from PhonePe Pulse)
├── 📁 assets/                     # Project images (e.g., ICN.png)
```

---

## 📌 How to Run the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Atharvmore6666/Phone_Pe-Transaction-Insight-.git
   cd Phone_Pe-Transaction-Insight-
   ```

2. **Ensure your data folder contains CSVs**
   > These are created by running `phone_pe.py` after cloning the PhonePe Pulse repo.

3. **Run the Streamlit App**
   ```bash
   streamlit run streamlit_app.py
   ```

4. The dashboard will launch in your browser.

---

## 📈 Insights Summary

1. **Peer-to-peer payments** dominate usage and show consistent growth.
2. **Merchant transactions** are rising rapidly — promising expansion potential.
3. **Xiaomi** and **Samsung** top device usage and engagement charts.
4. **Karnataka** and **Maharashtra** lead in insurance transaction volumes.
5. **Tier-2 cities** like **Patna** and **Jaipur** are emerging as strong digital payment zones.
6. **Northeast states** show high engagement per user.

---

## 🧾 Project Deliverables

- 📁 Cleaned datasets
- 📊 SQL queries and analysis
- 🌐 Streamlit web dashboard
- 📄 Final report with insights and recommendations

---

## 👨‍💻 Author

**Atharva More**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin)](https://www.linkedin.com/in/atharva-more-50717b140)  
📫 Email: atharvamore1304@gmail.com

---

> _Thanks for visiting! Feel free to ⭐ the repo if you found it useful._


