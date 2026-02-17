import pandas as pd
import streamlit as st

@st.cache_data(show_spinner="Loading data...")
def load_data():
    df = pd.read_csv("data/riders_trips.csv")
    df['pickup_time'] = pd.to_datetime(df['pickup_time'], utc=True)

    df['pickup_year'] = df['pickup_time'].dt.year
    df['pickup_month_num'] = df['pickup_time'].dt.month
    df['pickup_month_name'] = df['pickup_time'].dt.strftime('%b')

    return df

def load_data_segments():
    df = pd.read_csv("data/rfm_data.csv")
    df.drop(columns=['rfm_score'], inplace=True)

    return df

