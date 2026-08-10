import streamlit as st

from experiments.manual import manual_configuration
from experiments.historical import historical_configuration
from experiments.true_ab import experiment_configuration

from validation.validator import validate_dataset

from components.hero import show_hero
from components.alerts import info, error
from components.footer import show_footer

from engine.analysis_engine import AnalysisEngine


def show_configuration(app):

    show_hero(
        "Experiment Configuration",
        "Configure the data required for your selected analysis.",
    )

    info(f"Project: {app['project_name'] or 'Not specified'}")
    info(f"Analysis Mode: {app['mode']}")

    st.divider()

    if app["mode"] == "manual":
        dataset = manual_configuration()
    elif app["mode"] == "historical":
        dataset = historical_configuration()
    elif app["mode"] == "experiment":
        dataset = experiment_configuration()
    else:
        st.error("No analysis mode selected.")
        return

    dataset.project_name = app["project_name"]

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", use_container_width=True):
            app["page"] = "home"
            st.rerun()

    with col2:
        if st.button("Run Analysis →", use_container_width=True):
            is_valid, errors = validate_dataset(dataset)

            if not is_valid:
                for message in errors:
                    error(message)
            else:
                app["dataset"] = dataset
                app["results"] = AnalysisEngine(dataset).run()
                app["page"] = "dashboard"
                st.rerun()

    show_footer()
