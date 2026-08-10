import streamlit as st

from components.navbar import show_navbar
from components.hero import show_hero
from components.footer import show_footer

from visualization.summary_panel import show_summary_panel
from visualization.verdict_banner import show_verdict_banner
from visualization.metric_cards import show_metric_cards
from visualization.comparison_table import show_comparison_table
from visualization.statistics_panel import show_statistics_panel
from visualization.recommendation_panel import show_recommendation_panel
from visualization.funnel_chart import show_funnel_chart
from visualization.export_panel import show_export_panel


def show_dashboard(app):

    show_navbar()

    show_hero(
        "Experiment Dashboard",
        "Analyze experiment performance and statistical significance.",
    )

    results = app.get("results")

    if not results:
        st.info("No analysis results are available yet.")
        if st.button("← Back to Home", use_container_width=True):
            app["page"] = "home"
            st.rerun()
        show_footer()
        return

    dataset = results["dataset"]

    # Experiment Summary
    show_summary_panel(dataset)

    # Overall Verdict
    show_verdict_banner(results["statistics"])

    st.divider()

    # Metric Cards
    show_metric_cards(results["comparison"])

    st.divider()

    # Variant Comparison
    show_comparison_table(results["comparison"])

    st.divider()

    # Funnel (only if funnel metrics were selected)
    if results.get("funnel"):
        show_funnel_chart(results["funnel"])
        st.divider()

    # Statistical Results
    show_statistics_panel(results["statistics"])

    st.divider()

    # Recommendation
    show_recommendation_panel(results["statistics"], dataset)

    st.divider()

    # Export
    show_export_panel(results)

    st.divider()

    if st.button("← New Analysis", use_container_width=True):
        app["page"] = "home"
        app["results"] = None
        app["dataset"] = None
        app["mode"] = None
        st.rerun()

    show_footer()
