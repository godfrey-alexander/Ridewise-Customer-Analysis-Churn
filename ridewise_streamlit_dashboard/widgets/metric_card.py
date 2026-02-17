import streamlit as st

def metric_card(title, value, delta=None, prefix="", suffix=""):
     # Format the value safely
    if isinstance(value, (int, float)):
        formatted_value = f"{prefix}{value:,.0f}{suffix}"
    else:
        formatted_value = f"{prefix}{value}{suffix}"

    # Delta HTML
    delta_html = ""
    if delta is not None:
        color = "#2e7d32" if delta > 0 else "#c62828"
        arrow = "▲" if delta > 0 else "▼"
        delta_html = f"""
        <div style="
            font-size: 13px;
            margin-top: 6px;
            color: {color};
        ">
            {arrow} {abs(delta)}%
        </div>
        """

    # Card HTML
    html = f"""
    <div style="
        background-color: #3b3b3b;
        padding: 18px;
        margin-bottom: 50px;
        border-radius: 12px;
        border: 1px solid #1c2331;
        height: 100px;
        width: 250px;
        text-align: center;
    ">
        <div style="
            font-size: 20px;
            color: white;
            margin-bottom: 6px;
        ">
            {title}
            <div style="
                font-size: 30px;
                font-weight: 600;
                color: white;
            ">
                {formatted_value}
            </div>
        </div>
        {delta_html}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
