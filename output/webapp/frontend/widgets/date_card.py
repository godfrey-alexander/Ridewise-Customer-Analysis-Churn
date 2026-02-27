import streamlit as st

def date_card(value_min, value_max):

    # Card HTML
    html = f"""
    <div style="
        background-color: #3b3b3b;
        padding: 18px;
        margin-bottom: 50px;
        border-radius: 12px;
        border: 1px solid #1c2331;
        height: 100px;
        width: 500px;
        text-align: center;
    ">
        <div style="
            font-size: 20px;
            color: white;
            margin-bottom: 6px;
        ">
            Date Range
            <div style="
                font-size: 30px;
                font-weight: 600;
                color: white;
            ">
                {value_max} - {value_min} 
            </div>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
