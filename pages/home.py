import streamlit as st

from config.settings import APP_NAME

from components.navbar import show_navbar
from components.hero import show_hero
from components.cards import analysis_card
from components.buttons import primary_button
from components.footer import show_footer


def show_home(app):

    # Navbar

    show_navbar()

    # Hero

    show_hero(
        "Experiment Analytics, Without the Guesswork.",
        "Analyze experiments, measure impact, and make statistically informed decisions."
    )

    # Project name (previously collected nowhere — app["project_name"] stayed
    # "" for the entire session no matter what, despite being displayed on
    # the configuration and dashboard pages)

    app["project_name"] = st.text_input(
        "Project name",
        value=app.get("project_name", ""),
        placeholder="e.g. Homepage CTA Experiment",
        key="home_project_name",
    )

    st.divider()

    # Analysis methods

    st.subheader("Choose your analysis method")

    col1, col2, col3 = st.columns(3)

    with col1:

        analysis_card(
            "📝",
            "Manual Analysis",
            "Enter experiment data manually."
        )

        if primary_button(
            "Select Manual Analysis",
            key="select_manual"
        ):

            app["mode"] = "manual"
            app["page"] = "configure"

            st.rerun()

    with col2:

        analysis_card(
            "📊",
            "Historical Comparison",
            "Compare two historical GA4 periods."
        )

        if primary_button(
            "Select Historical",
            key="select_historical"
        ):

            app["mode"] = "historical"
            app["page"] = "configure"

            st.rerun()

    with col3:

        analysis_card(
            "🧪",
            "True A/B Experiment",
            "Analyze an actual experiment using GA4."
        )

        if primary_button(
            "Select True A/B",
            key="select_experiment"
        ):

            app["mode"] = "experiment"
            app["page"] = "configure"

            st.rerun()

    # Platform overview

    st.divider()

    st.subheader("What ABlytics measures")

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Core Metrics",
            "8"
        )

    with m2:

        st.metric(
            "Statistical Methods",
            "5+"
        )

    with m3:

        st.metric(
            "Data Sources",
            "2"
        )

    with m4:

        st.metric(
            "Report Types",
            "3"
        )

    # Footer

    show_footer()