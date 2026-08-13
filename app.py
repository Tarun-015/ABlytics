import streamlit as st
from pathlib import Path

from config.settings import APP_NAME

from pages.home import show_home
from pages.configuration import show_configuration
from pages.dashboard import show_dashboard
from pages.analytics import show_analytics
from pages.documentation import show_documentation


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CSS
# =========================================================

css_path = Path("assets/style.css")

if css_path.exists():

    css = css_path.read_text(
        encoding="utf-8"
    )

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


# =========================================================
# SESSION STATE
# =========================================================

if "app" not in st.session_state:

    st.session_state.app = {
        "page": "home",
        "project_name": "",
        "mode": None,
        "dataset": None,
        "results": None,
        "ga4": None,
    }


app = st.session_state.app


# =========================================================
# ROUTING
# =========================================================

if app["page"] == "home":

    show_home(app)


elif app["page"] == "configure":

    show_configuration(app)


elif app["page"] == "dashboard":

    show_dashboard(app)


elif app["page"] == "analytics":

    show_analytics(app)


elif app["page"] == "documentation":

    show_documentation(app)


else:

    app["page"] = "home"

    st.rerun()