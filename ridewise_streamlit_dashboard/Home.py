import streamlit as st
from style import inject_sidebar_style
from data_loader import load_data

inject_sidebar_style()

st.set_page_config(
    page_title="Customer Churn Dashboard",
    layout="wide"
)


st.title("Customer Churn Analysis")

st.markdown("""
This application explores customer churn using data analysis and machine learning.

### Pages
- **Data Overview** – Understand the dataset and key metrics  
- **Churn Risk Customers** – Identify high-risk segments  
- **Prediction Model** – Train and evaluate churn models  
- **Insights** – Business interpretation and recommendations
""")

st.info("Use the sidebar to navigate between pages.")

df = load_data()
