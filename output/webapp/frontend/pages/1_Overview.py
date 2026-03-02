import streamlit as st
import pandas as pd
import plotly.express as px
from style import inject_sidebar_style
from style import inject_background_style
from data_loader import load_data
from widgets.metric_card import metric_card

COLORS = ['#cccccc', '#3b3b3b', '#6c757d', '#9ca3af', '#d1d5db']

df = load_data()

st.set_page_config(page_title="Rideshare Executive Dashboard", layout="wide")

inject_sidebar_style()
inject_background_style()

# Sidebar Filters (Global)
# Sidebar
#     st.image("https://img.icons8.com/fluency/96/car.png", width=64)
#     st.markdown("## RideWise Churn")
#     st.markdown("Predict rider churn risk using RFMS and engagement features.")
#     st.divider()
with st.sidebar:
    st.markdown("### Global Filters")

city_options = ["All"] + list(df.city.unique())
city_choice = st.sidebar.selectbox("City", options=city_options, index=0)
cities = list(df.city.unique()) if city_choice == "All" else [city_choice]

loyalty_options = ["All"] + list(df.loyalty_status.unique())
loyalty_choice = st.sidebar.selectbox("Loyalty Tier", options=loyalty_options, index=0)
loyalty = list(df.loyalty_status.unique()) if loyalty_choice == "All" else [loyalty_choice]

df = df[df.city.isin(cities) & df.loyalty_status.isin(loyalty)]

# KPI Metrics
st.title("🚗 Rideshare Executive Summary")
st.caption("A data-driven view of trip activity, city distribution, and customer dynamics.")
st.subheader("📊 Key Metrics")



total_users = df.user_id.nunique()
total_trips = df.trip_id.nunique()
revenue = df.total_fare_with_tip.sum()

col1, col2, col3 = st.columns(3)

with col1:
    metric_card("👥 Total Users", 10000)

with col2:
    metric_card("🚕 Total Trips", total_trips)

with col3:
    metric_card("💰 Revenue", revenue)


def kpi_color(value, threshold):
    return "normal" if value < threshold else "inverse"



st.markdown("---")



# Customer Segmentation
customer = df.groupby('loyalty_status')['user_id'].count().reset_index()
customer.columns = ['loyalty_status', 'count']
customer['percentage'] = customer['count'] / customer['count'].sum()

fig_customers = px.pie(customer, values='percentage', names='loyalty_status', color='loyalty_status', color_discrete_sequence=COLORS) # title="Distribution of Customer Segmentation")

left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("👥 Customer Segmentation")
    with st.container():
        st.plotly_chart(fig_customers, use_container_width=True, )
        fig_customers.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        # fig_customers.update_layout(margin=dict(l=20, r=20, t=20, b=20))  # Adjust pixels to your liking)

with right_col:
    st.subheader("✈️ City Distribution")
    with st.container():
        city_seg = df.groupby('city')['user_id'].count().reset_index()
        city_seg.columns = ['city', 'count']
        
        fig_bar = px.bar(city_seg, x='count', y='city', orientation='h', color="city", color_discrete_sequence=COLORS) # title="Revenue by City"
        
        fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20),height=450)
        
        st.plotly_chart(fig_bar, use_container_width=True)