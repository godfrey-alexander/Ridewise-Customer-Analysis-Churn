import streamlit as st
from data_loader import load_data
from style import inject_sidebar_style, inject_background_style

inject_sidebar_style()
inject_background_style()


st.title("Rideshare Executive Dashboard")

st.write("This project demonstrates end-to-end applied data science, bridging analytics, modeling, explainability, and production deployment.")
st.write("Developed by Godfrey Alexander Abban")

st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.markdown("""
Explore the RideWise Ltd. business with interactive charts and filters. See trips, revenue, demand patterns, where revenue is at risk and which customers are at risk of churning.

### Pages
- **Overview** – Total users, trips, revenue, and how customers split by loyalty tier and city
- **Demand Analysis** – When rides happen: by hour of day and by day (plan drivers and spot peaks)
- **Revenue Analysis** – When revenue comes in: by hour and by day (compare with demand)
- **Exposure Analysis** – Revenue at risk if customers go inactive; see segments and who to re-engage
- **Churn Predictor** – Predict churn risk for a rider from RFMS and engagement features
""")

st.info("Use the navigation bar above to move between pages.")

df = load_data()
