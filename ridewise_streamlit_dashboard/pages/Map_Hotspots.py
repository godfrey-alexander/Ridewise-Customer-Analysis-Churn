import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("🗺️ Pickup & Dropoff Hotspots Map")

@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\godfr\Documents\Amdari\Project 4\Work\data\new_data\data_EDA.csv")  

df = load_data()

# Sample for performance
df = df.sample(20000)

# Pickup Hotspots
pickup_layer = pdk.Layer(
    "HexagonLayer",
    data=df,
    get_position='[pickup_lng, pickup_lat]',
    radius=200,
)

# Dropoff Hotspots
dropoff_layer = pdk.Layer(
    "HexagonLayer",
    data=df,
    get_position='[dropoff_lng, dropoff_lat]',
    radius=200,
)

view_state = pdk.ViewState(
    latitude=df.pickup_lat.mean(),
    longitude=df.pickup_lng.mean(),
    zoom=10,
)

st.subheader("Pickup Hotspots")
st.pydeck_chart(pdk.Deck(layers=[pickup_layer], initial_view_state=view_state))

st.subheader("Dropoff Hotspots")
st.pydeck_chart(pdk.Deck(layers=[dropoff_layer], initial_view_state=view_state))