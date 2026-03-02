import base64
from pathlib import Path

import streamlit as st

_FRONTEND_DIR = Path(__file__).resolve().parent
_BG_PATH = _FRONTEND_DIR / "assets" / "background.png"


def inject_background_style():
    """Use frontend/assets/background.png as full-app background for all pages."""
    bg_css = ".main { background: linear-gradient(135deg, #0E1117 0%, #1A1D24 50%, #0d1117 100%); }"
    if _BG_PATH.exists():
        try:
            bg_b64 = base64.b64encode(_BG_PATH.read_bytes()).decode("utf-8")
            bg_css = (
                ".stApp, [data-testid=\"stAppViewContainer\"] {"
                " background-image: linear-gradient(135deg, rgba(14, 17, 23, 0.91) 0%, rgba(26, 29, 36, 0.9) 50%, rgba(13, 17, 23, 0.91) 100%),"
                " url(\"data:image/png;base64," + bg_b64 + "\");"
                " background-size: cover; background-position: center; background-attachment: fixed; }"
            )
        except Exception:
            pass
    st.markdown("<style>" + bg_css + "</style>", unsafe_allow_html=True)


def inject_sidebar_style():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] a {
                font-size: 22px !important;
                padding: 14px 18px !important;
                margin-bottom: 10px !important;
                line-height: 1.6;
            }
            div[data-testid="stCaption"] {
                color: #ffffff !important;
                font-size: 14px;
            }
            div[data-testid="stDataFrame"] {
                margin-top: 40px;
                border-radius: 10px;
            }
            /* Minimal gap between top nav bar and page title */
            .stAppHeader {
                margin-bottom: 0 !important;
                padding-bottom: 0 !important;
            }
            .main .block-container,
            .reportview-container .main .block-container {
                padding-top: 0.25rem !important;
            }
            /* Less space before title (override block-container padding) */
            .st-emotion-cache-c38l67 {
                padding: 0.5rem 4rem 1rem !important;
            }
            /* Reduce space between metric cards and dividers */
            .main hr {
                margin-top: 0.5rem !important;
                margin-bottom: 0.5rem !important;
            }
            /* Less space under the metrics row */
            [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {
                margin-bottom: 0.25rem !important;
            }
            /* Viewport fit: scale to device */
            html, body, .stApp, [data-testid="stAppViewContainer"] {
                width: 100% !important;
                max-width: 100vw !important;
                overflow-x: hidden !important;
            }
            .main, .main .block-container {
                max-width: 100% !important;
                padding-left: clamp(0.5rem, 3vw, 2rem) !important;
                padding-right: clamp(0.5rem, 3vw, 2rem) !important;
            }
            .st-emotion-cache-c38l67 {
                padding-left: clamp(0.5rem, 4vw, 4rem) !important;
                padding-right: clamp(0.5rem, 4vw, 4rem) !important;
            }
            /* Charts and iframes scale within viewport */
            .main [data-testid="stPlotlyChart"], .main .stPlotlyChart, .main iframe {
                max-width: 100% !important;
            }
            @media (max-width: 768px) {
                [data-testid="stSidebarNav"] a { font-size: 16px !important; padding: 10px 12px !important; }
                .st-emotion-cache-c38l67 { padding: 0.5rem 1rem 1rem !important; }
            }
            /* Churn Predictor page: metrics, buttons */
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Outfit:wght@300;400;600;700&display=swap');
            .stMetric {
                background: linear-gradient(145deg, rgba(0, 217, 255, 0.08), rgba(124, 58, 237, 0.08));
                padding: 1rem 1.5rem;
                border-radius: 12px;
                border: 1px solid rgba(0, 217, 255, 0.2);
                box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
            }
            .risk-low { color: #22c55e; }
            .risk-medium { color: #eab308; }
            .risk-high { color: #f97316; }
            .risk-critical { color: #ef4444; }
            div[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1A1D24 0%, #0E1117 100%);
                border-right: 1px solid rgba(0, 217, 255, 0.15);
            }
            .stButton > button {
                font-family: 'JetBrains Mono', monospace !important;
                font-weight: 600;
                background: linear-gradient(90deg, #00D9FF, #7C3AED) !important;
                color: white !important;
                border: none !important;
                padding: 0.6rem 1.5rem !important;
                border-radius: 8px !important;
                transition: transform 0.2s, box-shadow 0.2s !important;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 20px rgba(0, 217, 255, 0.4) !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
