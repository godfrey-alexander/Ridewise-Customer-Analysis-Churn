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
    except requests.exceptions.HTTPError as e:
        detail = e.response.text
        try:
            detail = e.response.json().get("detail", detail)
        except Exception:
            pass
        st.error(f"API error ({e.response.status_code}): {detail}")
        return None
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
    st.caption("Built from 02_Data Processing & Classification Model Development • FastAPI + Streamlit")

# Main layout
st.title("🚗 RideWise Customer Churn Prediction")
st.markdown("Enter rider engagement and RFMS metrics to estimate churn risk.")

tab1, tab2, tab3 = st.tabs(["📊 Single Predict", "📁 Batch Predict", "ℹ️ About"])

# Raw feature options matching 03_SHAP preprocessor
LOYALTY_OPTIONS = ["Bronze", "Silver", "Gold", "Platinum"]
RFMS_OPTIONS = ["At Risk", "Occasional Riders", "Core Loyal Riders", "High-Value Surge-Tolerant"]
CITY_OPTIONS = ["Cairo", "Lagos", "Nairobi"]

with tab1:
    st.subheader("Rider Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Usage & Spend")
        recency = st.number_input("Recency", min_value=0.0, value=30.0, step=1.0, help="Days since last trip")
        total_trips = st.number_input("Total Trips", min_value=0, value=20, step=1)
        avg_spend = st.number_input("Avg Spend ($)", min_value=0.0, value=15.0, step=0.5)
        total_tip = st.number_input("Total Tip ($)", min_value=0.0, value=3.0, step=0.5)
        avg_tip = st.number_input("Avg Tip ($)", min_value=0.0, value=0.15, step=0.02)
        avg_rating_given = st.slider("Avg Rating Given", 0.0, 5.0, 4.0, 0.1)

    with col2:
        st.markdown("#### Trip & Segment")
        loyalty_status = st.selectbox("Loyalty Status", LOYALTY_OPTIONS)
        avg_distance = st.number_input("Avg Distance", min_value=0.0, value=5.0, step=0.5)
        avg_duration = st.number_input("Avg Duration (min)", min_value=0.0, value=18.0, step=1.0)
        RFMS_segment = st.selectbox("RFMS Segment", RFMS_OPTIONS)

    with col3:
        st.markdown("#### City")
        city = st.selectbox("City", CITY_OPTIONS)

    if st.button("🔮 Predict Churn Risk"):
        payload = {
            "recency": float(recency),
            "total_trips": float(total_trips),
            "avg_spend": float(avg_spend),
            "total_tip": float(total_tip),
            "avg_tip": float(avg_tip),
            "avg_rating_given": float(avg_rating_given),
            "loyalty_status": loyalty_status,
            "city": city,
            "avg_distance": float(avg_distance),
            "avg_duration": float(avg_duration),
            "RFMS_segment": RFMS_segment,
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
                "recency", "total_trips", "avg_spend", "total_tip", "avg_tip", "avg_rating_given",
                "loyalty_status", "city", "avg_distance", "avg_duration", "RFMS_segment",
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
    This app predicts **rider churn** using the **preprocessor + model pipeline** from `03_SHAP Explainability`.
    
    **Raw features (11):** recency, total_trips, avg_spend, total_tip, avg_tip, avg_rating_given,
    loyalty_status, city, avg_distance, avg_duration, RFMS_segment.
    
    The backend applies the same preprocessing as the notebook (RobustScaler, OrdinalEncoder for
    loyalty/RFMS, OneHotEncoder for city) then runs the trained model.
    
    **API:** `POST /predict` with JSON body of these 11 raw features.
    """)
    st.caption("RideWise Churn Predictor v1.0 • FastAPI + Streamlit")
