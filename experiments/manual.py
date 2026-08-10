"""
Manual A/B configuration — data-driven from METRIC_SPECS.

Previously this file hand-wrote a near-identical `if "X" in selected_metrics:
st.number_input(...)` block eight times, once per metric, duplicated again
for both variant columns (so ~16 copy-pasted blocks total), and a third
near-identical copy lived in validation/validator.py and a fourth shape of
the same logic in analytics/metrics.py. All four now read from the same
config.constants.METRIC_SPECS table — add a 9th metric there and it appears
here, in validation, and in metrics automatically.
"""

import streamlit as st

from config.constants import METRIC_SPECS, PRIMARY_METRICS
from core.schema import StandardDataset, VariantData, FunnelStep


def _render_ratio_inputs(spec, variant_letter: str, default_num, default_den):
    denom = st.number_input(
        spec.denominator_label, min_value=1, value=int(default_den),
        key=f"manual_{variant_letter}_{spec.denominator}",
    )
    num_kwargs = dict(min_value=0.0, value=float(default_num)) if spec.numerator_is_float \
        else dict(min_value=0, value=int(default_num))
    num = st.number_input(
        spec.numerator_label, key=f"manual_{variant_letter}_{spec.numerator}", **num_kwargs,
    )
    return {spec.denominator: denom, spec.numerator: num}


def _render_direct_input(spec, variant_letter: str, default_val):
    val = st.number_input(
        spec.field_label, min_value=0, value=int(default_val),
        key=f"manual_{variant_letter}_{spec.field_name}",
    )
    return {spec.field_name: val}


def _render_funnel_steps():
    st.markdown("### Funnel Steps")
    st.caption("Ordered from first step (entry) to last step (conversion). At least 2 steps.")

    if "manual_funnel_step_count" not in st.session_state:
        st.session_state.manual_funnel_step_count = 3

    col_add, col_remove = st.columns(2)
    with col_add:
        if st.button("+ Add step", key="manual_add_funnel_step"):
            st.session_state.manual_funnel_step_count = min(
                st.session_state.manual_funnel_step_count + 1, 8
            )
    with col_remove:
        if st.button("- Remove step", key="manual_remove_funnel_step"):
            st.session_state.manual_funnel_step_count = max(
                st.session_state.manual_funnel_step_count - 1, 2
            )

    default_names = ["Landing Page", "Product View", "Add to Cart", "Checkout Started", "Purchase"]
    steps = []
    for i in range(st.session_state.manual_funnel_step_count):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            name = st.text_input(
                f"Step {i + 1} name",
                value=default_names[i] if i < len(default_names) else f"Step {i + 1}",
                key=f"manual_funnel_step_name_{i}",
            )
        with c2:
            count_a = st.number_input(
                "Variant A count", min_value=0,
                value=max(1000 - i * 250, 50),
                key=f"manual_funnel_step_a_{i}",
            )
        with c3:
            count_b = st.number_input(
                "Variant B count", min_value=0,
                value=max(1050 - i * 230, 50),
                key=f"manual_funnel_step_b_{i}",
            )
        steps.append(FunnelStep(name=name, count_a=count_a, count_b=count_b))
    return steps


def manual_configuration() -> StandardDataset:

    st.subheader("Manual A/B Test")

    selected_metrics = st.multiselect(
        "Select Metrics",
        PRIMARY_METRICS,
        default=["Conversion Rate"],
    )

    if not selected_metrics:
        st.info("Select at least one metric.")
        return StandardDataset(
            source="manual", selected_metrics=[],
            variant_a=VariantData(), variant_b=VariantData(),
        )

    st.divider()

    needs_funnel = any(METRIC_SPECS[m].kind == "funnel" for m in selected_metrics)
    funnel_steps = _render_funnel_steps() if needs_funnel else []

    if needs_funnel:
        st.divider()

    col1, col2 = st.columns(2)

    fields_a: dict = {}
    fields_b: dict = {}

    with col1:
        st.markdown("### Variant A")
        for metric_name in selected_metrics:
            spec = METRIC_SPECS[metric_name]
            if spec.kind == "ratio":
                fields_a.update(_render_ratio_inputs(spec, "a", spec.default_a[1], spec.default_a[0]))
            elif spec.kind == "direct":
                fields_a.update(_render_direct_input(spec, "a", spec.default_a[0]))

    with col2:
        st.markdown("### Variant B")
        for metric_name in selected_metrics:
            spec = METRIC_SPECS[metric_name]
            if spec.kind == "ratio":
                fields_b.update(_render_ratio_inputs(spec, "b", spec.default_b[1], spec.default_b[0]))
            elif spec.kind == "direct":
                fields_b.update(_render_direct_input(spec, "b", spec.default_b[0]))

    return StandardDataset(
        source="manual",
        selected_metrics=selected_metrics,
        variant_a=VariantData(**fields_a),
        variant_b=VariantData(**fields_b),
        funnel_steps=funnel_steps,
    )
