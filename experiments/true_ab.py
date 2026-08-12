import streamlit as st
from ga4.fetcher import GA4Fetcher
from ga4.parser import GA4Parser
from ga4.auth import get_credentials

from config.constants import PRIMARY_METRICS
from core.schema import StandardDataset, VariantData


def experiment_configuration(app) -> StandardDataset:

    st.subheader("True A/B Experiment")

    st.info(
        "True A/B Experiment compares simultaneously exposed "
        "Variant A and Variant B users."
    )

    # =========================================================
    # GA4 PROPERTY
    # =========================================================

    ga4_property = app.get("ga4")

    if ga4_property:

        st.success(
            f"Connected property: "
            f"{ga4_property.get('display_name', 'GA4 Property')} "
            f"({ga4_property.get('property_id', '')})"
        )

    else:

        st.warning(
            "Connect a GA4 property before configuring the experiment."
        )

    st.divider()

    # =========================================================
    # EXPERIMENT
    # =========================================================

    st.markdown("### Experiment")

    experiment_name = st.text_input(
        "Experiment Name",
        placeholder="Homepage CTA Experiment",
        key="true_ab_experiment_name",
    )

    # =========================================================
    # DATE RANGE
    # =========================================================

    st.markdown("### Experiment Period")

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "Start Date",
            key="true_ab_start_date",
        )

    with col2:

        end_date = st.date_input(
            "End Date",
            key="true_ab_end_date",
        )

    st.divider()

    # =========================================================
    # VARIANTS
    # =========================================================

    st.markdown("### Variants")

    col1, col2 = st.columns(2)

    with col1:

        variant_a = st.text_input(
            "Variant A",
            value="Control",
            key="true_ab_variant_a",
        )

    with col2:

        variant_b = st.text_input(
            "Variant B",
            value="Treatment",
            key="true_ab_variant_b",
        )

    st.divider()

    # =========================================================
    # VARIANT DIMENSION
    # =========================================================

    st.markdown("### GA4 Variant Dimension")

    variant_dimension = st.text_input(
        "Dimension used to identify variants",
        value="experiment_variant",
        help=(
            "The GA4 dimension containing the Control/Treatment "
            "assignment."
        ),
        key="true_ab_variant_dimension",
    )

    st.caption(
        "This must match a dimension actually available in the "
        "selected GA4 property."
    )

    st.divider()

    # =========================================================
    # METRICS
    # =========================================================

    selected_metrics = st.multiselect(
        "Select Metrics",
        PRIMARY_METRICS,
        default=["Conversion Rate"],
        key="true_ab_metrics",
    )

    # =========================================================
    # CURRENT STATUS
    # =========================================================

    st.info(
        "Configuration is ready. The next pipeline step will "
        "query GA4 using the selected variant dimension and "
        "map the returned Control/Treatment rows into "
        "StandardDataset."
    )

    return StandardDataset(
        source="true_ab",
        selected_metrics=selected_metrics,
        variant_a=VariantData(),
        variant_b=VariantData(),
        variant_a_label=variant_a or "Variant A",
        variant_b_label=variant_b or "Variant B",
        meta={
            "experiment_name": experiment_name,
            "start_date": start_date,
            "end_date": end_date,
            "variant_dimension": variant_dimension,
            "property_id": (
                ga4_property.get("property_id")
                if ga4_property
                else None
            ),
        },
    )