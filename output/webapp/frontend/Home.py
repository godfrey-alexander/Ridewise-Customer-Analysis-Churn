import streamlit as st
from style import inject_sidebar_style
from data_loader import load_data, load_data_segments

inject_sidebar_style()

st.set_page_config(
    page_title="RideWise Dashboard",
    layout="wide"
)


st.title("RideWise Dashboard")

st.markdown("""
Explore your rideshare business with interactive charts and filters. See trips, revenue, demand patterns, and where revenue is at risk — then use the **sidebar** to open any page below.

### Pages
- **Overview** – Total users, trips, revenue, and how customers split by loyalty tier and city
- **Demand Analysis** – When rides happen: by hour of day and by day (plan drivers and spot peaks)
- **Revenue Analysis** – When revenue comes in: by hour and by day (compare with demand)
- **Exposure Analysis** – Revenue at risk if customers go inactive; see segments and who to re-engage
""")

st.info("Use the sidebar to navigate between pages.")

df = load_data()