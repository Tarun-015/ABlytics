"""
Pure validation logic.

validate_dataset() takes a StandardDataset and returns (is_valid, errors) —
it has no dependency on Streamlit and no side effects. This is what makes it
reusable across every future entry point (the current Streamlit UI, a future
API endpoint, a GA4 batch job, or a unit test) instead of being hard-wired to
st.error() calls, which the previous version was.

The Streamlit page is responsible for deciding how to *display* the errors;
this module is only responsible for deciding what they are.
"""

from config.constants import METRIC_SPECS


def validate_dataset(dataset) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if not dataset.selected_metrics:
        errors.append("Select at least one metric.")
        return False, errors

    va, vb = dataset.variant_a, dataset.variant_b

    for metric_name in dataset.selected_metrics:
        spec = METRIC_SPECS.get(metric_name)
        if spec is None:
            errors.append(f"Unknown metric: {metric_name}")
            continue

        if spec.kind == "ratio":
            num, den = spec.numerator, spec.denominator
            for label, variant in (("Variant A", va), ("Variant B", vb)):
                denom_val = variant.get(den, 0)
                if denom_val is None or denom_val <= 0:
                    errors.append(
                        f"{label}: {spec.denominator_label} must be greater than 0 "
                        f"for {metric_name}."
                    )
                    continue
                num_val = variant.get(num, 0)
                if num_val is None or num_val < 0:
                    errors.append(
                        f"{label}: {spec.numerator_label} cannot be negative "
                        f"for {metric_name}."
                    )
                if num_val is not None and denom_val and num_val > denom_val and not spec.numerator_is_float:
                    errors.append(
                        f"{label}: {spec.numerator_label} ({num_val}) cannot exceed "
                        f"{spec.denominator_label} ({denom_val}) for {metric_name}."
                    )

        elif spec.kind == "direct":
            for label, variant in (("Variant A", va), ("Variant B", vb)):
                val = variant.get(spec.field_name, None)
                if val is None or val < 0:
                    errors.append(f"{label}: {spec.field_label} must be 0 or greater.")

        elif spec.kind == "funnel":
            if not dataset.funnel_steps or len(dataset.funnel_steps) < 2:
                errors.append(
                    f"{metric_name} requires at least 2 funnel steps to be configured."
                )
            else:
                first = dataset.funnel_steps[0]
                if first.count_a <= 0 or first.count_b <= 0:
                    errors.append(
                        "The first funnel step must have a count greater than 0 "
                        "for both variants."
                    )
                for step in dataset.funnel_steps:
                    if step.count_a < 0 or step.count_b < 0:
                        errors.append(f"Funnel step '{step.name}' has a negative count.")
                for i in range(1, len(dataset.funnel_steps)):
                    prev, curr = dataset.funnel_steps[i - 1], dataset.funnel_steps[i]
                    if curr.count_a > prev.count_a or curr.count_b > prev.count_b:
                        errors.append(
                            f"Funnel step '{curr.name}' cannot have a higher count "
                            f"than the previous step '{prev.name}'."
                        )

    return (len(errors) == 0), errors
