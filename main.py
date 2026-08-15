import streamlit as st
from UI_customization import *
st.set_page_config(page_title="InsightFlow",
                   page_icon="logos/project_logo.png",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   )

color = st.sidebar.radio("Theme",["light","dark"])
st.session_state["color"] = color

apply_theme(color)
coloring_widgets()
customize_expanders(color)


pages = {
    "InsightFlow": [
        st.Page("app.py",title="Home",icon="🏠")
        ],
    "File Uploader":[
        st.Page("pages/upload_dataset.py",title="Upload Dataset",icon="📁")
       ],
    "Analytics":[
        st.Page("pages/executive_dashboard.py", title="Executive Dashboard", icon="💎"),
        st.Page("pages/customer_feedback.py",title="Customer Insights",icon="🙎‍♂️"),
        st.Page("pages/product_performance.py",title="Product Performance",icon="📦"),
        st.Page("pages/reports.py",title="Reports",icon="📑")
        ],
    "Ai Integration":[
        st.Page("pages/trends_and_forecast.py",title="Trends and Predictions",icon="🧠")
        ]
    }

pg = st.navigation(pages)
pg.run()

