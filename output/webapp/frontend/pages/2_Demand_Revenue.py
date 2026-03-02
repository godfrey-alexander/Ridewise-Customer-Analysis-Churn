# Demand & Revenue – single page with tabs

import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_data
from style import inject_sidebar_style
try:
    from style import inject_background_style
except ImportError:
    inject_background_style = lambda: None
from widgets.metric_card import metric_card

inject_sidebar_style()
inject_background_style()

df = load_data()
st.set_page_config(page_title="Rideshare Analytics Dashboard", layout="wide")

st.title("🚗 Rideshare Interactive Dashboard")
st.caption("Track demand and revenue by hour and day. Use the tabs below to switch between Demand and Revenue views.")
st.subheader("📊 Key Metrics")

# -----------------------------
# Sidebar filters (shared) – "All" or single choice
# -----------------------------
st.sidebar.header("Filters")
years = sorted(df["pickup_year"].dropna().unique())
year_options = ["All"] + list(years)
year_choice = st.sidebar.selectbox("Select Year", options=year_options, index=0)
selected_years = list(years) if year_choice == "All" else [year_choice]

months = sorted(df["pickup_month_num"].unique())
month_options = ["All"] + list(months)
month_choice = st.sidebar.selectbox(
    "Select Month",
    options=month_options,
    format_func=lambda x: "All" if x == "All" else pd.to_datetime(str(x), format="%m").strftime("%b"),
    index=0,
)
selected_months = list(months) if month_choice == "All" else [month_choice]

city_options = ["All"] + list(df["city"].unique())
city_choice = st.sidebar.selectbox("Select City", options=city_options, index=0)
cities = list(df["city"].unique()) if city_choice == "All" else [city_choice]

filtered_df = df[
    (df["pickup_year"].isin(selected_years))
    & (df["pickup_month_num"].isin(selected_months))
    & (df["city"].isin(cities))
]

# -----------------------------
# Shared KPIs
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("👥 Total Users", filtered_df["user_id"].nunique())
with col2:
    metric_card("🚕 Total Trips", filtered_df["trip_id"].nunique())
with col3:
    metric_card("💰 Revenue", f"${filtered_df['total_fare_with_tip'].sum():,.0f}")
with col4:
    metric_card("Avg Fare", f"${filtered_df['total_fare_with_tip'].mean():.2f}")

st.markdown("---")

# -----------------------------
# Tabs: Demand | Revenue
# -----------------------------
tab_demand, tab_revenue = st.tabs(["⏰ Demand Analysis", "💰 Revenue Analysis"])

with tab_demand:
    st.subheader("Demand Analysis")
    hourly = filtered_df.groupby("pickup_hour")["trip_id"].count().reset_index()
    fig_hour = px.bar(
        hourly,
        x="pickup_hour",
        y="trip_id",
        labels={"trip_id": "Trips"},
        title="Hourly Trips within the Day (24-hour format)",
        color_discrete_sequence=["#6c757d"],
    )
    st.plotly_chart(fig_hour, use_container_width=True)
    st.markdown("---")
    daily_totals = (
        filtered_df.groupby(filtered_df["pickup_time"].dt.date)["trip_id"].count().reset_index()
    )
    daily_totals.columns = ["Date", "Total_Trips"]
    daily_totals["Month_Label"] = pd.to_datetime(daily_totals["Date"]).dt.strftime("%b %Y")
    fig_month = px.line(
        daily_totals,
        x="Date",
        y="Total_Trips",
        title="Daily Demand over the Month",
        markers=True,
        labels={"Total_Trips": "Trips"},
        color_discrete_sequence=["#6c757d"],
    )
    st.plotly_chart(fig_month, use_container_width=True)

with tab_revenue:
    st.subheader("Revenue Analysis")
    hourly_rev = filtered_df.groupby("pickup_hour")["total_fare"].sum().reset_index()
    fig_hour_rev = px.bar(
        hourly_rev,
        x="pickup_hour",
        y="total_fare",
        labels={"total_fare": "Revenue"},
        title="Revenue by Hour",
        color_discrete_sequence=["#6c757d"],
    )
    st.plotly_chart(fig_hour_rev, use_container_width=True)
    st.markdown("---")
    daily_rev = (
        filtered_df.groupby(filtered_df["pickup_time"].dt.date)["total_fare"].sum().reset_index()
    )
    daily_rev.columns = ["Date", "Total_Revenue"]
    daily_rev["Month_Label"] = pd.to_datetime(daily_rev["Date"]).dt.strftime("%b %Y")
    fig_month_rev = px.line(
        daily_rev,
        x="Date",
        y="Total_Revenue",
        title="Daily Revenue over the Month",
        markers=True,
        labels={"Total_Revenue": "Revenue"},
        color_discrete_sequence=["#6c757d"],
    )
    st.plotly_chart(fig_month_rev, use_container_width=True)
