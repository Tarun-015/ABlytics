import streamlit as st

from components.navbar import show_navbar
from components.hero import show_hero
from components.footer import show_footer


def show_documentation(app):

    show_navbar()

    show_hero(
        "Documentation",
        "Understand the experiment workflow, metrics, data sources, and storage model behind ABlytics.",
    )

    # =====================================================
    # GETTING STARTED
    # =====================================================

    st.markdown("## Getting Started")

    st.write(
        """
        ABlytics provides three analysis modes. Choose the mode that matches
        the source and structure of your experiment data.
        """
    )

    st.divider()

    # =====================================================
    # MODES
    # =====================================================

    st.markdown("## Analysis Modes")

    with st.expander("Manual A/B", expanded=True):

        st.write(
            """
            Manual A/B allows the user to enter Variant A and Variant B
            values directly.

            It is useful for:

            - Testing the analytics pipeline
            - Demonstrations
            - Testing statistical calculations
            - Working with data that is already aggregated
            """
        )

    with st.expander("Historical Comparison"):

        st.write(
            """
            Historical Comparison retrieves data from two different GA4
            date ranges.

            Example:

            Period A → January 1 to January 15

            Period B → January 16 to January 31

            This should be treated as a historical comparison rather than
            a true simultaneous A/B experiment.
            """
        )

    with st.expander("True A/B Experiment"):

        st.write(
            """
            True A/B analysis is intended for experiments where users are
            simultaneously assigned to different variants.

            Example:

            Control → 50% of eligible users

            Treatment → 50% of eligible users

            The two groups can then be compared using experiment metrics
            and statistical analysis.
            """
        )

    st.divider()

    # =====================================================
    # METRICS
    # =====================================================

    st.markdown("## Metrics")

    metrics = {
        "Conversion Rate": "Conversions divided by the relevant user or visitor population.",
        "CTR": "Clicks divided by impressions.",
        "Bounce Rate": "The proportion of sessions considered bounced.",
        "Revenue per Session": "Revenue generated per session.",
        "New User Rate": "New users relative to the relevant user population.",
        "Session Duration": "Average duration of user sessions.",
        "Funnel Completion": "The proportion of users progressing through the defined funnel.",
        "Funnel Drop-off": "The proportion of users lost between funnel stages.",
    }

    for name, description in metrics.items():

        st.markdown(f"**{name}**")

        st.caption(description)

    st.divider()

    # =====================================================
    # STATISTICS
    # =====================================================

    st.markdown("## Statistical Analysis")

    st.write(
        """
        ABlytics separates descriptive metric comparison from statistical
        analysis.

        The purpose of statistical testing is to determine whether the
        observed difference between variants provides sufficient evidence
        against the relevant null hypothesis.
        """
    )

    with st.expander("Statistical significance"):

        st.write(
            """
            Statistical significance helps determine whether an observed
            difference is unlikely to have occurred under the null hypothesis.
            """
        )

    with st.expander("Confidence intervals"):

        st.write(
            """
            Confidence intervals provide a range around an estimated effect
            and help communicate uncertainty around the result.
            """
        )

    with st.expander("Statistical power"):

        st.write(
            """
            Statistical power describes the probability of detecting an effect
            of a specified size under the assumptions of the test.
            """
        )

    st.divider()

    # =====================================================
    # GA4
    # =====================================================

    st.markdown("## Google Analytics 4")

    st.write(
        """
        Historical and True A/B modes can use Google Analytics 4 as a data
        source.

        The user authenticates through Google OAuth and selects a GA4
        property that the authenticated Google account has permission to
        access.
        """
    )

    st.warning(
        "The Google account must have sufficient access to the selected GA4 property."
    )

    st.divider()

    # =====================================================
    # DATABASE
    # =====================================================

    st.markdown("## What does the database store?")

    st.write(
        """
        ABlytics should separate experiment configuration from raw
        authentication credentials.

        Experiment-related records can include:
        """
    )

    st.markdown(
        """
        - Project / experiment name
        - Analysis mode
        - Selected GA4 property identifier
        - Variant names
        - Selected metrics
        - Experiment configuration
        - Analysis results or saved reports
        - Timestamps
        """
    )

    st.error(
        "Google OAuth access tokens and client secrets should not be stored as ordinary experiment data or committed to GitHub."
    )

    st.divider()

    # =====================================================
    # PIPELINE
    # =====================================================

    st.markdown("## ABlytics Data Pipeline")

    st.code(
        """
Google OAuth / Manual Input
          ↓
Data Source
          ↓
GA4 / Manual Data
          ↓
GA4 Parser / Normalization
          ↓
StandardDataset
          ↓
Validation
          ↓
Analytics Engine
          ↓
Metrics + Comparison
          ↓
Statistical Analysis
          ↓
Dashboard
        """,
        language="text",
    )

    show_footer()