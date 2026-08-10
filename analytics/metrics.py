"""
Metric calculation — data-driven from METRIC_SPECS instead of one hand-written
if-block per metric. Adding a 9th metric to this platform now means adding one
entry to config/constants.py, not editing this file, experiments/manual.py,
AND validation/validator.py by hand in three places.

Every division is guarded: a metric with a zero denominator returns None
rather than raising ZeroDivisionError. This matters beyond the manual-entry
UI (which currently prevents zero denominators via Streamlit's min_value) —
GA4-sourced data in Historical/True A/B mode will not go through that UI
guard at all, so the guard belongs here, in the math itself.
"""

from config.constants import METRIC_SPECS
from analytics.funnel import calculate_funnel


def _safe_ratio(numerator, denominator, as_percentage: bool):
    if denominator is None or denominator == 0:
        return None
    if numerator is None:
        return None
    value = numerator / denominator
    return value * 100 if as_percentage else value


def calculate_metrics(dataset) -> dict:
    """dataset: a core.schema.StandardDataset"""

    va, vb = dataset.variant_a, dataset.variant_b
    metrics = {"variant_a": {}, "variant_b": {}}

    funnel_result = None
    if any(METRIC_SPECS[m].kind == "funnel" for m in dataset.selected_metrics):
        funnel_result = calculate_funnel(dataset)

    for metric_name in dataset.selected_metrics:
        spec = METRIC_SPECS.get(metric_name)
        if spec is None:
            continue

        if spec.kind == "ratio":
            metrics["variant_a"][metric_name] = _safe_ratio(
                va.get(spec.numerator), va.get(spec.denominator), spec.is_percentage
            )
            metrics["variant_b"][metric_name] = _safe_ratio(
                vb.get(spec.numerator), vb.get(spec.denominator), spec.is_percentage
            )

        elif spec.kind == "direct":
            metrics["variant_a"][metric_name] = va.get(spec.field_name)
            metrics["variant_b"][metric_name] = vb.get(spec.field_name)

        elif spec.kind == "funnel" and funnel_result:
            if metric_name == "Funnel Completion Rate":
                metrics["variant_a"][metric_name] = funnel_result["variant_a"]["completion_rate"]
                metrics["variant_b"][metric_name] = funnel_result["variant_b"]["completion_rate"]
            elif metric_name == "Drop-off Rate":
                metrics["variant_a"][metric_name] = funnel_result["variant_a"]["max_dropoff_rate"]
                metrics["variant_b"][metric_name] = funnel_result["variant_b"]["max_dropoff_rate"]

    return metrics
