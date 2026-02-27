import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 
from data_loader import load_data
from style import inject_sidebar_style
from widgets.metric_card import metric_card
inject_sidebar_style()


# -----------------------------
# 0. Load Data
# -----------------------------
df = load_data()

st.set_page_config(page_title="Rideshare Analytics Dashboard", layout="wide")

st.title("🚗 Rideshare Interactive Dashboard")
st.caption("Tracking hourly and daily revenue to monitor financial performance over time.")
st.subheader("📊 Key Metrics")

# -----------------------------
# 1. Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")
# Year filter
years = sorted(df['pickup_year'].unique())
selected_years = st.sidebar.multiselect(
    "Select Year", 
    options=years, 
    default=years[0]
    )

# Month filter
months = sorted(df['pickup_month_num'].unique())
selected_months = st.sidebar.multiselect(
    "Select Month",
    options=months,
    format_func=lambda x: pd.to_datetime(str(x), format='%m').strftime('%b'),
    default=months[4]
)

# City filter
cities = st.sidebar.multiselect(
    "Select Cities", 
    options=df['city'].unique(), 
    default=df['city'].unique()
    )

# Filter data
filtered_df = df[
    (df['pickup_year'].isin(selected_years)) &
    (df['pickup_month_num'].isin(selected_months)) &
    (df['city'].isin(cities))
] 

# -----------------------------
# 2. KPI Metrics
# -----------------------------


col1, col2, col3, col4, = st.columns(4)

with col1:
    metric_card("👥 Total Users", filtered_df['user_id'].nunique())
with col2:
    metric_card("🚕 Total Trips", filtered_df['trip_id'].nunique())
with col3:
    metric_card("💰 Revenue", f"${filtered_df['total_fare_with_tip'].sum():,.0f}")
with col4:
    metric_card("Avg Fare", f"${filtered_df['total_fare_with_tip'].mean():.2f}")

st.markdown("---")

# -----------------------------
# 3. Demand Analysis
# -----------------------------
st.subheader("💰 Revenue Analysis")

# Trips by Hour
hourly = filtered_df.groupby('pickup_hour')['total_fare'].sum().reset_index()
fig_hour = px.bar(hourly, x='pickup_hour', y='total_fare', labels={'trip_id':'Trips'}, title="Revenue by Hour", color_discrete_sequence=['#6c757d'])
st.plotly_chart(fig_hour, use_container_width=True)

st.markdown("---")

# Revenue by Month
daily_totals = filtered_df.groupby(filtered_df['pickup_time'].dt.date)['total_fare'].sum().reset_index()
daily_totals.columns = ['Date', 'Total_Revenue']
daily_totals['Month_Label'] = pd.to_datetime(daily_totals['Date']).dt.strftime('%b %Y')

fig_month = px.line(
    daily_totals, 
    x='Date', 
    y='Total_Revenue', 
    title='Daily Revenue over the Month', 
    markers=True, 
    labels={'Total_Trips':'Trips'}, 
    color_discrete_sequence=['#6c757d']
)

st.plotly_chart(fig_month, use_container_width=True)