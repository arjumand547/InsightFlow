#UI_customization

import streamlit as st

def apply_theme(color):
    if color == "light":
        st.markdown("""
            <style>
            .stApp{
            background :linear-gradient(135deg,#EDF2EF,#FFFFFF);
            color:#000000;
            }
            [data-testid="stSidebar"]{
            background-color:#C0D6DF;
            color:#000000;
            }
             [data-testid="stHeader"]{
             display : none;
            }
            </style>""", unsafe_allow_html=True)
    elif color == "dark":
        st.markdown("""
        <style>
        .stApp{
        background : linear-gradient(135deg,#000000,#2D1E2F);
        color:#FFFFFF;
        }
        [data-testid="stSidebar"]{
        background-color:#4F6D7A;
        }
        [data-testid="stSidebar"] * {
        color:#FFFFFF !important;
        }
        [data-testid="stHeader"]{
        display : none;
        }
        </style>""",unsafe_allow_html=True)


def coloring_widgets():
    st.markdown("""
    <style>
    [data-testid="stFileUploader"] button {
    background-color:#E71D36;
    color:#FFFFFF;
    border : 1px solid #E71D36;
    border-radius : 5px;
    padding: 5px;
    }
    .stButton > button {
    background-color:#E71D36;
    color:#FFFFFF;
    border : 1px solid #E71D36;
    border-radius : 5px;
    padding: 5px;
    }
    .stDownloadButton > button {
        background-color: #EA2B1F;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-size: 20px;
        font-weight: bold;
    }

    </style>""",unsafe_allow_html=True)


def kpi_card(color, icon, title, value):

    if color == "light":
        background = "#C0D6DF"
        text = "#000000"
        border = "1px solid #000000"
    else:
        background = "#4F6D7A"
        text = "#FFFFFF"
        border = "1px solid #FFFFFF"

    st.markdown(f"""
<div style="
    background-color: {background};
    color: {text};
    border: {border};
    border-radius: 10px;
    padding: 20px;
    height: 200px;
    text-align: center;
">

<div style="font-size: 35px;">
    {icon}
</div>

<div style="font-size: 18px; font-weight: bold;">
    {title}
</div>

<div style="font-size: 28px; font-weight: 700;">
    {value}
</div>

</div>
""", unsafe_allow_html=True)



def customize_expanders(color):

    if color == "light":

        header = "#C0D6DF"
        body = "#F5F5F5"
        text = "#000000"
        border = "#D0D0D0"

    else:

        header = "#4F6D7A"
        body = "#17121A"
        text = "#FFFFFF"
        border = "#3A3540"


    st.markdown(f"""
    <style>

    [data-testid="stExpander"] summary {{
        background-color: {header} !important;

        color: {text} !important;

        border: 1px solid {border} !important;

        border-radius: 10px !important;

        font-weight: 600 !important;

        font-size: 18px !important;
    }}

    [data-testid="stExpander"] summary p {{
        color: {text} !important;
    }}

    [data-testid="stExpander"] summary svg {{
        color: {text} !important;
    }}

    [data-testid="stExpander"] > details > div {{
        background-color: {body} !important;

        border-radius: 0 0 10px 10px !important;
    }}

    </style>
    """, unsafe_allow_html=True)