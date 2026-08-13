import streamlit as st

from components.navbar import show_navbar
from components.hero import show_hero
from components.footer import show_footer


def show_analytics(app):

    show_navbar()

    show_hero(
        "Analytics",
        "Understand how ABlytics turns experiment data into measurable product decisions.",
    )

    st.markdown(
        '<div class="ab-section-title">What ABlytics does</div>',
        unsafe_allow_html=True,
    )

    st.write(
        """
        ABlytics is an experiment analytics platform designed to compare
        Variant A and Variant B, calculate business metrics, evaluate
        statistical evidence, and produce an experiment recommendation.
        """
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 1. Measure")

        st.write(
            """
            ABlytics calculates experiment metrics such as:

            - Conversion Rate
            - Click-through Rate
            - Bounce Rate
            - Revenue per Session
            - New User Rate
            - Session Duration
            - Funnel Completion
            - Funnel Drop-off
            """
        )

    with col2:

        st.markdown("### 2. Compare")

        st.write(
            """
            Variant A and Variant B are compared using their underlying
            counts and values rather than relying only on raw percentages.
            """
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 3. Test")

        st.write(
            """
            Statistical analysis evaluates whether the observed difference
            provides enough evidence to distinguish the variants.
            """
        )

    with col2:

        st.markdown("### 4. Decide")

        st.write(
            """
            The dashboard combines the metric comparison and statistical
            results into an experiment verdict and recommendation.
            """
        )

    st.divider()

    st.markdown("### Analysis modes")

    st.info(
        "Manual A/B is intended for directly entered experiment data."
    )

    st.info(
        "Historical Comparison compares two GA4 date ranges and should "
        "not be interpreted as a simultaneous A/B experiment."
    )

    st.info(
        "True A/B is intended for simultaneously exposed experiment "
        "variants."
    )

    show_footer()