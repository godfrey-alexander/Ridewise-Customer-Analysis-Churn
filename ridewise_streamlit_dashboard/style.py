import streamlit as st

def inject_sidebar_style():
    st.markdown(
        """
        <style>
            /* Sidebar navigation links */
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

           /* Style dataframe block container */
            div[data-testid="stDataFrame"] {
                margin-top: 40px;
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
