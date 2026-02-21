"""
RideWise Churn Prediction - Professional Streamlit Frontend
ML-powered customer churn risk assessment for ride-sharing analytics.
"""
import os
import base64
from pathlib import Path
import streamlit as st
import requests
import pandas as pd
from typing import Optional

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="RideWise Churn Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load background from assets (background.png or backfround.png)
_assets_dir = Path(__file__).resolve().parent / "assets"
_bg_path = _assets_dir / "background.png"
if not _bg_path.exists():
    _bg_path = _assets_dir / "backfround.png"

_bg_css = ".main { background: linear-gradient(135deg, #0E1117 0%, #1A1D24 50%, #0d1117 100%); }"
if _bg_path.exists():
    try:
        _bg_b64 = base64.b64encode(_bg_path.read_bytes()).decode("utf-8")
        _bg_css = f"""
        .stApp, [data-testid="stAppViewContainer"] {{
            background-image: linear-gradient(135deg, rgba(14, 17, 23, 0.91) 0%, rgba(26, 29, 36, 0.9) 50%, rgba(13, 17, 23, 0.91) 100%),
                              url("data:image/png;base64,{_bg_b64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        """
    except Exception:
        pass

# Custom CSS for futuristic styling
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Outfit:wght@300;400;600;700&display=swap');
    
    {_bg_css}
    
    h1, h2, h3 {{
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #00D9FF, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .stMetric {{
        background: linear-gradient(145deg, rgba(0, 217, 255, 0.08), rgba(124, 58, 237, 0.08));
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(0, 217, 255, 0.2);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
    }}
    
    .risk-low {{ color: #22c55e; }}
    .risk-medium {{ color: #eab308; }}
    .risk-high {{ color: #f97316; }}
    .risk-critical {{ color: #ef4444; }}
    
    div[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1A1D24 0%, #0E1117 100%);
        border-right: 1px solid rgba(0, 217, 255, 0.15);
    }}
    
    .stButton > button {{
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600;
        background: linear-gradient(90deg, #00D9FF, #7C3AED) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 1.5rem !important;
        border-radius: 8px !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 217, 255, 0.4) !important;
    }}
</style>
""", unsafe_allow_html=True)


def check_api_health() -> tuple[bool, str]:
    """Verify backend is reachable."""
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        r.raise_for_status()
        data = r.json()
        if not data.get("model_loaded", False):
            return False, "Model not loaded on backend. Train the model first."
        return True, "Connected"
    except requests.exceptions.ConnectionError:
        return False, "Cannot reach API. Start backend: uvicorn backend.main:app"
    except Exception as e:
        return False, str(e)


def predict(features: dict) -> Optional[dict]:
    """Call predict endpoint."""
    try:
        r = requests.post(f"{API_URL}/predict", json=features, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def risk_class(p: float) -> str:
    if p < 0.25: return "risk-low"
    if p < 0.5: return "risk-medium"
    if p < 0.75: return "risk-high"
    return "risk-critical"


# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/car.png", width=64)
    st.markdown("## RideWise Churn")
    st.markdown("Predict rider churn risk using RFMS and engagement features.")
    st.divider()
    ok, msg = check_api_health()
    if ok:
        st.success("✓ API ready")
    else:
        st.error(f"⚠ {msg}")
    st.divider()
    st.caption("Built from 05_Model_Building notebook • FastAPI + Streamlit")

# Main layout
st.title("🚗 RideWise Customer Churn Prediction")
st.markdown("Enter rider engagement and RFMS metrics to estimate churn risk.")

tab1, tab2, tab3 = st.tabs(["📊 Single Predict", "📁 Batch Predict", "ℹ️ About"])

with tab1:
    st.subheader("Rider Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Trip & Spend")
        total_trips = st.number_input("Total Trips", min_value=0, value=20, step=1)
        total_spent = st.number_input("Total Spent ($)", min_value=0.0, value=350.0, step=10.0)
        avg_fare = st.number_input("Avg Fare ($)", min_value=0.0, value=14.0, step=0.5)
        total_tip = st.number_input("Total Tip ($)", min_value=0.0, value=3.0, step=0.5)
        avg_tip = st.number_input("Avg Tip ($)", min_value=0.0, value=0.12, step=0.02)
        avg_surge = st.number_input("Avg Surge", min_value=1.0, value=1.1, step=0.05)
        weekend_trip_ratio = st.slider("Weekend Trip Ratio", 0.0, 1.0, 0.25)
        peak_hour_trip_ratio = st.slider("Peak Hour Trip Ratio", 0.0, 1.0, 0.3)

    with col2:
        st.markdown("#### App Engagement")
        total_sessions = st.number_input("Total Sessions", min_value=0.0, value=15.0, step=1.0)
        total_time_on_app = st.number_input("Total Time on App (min)", min_value=0.0, value=450.0, step=50.0)
        avg_time_on_app = total_time_on_app / total_sessions if total_sessions > 0 else 0.0
        st.caption(f"Avg time/session: {avg_time_on_app:.1f} min")
        total_pages_visited = st.number_input("Total Pages Visited", min_value=0.0, value=45.0, step=5.0)
        avg_pages_visited = total_pages_visited / total_sessions if total_sessions > 0 else 0.0
        st.caption(f"Avg pages/session: {avg_pages_visited:.1f}")
        conversion_rate = st.slider("Conversion Rate", 0.0, 1.0, 0.5)
        RFMS_weighted_score = st.number_input("RFMS Weighted Score", min_value=0.0, value=2.5, step=0.2)
        age = st.number_input("Age", min_value=18, max_value=100, value=35)

    with col3:
        st.markdown("#### Demographics & Segment")
        RFMS_segment = st.selectbox(
            "RFMS Segment",
            ["At Risk", "Core Loyal Riders", "High-Value Surge-Tolerant", "Occasional Riders"],
        )
        city = st.selectbox("City", ["Nairobi", "Lagos", "Cairo"])
        loyalty_status = st.selectbox("Loyalty Status", ["Bronze", "Silver", "Gold", "Platinum"])

    if st.button("🔮 Predict Churn Risk"):
        payload = {
            "total_trips": total_trips,
            "total_spent": total_spent,
            "avg_fare": avg_fare,
            "total_tip": total_tip,
            "avg_tip": avg_tip,
            "avg_surge": avg_surge,
            "weekend_trip_ratio": weekend_trip_ratio,
            "peak_hour_trip_ratio": peak_hour_trip_ratio,
            "total_sessions": total_sessions,
            "total_time_on_app": total_time_on_app,
            "avg_time_on_app": avg_time_on_app,
            "total_pages_visited": total_pages_visited,
            "avg_pages_visited": avg_pages_visited,
            "conversion_rate": conversion_rate,
            "RFMS_weighted_score": RFMS_weighted_score,
            "RFMS_segment": RFMS_segment,
            "city": city,
            "loyalty_status": loyalty_status,
            "age": float(age),
        }
        res = predict(payload)
        if res:
            p = res["churn_probability"]
            risk = res["risk_level"]
            rc = risk_class(p)
            st.success("Prediction complete")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Churn Probability", f"{p:.2%}")
            with m2:
                st.metric("Risk Level", risk)
            with m3:
                st.metric("Label", "Churn" if res["churn_label"] == 1 else "Retained")
            st.progress(min(p, 1.0))
            st.caption(f"Threshold: {res['threshold']:.2%}")

with tab2:
    st.subheader("Batch Upload")
    st.markdown("Upload a CSV with columns matching the single-predict inputs. See About for schema.")
    uploaded = st.file_uploader("CSV file", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head(10), use_container_width=True)
        if st.button("Predict batch"):
            required = [
                "total_trips", "total_spent", "avg_fare", "total_tip", "avg_tip", "avg_surge",
                "weekend_trip_ratio", "peak_hour_trip_ratio", "total_sessions", "total_time_on_app",
                "avg_time_on_app", "total_pages_visited", "avg_pages_visited", "conversion_rate",
                "RFMS_weighted_score", "RFMS_segment", "city", "loyalty_status", "age",
            ]
            missing = [c for c in required if c not in df.columns]
            if missing:
                st.error(f"Missing columns: {missing}")
            else:
                try:
                    r = requests.post(f"{API_URL}/predict/batch", json=df.to_dict(orient="records"), timeout=30)
                    r.raise_for_status()
                    out = r.json()
                    preds = pd.DataFrame(out["predictions"])
                    st.success(f"Processed {out['count']} rows")
                    st.dataframe(preds, use_container_width=True)
                    st.download_button("Download results", preds.to_csv(index=False), "predictions.csv", "text/csv")
                except Exception as e:
                    st.error(str(e))

with tab3:
    st.subheader("About")
    st.markdown("""
    This app predicts **rider churn** using the model trained in `05_Model_Building.ipynb`.
    
    **Features used (19):**
    - Trip & spend: total_trips, total_spent, avg_fare, total_tip, avg_tip, avg_surge
    - Ratios: weekend_trip_ratio, peak_hour_trip_ratio
    - Engagement: total_sessions, total_time_on_app, avg_time_on_app
    - App usage: total_pages_visited, avg_pages_visited, conversion_rate
    - RFMS: RFMS_weighted_score, RFMS_segment
    - Demographics: city, loyalty_status, age
    
    **API:** `POST /predict` with JSON body of these features.
    """)
    st.caption("RideWise Churn Predictor v1.0 • FastAPI + Streamlit")
