import pandas as pd
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

@st.cache_data(show_spinner="Loading data...")
def load_data():
    file_path = DATA_DIR / "riders_trips.csv"
    df = pd.read_csv(file_path)
    df['pickup_time'] = pd.to_datetime(df['pickup_time'], utc=True)

    df['pickup_year'] = df['pickup_time'].dt.year
    df['pickup_month_num'] = df['pickup_time'].dt.month
    df['pickup_month_name'] = df['pickup_time'].dt.strftime('%b')

    return df

def load_data_segments():
    file_path = DATA_DIR / "rfm_data.csv"
    df = pd.read_csv(file_path)
    df.drop(columns=['rfm_score'], inplace=True)

    return df

