import streamlit as st
from style import inject_sidebar_style

try:
    from style import inject_background_style
except ImportError:
    inject_background_style = lambda: None

st.set_page_config(
    page_title="RideWise Dashboard",
    layout="wide"
)

inject_sidebar_style()
inject_background_style()

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/car.png", width=64)
    st.markdown("## RideWise Ltd")
    st.divider()
   

pages = [
    st.Page("pages/0_Dashboard.py", title="Home"),
    st.Page("pages/1_Overview.py", title="Overview"),
    st.Page("pages/2_Demand_Revenue.py", title="Demand & Revenue"),
    st.Page("pages/4_Exposure_Analysis.py", title="Exposure Analysis"),
    st.Page("pages/5_Churn_Predictor.py", title="Churn Predictor"),
]

pg = st.navigation(pages, position="top")
pg.run()
