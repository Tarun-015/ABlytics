import streamlit as st
from pathlib import Path

from config.settings import APP_NAME

from pages.home import show_home
from pages.configuration import show_configuration
from pages.dashboard import show_dashboard


# Page configuration

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Load CSS

css = Path("assets/style.css").read_text()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True
)


# Session state

if "app" not in st.session_state:

    st.session_state.app = {

        "page": "home",

        "project_name": "",

        "mode": None,

        "dataset": None,

        "results": None,

        "ga4": None

    }


app = st.session_state.app


# Page routing

if app["page"] == "home":

    show_home(app)


elif app["page"] == "configure":

    show_configuration(app)


elif app["page"] == "dashboard":

    show_dashboard(app)