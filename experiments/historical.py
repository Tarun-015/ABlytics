import streamlit as st

from config.constants import PRIMARY_METRICS
from core.schema import StandardDataset, VariantData


def historical_configuration() -> StandardDataset:

    st.subheader("Historical Comparison")

    st.info(
        "Historical Comparison will compare two GA4 date ranges."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Period A")

        start_a = st.date_input(
            "Start Date (A)",
            key="historical_start_a"
        )

        end_a = st.date_input(
            "End Date (A)",
            key="historical_end_a"
        )

    with col2:

        st.markdown("### Period B")

        start_b = st.date_input(
            "Start Date (B)",
            key="historical_start_b"
        )

        end_b = st.date_input(
            "End Date (B)",
            key="historical_end_b"
        )

    st.divider()

    selected_metrics = st.multiselect(
        "Select Metrics",
        PRIMARY_METRICS,
        default=["Conversion Rate"],
        key="historical_metrics"
    )

    st.warning(
        "GA4 data fetching is not yet implemented (see ga4/fetcher.py). "
        "This mode cannot produce results until that pipeline is built — "
        "it currently returns empty variant data, which will fail validation "
        "by design rather than silently showing a fake result."
    )

    return StandardDataset(
        source="historical",
        selected_metrics=selected_metrics,
        variant_a=VariantData(),
        variant_b=VariantData(),
        meta={"period_a": {"start": start_a, "end": end_a}, "period_b": {"start": start_b, "end": end_b}},
    )