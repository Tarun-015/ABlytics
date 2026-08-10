import streamlit as st

from config.constants import PRIMARY_METRICS
from core.schema import StandardDataset, VariantData


def experiment_configuration() -> StandardDataset:

    st.subheader("True A/B Experiment")

    st.info(
        "True A/B Experiment will use data from a live GA4 experiment."
    )

    st.markdown("### Experiment")

    experiment_name = st.text_input(
        "Experiment Name",
        placeholder="Homepage CTA Experiment",
        key="true_ab_experiment_name"
    )

    st.divider()

    st.markdown("### Variants")

    col1, col2 = st.columns(2)

    with col1:

        variant_a = st.text_input(
            "Variant A",
            value="Control",
            key="true_ab_variant_a"
        )

    with col2:

        variant_b = st.text_input(
            "Variant B",
            value="Treatment",
            key="true_ab_variant_b"
        )

    st.divider()

    selected_metrics = st.multiselect(
        "Select Metrics",
        PRIMARY_METRICS,
        default=["Conversion Rate"],
        key="true_ab_metrics"
    )

    st.warning(
        "GA4 experiment fetching is not yet implemented (see ga4/fetcher.py). "
        "This mode cannot produce results until that pipeline is built — "
        "it currently returns empty variant data, which will fail validation "
        "by design rather than silently showing a fake result."
    )

    return StandardDataset(
        source="true_ab",
        selected_metrics=selected_metrics,
        variant_a=VariantData(),
        variant_b=VariantData(),
        variant_a_label=variant_a or "Variant A",
        variant_b_label=variant_b or "Variant B",
        meta={"experiment_name": experiment_name},
    )