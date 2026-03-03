"""
RideWise Churn Prediction - Professional Streamlit Frontend
ML-powered customer churn risk assessment for ride-sharing analytics.
"""
import os
import streamlit as st
import requests
import pandas as pd
from typing import Optional

from style import inject_sidebar_style
try:
    from style import inject_background_style
except ImportError:
    inject_background_style = lambda: None

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="RideWise Churn Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_sidebar_style()
inject_background_style()


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


@st.dialog("Churn Prediction Result", width="medium", on_dismiss="rerun")
def show_result_dialog(res: dict):
    """Display prediction result in an overlay."""
    p = res["churn_probability"]
    risk = res["risk_level"]
    st.metric("Churn Probability", f"{p:.2%}")
    st.metric("Risk Level", risk)
    st.metric("Label", "Churn" if res["churn_label"] == 1 else "Retained")
    st.progress(min(p, 1.0))
    st.caption(f"Threshold: {res['threshold']:.2%}")
    rec = res.get("recommendation", "")
    if rec:
        st.markdown("**Recommendation**")
        st.info(rec)


# Sidebar
with st.sidebar:
    ok, msg = check_api_health()
    if ok:
        st.success("✓ API ready")
    else:
        st.error(f"⚠ {msg}")
    st.divider()

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

    if "churn_result" not in st.session_state:
        st.session_state.churn_result = None

    # Form: changing any input does not trigger a rerun; only the submit button does (no fade).
    with st.form("churn_predict_form"):
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
            st.markdown("#### Trip, Segment & City")
            loyalty_status = st.selectbox("Loyalty Status", LOYALTY_OPTIONS)
            avg_distance = st.number_input("Avg Distance", min_value=0.0, value=5.0, step=0.5)
            avg_duration = st.number_input("Avg Duration (min)", min_value=0.0, value=18.0, step=1.0)
            RFMS_segment = st.selectbox("RFMS Segment", RFMS_OPTIONS)
            city = st.selectbox("City", CITY_OPTIONS)

        with col3:
            res = st.session_state.churn_result
            st.info("Click **Predict Churn Risk** to see the result.")

        submitted = st.form_submit_button("🔮 Predict Churn Risk")

    if submitted:
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
            st.session_state.churn_result = res
            show_result_dialog(res)

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
    **RideWise Churn Predictor** estimates how likely a rider is to churn (stop using the service) and suggests actions to retain them.

    **What you can do**
    - **Single Predict** — Enter one rider’s engagement and RFMS details; click **Predict Churn Risk** to see a pop-up with churn probability, risk level (Low / Medium / High), and a **recommendation** tailored to their segment and risk.
    - **Batch Predict** — Upload a CSV with the same 11 columns; get churn probabilities and risk levels for all rows and download the results.

    **Inputs (11 features)**  
    The model uses: **recency** (days since last trip), **total_trips**, **avg_spend**, **total_tip**, **avg_tip**, **avg_rating_given**, **avg_distance**, **avg_duration**, **loyalty_status** (Bronze / Silver / Gold / Platinum), **RFMS_segment** (At Risk, Occasional Riders, Core Loyal Riders, High-Value Surge-Tolerant), and **city** (Cairo, Lagos, Nairobi).

    **Outputs**  
    For each rider you get: **churn probability**, **risk level**, **churn/retained label**, and a **recommendation** (e.g. targeted discounts, win-back offers, or recognition) based on their segment and risk.

    **Backend** — A FastAPI service loads a preprocessor and trained model, runs the preprocessoring pipeline, and returns the prediction and recommendation. The sidebar shows whether the API is connected.
    """)
    st.caption("RideWise Churn Predictor v1.0 • FastAPI + Streamlit")
