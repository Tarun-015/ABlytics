import streamlit as st

from components.navbar import show_navbar
from components.hero import show_hero
from components.cards import analysis_card, stat_card
from components.buttons import primary_button
from components.footer import show_footer


def show_home(app):

    show_navbar()

    show_hero(
        "Experiment Analytics, Without the Guesswork.",
        "Analyze experiments, measure impact, and make statistically informed decisions.",
    )

    # =====================================================
    # PROJECT
    # =====================================================

    st.markdown(
        '<div class="ab-section-title">Start a new analysis</div>',
        unsafe_allow_html=True,
    )

    app["project_name"] = st.text_input(
        "Project name",
        value=app.get("project_name", ""),
        placeholder="e.g. Homepage CTA Experiment",
        key="home_project_name",
    )

    st.divider()

    # =====================================================
    # ANALYSIS MODES
    # =====================================================

    st.markdown(
        '<div class="ab-section-title">Choose your analysis method</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="ab-section-description">'
        "Choose based on how your experiment data is available."
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        analysis_card(
            "Manual A/B",
            "Enter Variant A and Variant B data directly. "
            "Useful for testing the analytics engine without a live website.",
            "✍️",
        )

        st.write("")

        if primary_button(
            "Use Manual A/B",
            key="home_manual",
        ):
            app["mode"] = "manual"
            app["page"] = "configure"
            st.rerun()

    with col2:

        analysis_card(
            "Historical Comparison",
            "Compare two different GA4 date ranges. "
            "This is a historical comparison, not a simultaneous experiment.",
            "📊",
        )

        st.write("")

        if primary_button(
            "Use Historical",
            key="home_historical",
        ):
            app["mode"] = "historical"
            app["page"] = "configure"
            st.rerun()

    with col3:

        analysis_card(
            "True A/B Experiment",
            "Compare simultaneously exposed Control and Treatment "
            "groups using experiment data.",
            "🧪",
        )

        st.write("")

        if primary_button(
            "Use True A/B",
            key="home_true_ab",
        ):
            app["mode"] = "experiment"
            app["page"] = "configure"
            st.rerun()

    # =====================================================
    # WHAT ABLYTICS MEASURES
    # =====================================================

    st.write("")

    st.markdown(
        '<div class="ab-section">'
        '<div class="ab-section-title">What ABlytics measures</div>'
        '<div class="ab-section-description">'
        "Core analytics capabilities available in the platform."
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        stat_card("Core Metrics", "8")

    with m2:
        stat_card("Statistical Methods", "5+")

    with m3:
        stat_card("Data Sources", "2")

    with m4:
        stat_card("Report Types", "3")

    show_footer()