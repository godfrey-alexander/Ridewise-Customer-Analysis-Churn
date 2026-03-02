import streamlit as st
import pandas as pd
import plotly.express as px
from style import inject_sidebar_style
try:
    from style import inject_background_style
except ImportError:
    inject_background_style = lambda: None
from data_loader import load_data_segments
from widgets.metric_card import metric_card
from widgets.date_card import date_card

inject_sidebar_style()
inject_background_style()

st.title("🚗 Rideshare Interactive Dashboard")
st.caption(" Maximum potential revenue lost if customers inactive for the selected number of days are not re-engaged.")

st.html("""
    <style>
        .st-key-custom_margin {
            margin-top: 40px;
            height: 400px;
        }
    </style>
""")

rfm = load_data_segments()

# Sidebar Filters (Global)
st.sidebar.title("Inactivity Threshold")
inactivity_threshold  = st.sidebar.slider(
    "Days since last activity", 
    min_value=7, 
    max_value=90, 
    value=7, 
    step=7
)

at_risk_customers  = rfm[rfm['recency'] <= inactivity_threshold]

exposure_by_segment  = (
    at_risk_customers
    .groupby('segments', as_index=False)['monetary']
    .sum()
    .rename(columns={'segments': 'Segments', 'monetary': 'Revenue Exposure'})
)

if not exposure_by_segment.empty:
    exposure_by_segment["Proportion"] = (
        exposure_by_segment["Revenue Exposure"]
        / exposure_by_segment["Revenue Exposure"].sum()
)

st.subheader("📊 Key Metrics")

total_revenue_exposed = at_risk_customers["monetary"].sum()
total_customers_exposed = at_risk_customers["user_id"].nunique()

top_row_left_col, top_row_right_col = st.columns([1.2, 1])

with top_row_left_col:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            metric_card("Revenue at Risk", f"£{total_revenue_exposed:,.0f}")
        with col2:
            metric_card("Customers Exposed", f"{total_customers_exposed:,.0f}")

with top_row_right_col:
    customers_min_date = at_risk_customers['last_trip_time'].min()
    customers_max_date = at_risk_customers['last_trip_time'].max()

    date_card(customers_min_date, customers_max_date)


st.markdown("---")


left_col, right_col = st.columns([1.2, 1])

with left_col:
    with st.container():
        fig = px.treemap(
            exposure_by_segment,
            path=["Segments"],
            values="Revenue Exposure",
            custom_data=["Proportion"],
            color="Revenue Exposure",
            color_continuous_scale="Greys",
            title="Proportion of Revenue Lost by Customer Segments",
        )

        fig.update_layout(
            width=1000, 
            height=700, 
            title_font_size=22, 
            font=dict(size=16),
            margin=dict(r=20)
        )  # affects labels, hover, etc. margin=dict(t=60, l=10, r=10, b=10)

        fig.update_traces(
            textfont_size=25,
            texttemplate="<b>%{label}<br><b>%{customdata[0]:.1%}",
            hovertemplate=
                "<b>%{label}</b><br>" +
                "Amount: $%{value}<br>" +
                "<extra></extra>"
        )

        fig.update_coloraxes(showscale=False)

        st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.subheader("👥 Customers Driving Exposure")
    st.dataframe(at_risk_customers.drop(columns=['last_trip_time']), height=525)