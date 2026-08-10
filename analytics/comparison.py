"""
Variant comparison — now direction-aware. The previous version reported a
raw percentage_change for every metric with no sense of whether a positive
change was good or bad, which is wrong for metrics like Bounce Rate and
Drop-off Rate where a *decrease* is the improvement. Downstream (dashboard,
decision engine) needs to know "did B improve on A", not just "B minus A".
"""

from config.constants import METRIC_SPECS


def compare_variants(metrics: dict) -> list[dict]:
    comparison = []

    variant_a = metrics["variant_a"]
    variant_b = metrics["variant_b"]

    for metric_name in variant_a:
        value_a = variant_a[metric_name]
        value_b = variant_b[metric_name]

        if value_a is None or value_b is None:
            comparison.append({
                "metric": metric_name,
                "variant_a": value_a,
                "variant_b": value_b,
                "difference": None,
                "percentage_change": None,
                "improved": None,
            })
            continue

        difference = value_b - value_a
        percentage_change = (difference / value_a * 100) if value_a != 0 else None

        spec = METRIC_SPECS.get(metric_name)
        higher_is_better = spec.higher_is_better if spec else True
        improved = (difference > 0) if higher_is_better else (difference < 0)

        comparison.append({
            "metric": metric_name,
            "variant_a": value_a,
            "variant_b": value_b,
            "difference": difference,
            "percentage_change": percentage_change,
            "improved": improved,
        })

    return comparison
