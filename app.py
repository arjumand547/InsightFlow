import streamlit as st
from UI_customization import *



GITHUB_URL = "https://github.com/arjumand547"
STREAMLIT_URL = "https://share.streamlit.io/user/arjumand547"


st.title("📊 InsightFlow")

st.markdown(
    """
    ### Turn Your Raw Data Into Meaningful Insights

    Upload your dataset, map your columns, and explore your business
    through interactive dashboards, customer insights, product performance,
    and downloadable reports.
    """
)

st.divider()


st.subheader("👨‍💻 About the Developer")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(
        """
        ## Syed Arjumand  
        Haider Shah
        """
    )

with col2:
    st.write(
        """
        I am an aspiring Data Analyst and BS Artificial Intelligence student
        with an interest in data analysis, dashboard development, programming,
        and technology.
        """
    )

    st.write(
        "📊 Data Analyst | 🎓 BS Artificial Intelligence | 💻 Dashboard Developer"
    )


st.markdown("### 🔗 Connect With Me")

col1, col2 = st.columns(2)

with col1:
    st.link_button(
        "🐙 Visit My GitHub",
        GITHUB_URL,
        width="stretch"
    )

with col2:
    st.link_button(
        "🚀 Visit My Streamlit Profile",
        STREAMLIT_URL,
        width="stretch"
    )


st.divider()


st.subheader("🛠️ Tools & Technologies Used")

tech_col1, tech_col2, tech_col3, tech_col4, tech_col5 = st.columns(5)

with tech_col1:
    st.info("🐍 Python")

with tech_col2:
    st.info("📺 Streamlit")

with tech_col3:
    st.info("🐼 Pandas")

with tech_col4:
    st.info("🔌 SQLite")

with tech_col5:
    st.info("📊 Plotly")


st.divider()


st.subheader("🚀 How to Use InsightFlow")

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown(
        """
        ### 1️⃣ Upload

        Upload your CSV or Excel dataset through the **Upload Dataset** page.
        """
    )

with step2:
    st.markdown(
        """
        ### 2️⃣ Map Columns

        Match your dataset columns with the standard columns required by InsightFlow.
        """
    )

with step3:
    st.markdown(
        """
        ### 3️⃣ Explore

        Analyze your business using dashboards, customer insights, and product performance.
        """
    )

with step4:
    st.markdown(
        """
        ### 4️⃣ Download

        Generate and download filtered tables and summary reports as CSV files.
        """
    )


st.divider()


st.subheader("📈 Explore the Application")

with st.expander("📁 Upload Dataset"):
    st.write(
        """
        Upload your CSV or Excel dataset. You can map your own column names
        to the standard structure required by InsightFlow.
        """
    )

with st.expander("💎 Executive Dashboard"):
    st.write(
        """
        Get an overall view of your business through important KPIs and
        interactive visualizations.
        """
    )

with st.expander("🙎‍♂️ Customer Insights"):
    st.write(
        """
        Analyze customer behavior, sales contribution, purchasing patterns,
        and other customer-related insights.
        """
    )

with st.expander("📦 Product Performance"):
    st.write(
        """
        Explore product sales, profitability, categories, and identify
        your best-performing products.
        """
    )

with st.expander("📑 Reports"):
    st.write(
        """
        View detailed business tables, customer reports, product reports,
        and download them as CSV files.
        """
    )

with st.expander("🧠 Trends and Predictions"):
    st.write(
        """
        This section is currently under development. Future versions of
        InsightFlow will include machine learning and AI-powered analytics.
        """
    )


st.divider()


st.markdown(
    """
    <div style="
        text-align: center;
        padding: 20px;
        font-size: 16px;
    ">
        <b>InsightFlow</b><br>
        Data Analysis • Business Intelligence • Interactive Dashboards
        <br><br>
        Developed by <b>Syed Arjumand Haider Shah</b>
    </div>
    """,
    unsafe_allow_html=True
)