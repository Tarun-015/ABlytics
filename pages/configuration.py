import streamlit as st

from experiments.manual import manual_configuration
from experiments.historical import historical_configuration
from experiments.true_ab import experiment_configuration

from validation.validator import validate_dataset

from components.hero import show_hero
from components.alerts import info, error
from components.footer import show_footer

from engine.analysis_engine import AnalysisEngine
from components.google_connection import connect_google_analytics
from components.property_selector import show_property_selector


def show_configuration(app):

    show_hero(
        "Experiment Configuration",
        "Configure the data required for your selected analysis.",
    )

    info(
        f"Project: {app['project_name'] or 'Not specified'}"
    )

    info(
        f"Analysis Mode: {app['mode']}"
    )

    # =========================================================
    # GA4 CONNECTION
    # =========================================================

    properties = None

    if app["mode"] in ["historical", "experiment"]:

        properties = connect_google_analytics()

        if properties:

            selected_property = show_property_selector(
                properties
            )

            if selected_property:

                app["ga4"] = selected_property

    # =========================================================
    # MODE CONFIGURATION
    # =========================================================

    if app["mode"] == "manual":

        dataset = manual_configuration()

    elif app["mode"] == "historical":

        dataset = historical_configuration(app)

    elif app["mode"] == "experiment":

        dataset = experiment_configuration(app)

    else:

        st.error("Unknown analysis mode.")

        return

    # =========================================================
    # PROJECT INFORMATION
    # =========================================================

    dataset.project_name = app["project_name"]

    # =========================================================
    # ACTIONS
    # =========================================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            app["page"] = "home"

            st.rerun()

    with col2:

        if st.button(
            "Run Analysis →",
            type="primary",
            use_container_width=True
        ):

            # ---------------------------------------------
            # Validate dataset
            # ---------------------------------------------

            is_valid, errors = validate_dataset(dataset)

            if not is_valid:

                for message in errors:

                    error(message)

            else:

                # -----------------------------------------
                # Run analysis
                # -----------------------------------------

                try:

                    engine = AnalysisEngine(dataset)

                    result = engine.run()

                    app["dataset"] = dataset

                    app["analysis_result"] = result

                    app["page"] = "dashboard"

                    st.rerun()

                except Exception as exc:

                    error(
                        f"Analysis failed: {exc}"
                    )

    show_footer()