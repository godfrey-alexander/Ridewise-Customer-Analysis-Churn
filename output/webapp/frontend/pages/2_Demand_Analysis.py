# Demand Dashboard.py

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
st.caption("Tracking hourly and daily ride demand to monitor trends and operational patterns over time.")
st.subheader("📊 Key Metrics")

# -----------------------------
# 1. Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")
# Year filter
years = sorted(df['pickup_year'].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Select Year", 
    options=years, 
    default=years[0])

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
col1, col2, col3, col4  = st.columns(4)

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
st.subheader("⏰ Demand Analysis")

# Trips by Hour
hourly = filtered_df.groupby('pickup_hour')['trip_id'].count().reset_index()
fig_hour = px.bar(
    hourly, 
    x='pickup_hour', 
    y='trip_id', 
    labels={'trip_id':'Trips'}, 
    title="Hourly Trips within the Day (24-hour format)", 
    color_discrete_sequence=['#6c757d'])

st.plotly_chart(fig_hour, use_container_width=True)


st.markdown("---")

# Trips by Month
daily_totals = filtered_df.groupby(filtered_df['pickup_time'].dt.date)['trip_id'].count().reset_index()
daily_totals.columns = ['Date', 'Total_Trips']
daily_totals['Month_Label'] = pd.to_datetime(daily_totals['Date']).dt.strftime('%b %Y')

fig_month = px.line(
    daily_totals, 
    x='Date', 
    y='Total_Trips', 
    title='Daily Demand over the Month', 
    markers=True, 
    labels={'Total_Trips':'Trips'},
    color_discrete_sequence=['#6c757d'])

st.plotly_chart(fig_month, use_container_width=True)































# # -----------------------------
# # 4. Revenue Analysis
# # -----------------------------
# st.subheader("💰 Revenue Analysis")

# # Revenue by City
# city_rev = filtered_df.groupby('city')['total_fare_with_tip'].sum().reset_index()
# fig_city = px.bar(city_rev, x='city', y='total_fare_with_tip', labels={'total_fare_with_tip':'Revenue'}, title="Revenue by City")
# st.plotly_chart(fig_city, use_container_width=True)

# # Revenue by Loyalty Tier
# loyalty_rev = filtered_df.groupby('loyalty_status')['total_fare_with_tip'].mean().reset_index()
# fig_loyalty = px.bar(loyalty_rev, x='loyalty_status', y='total_fare_with_tip', labels={'total_fare_with_tip':'Avg Fare'}, title="Avg Fare by Loyalty Tier")
# st.plotly_chart(fig_loyalty, use_container_width=True)

# st.markdown("---")

# # -----------------------------
# # 5. Surge & Pricing Analysis
# # -----------------------------
# st.subheader("🚀 Surge & Pricing Analysis")

# # Surge vs Revenue
# # surge_rev = filtered_df.groupby('surge_multiplier')['total_fare_with_tip'].mean().reset_index()
# # fig_surge = px.scatter(surge_rev, x='surge_multiplier', y='total_fare_with_tip', trendline="ols", labels={'total_fare_with_tip':'Avg Fare'}, title="Surge Multiplier vs Avg Fare")
# # st.plotly_chart(fig_surge, use_container_width=True)

# # # Surge vs Demand
# # surge_demand = filtered_df.groupby('surge_multiplier')['trip_id'].count().reset_index()
# # fig_surge_demand = px.line(surge_demand, x='surge_multiplier', y='trip_id', labels={'trip_id':'Trips'}, title="Surge Multiplier vs Trips")
# # st.plotly_chart(fig_surge_demand, use_container_width=True)

# # st.markdown("---")

# # -----------------------------
# # 6. Trip Economics
# # -----------------------------
# st.subheader("📈 Trip Economics")

# # Distance vs Fare
# fig_dist = px.scatter(filtered_df, x='trip_distance_km', y='total_fare_with_tip', trendline="ols", labels={'total_fare_with_tip':'Fare'}, title="Trip Distance vs Fare")
# st.plotly_chart(fig_dist, use_container_width=True)

# # Duration vs Fare
# fig_dur = px.scatter(filtered_df, x='trip_duration_min', y='total_fare_with_tip', trendline="ols", labels={'total_fare_with_tip':'Fare'}, title="Trip Duration vs Fare")
# st.plotly_chart(fig_dur, use_container_width=True)

# st.markdown("---")

# # -----------------------------
# # 7. Churn & Customer Analysis
# # -----------------------------
# st.subheader("👥 Customer & Churn Analysis")

# # Churn by Loyalty Tier
# churn_loyalty = filtered_df.groupby('loyalty_status')['churn_prob'].mean().reset_index()
# fig_churn = px.bar(churn_loyalty, x='loyalty_status', y='churn_prob', labels={'churn_prob':'Avg Churn Prob'}, title="Churn Probability by Loyalty Tier")
# st.plotly_chart(fig_churn, use_container_width=True)

# # Age vs Revenue
# fig_age = px.scatter(filtered_df, x='age', y='total_fare_with_tip', trendline="ols", labels={'total_fare_with_tip':'Fare'}, title="Age vs Fare")
# st.plotly_chart(fig_age, use_container_width=True)

# st.markdown("---")

# # -----------------------------
# # 8. Weather Impact
# # -----------------------------
# st.subheader("🌧️ Weather Impact")

# # Weather Demand Index
# weather_idx = filtered_df.groupby('weather')['weather_demand_index'].mean().reset_index()
# fig_weather = px.bar(weather_idx, x='weather', y='weather_demand_index', labels={'weather_demand_index':'Demand Index'}, title="Weather Demand Index")
# st.plotly_chart(fig_weather, use_container_width=True)

# # Bad Weather Surge
# weather_surge = filtered_df.groupby('bad_weather_flag')['surge_multiplier'].mean().reset_index()
# fig_weather_surge = px.bar(weather_surge, x='bad_weather_flag', y='surge_multiplier', labels={'surge_multiplier':'Avg Surge'}, title="Surge Multiplier in Bad Weather")
# st.plotly_chart(fig_weather_surge, use_container_width=True)

# st.markdown("---")

# # -----------------------------
# # 9. Payment & Tipping
# # -----------------------------
# st.subheader("💳 Payment & Tipping")

# # Payment Method
# pay = filtered_df['payment_type'].value_counts(normalize=True).reset_index()
# pay.columns = ['payment_type','share']
# fig_pay = px.pie(pay, names='payment_type', values='share', title="Payment Method Distribution")
# st.plotly_chart(fig_pay, use_container_width=True)

# # Tip Percentage
# fig_tip = px.histogram(filtered_df, x='tip_percentage', nbins=30, title="Tip Percentage Distribution")
# st.plotly_chart(fig_tip, use_container_width=True)

# st.markdown("---")
# st.info("📌 Use the filters in the sidebar to dynamically update all charts and KPIs!")