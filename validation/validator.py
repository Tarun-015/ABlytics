from core.schema import StandardDataset


def validate_dataset(
    dataset: StandardDataset,
) -> tuple[bool, list[str]]:

    errors = []

    # =========================================================
    # Basic dataset validation
    # =========================================================

    if not isinstance(dataset, StandardDataset):
        return False, ["Invalid dataset type."]

    if not dataset.selected_metrics:
        errors.append(
            "Select at least one metric."
        )

    # =========================================================
    # Variant validation
    # =========================================================

    if dataset.variant_a is None:
        errors.append(
            "Variant A data is missing."
        )

    if dataset.variant_b is None:
        errors.append(
            "Variant B data is missing."
        )

    # =========================================================
    # True A/B specific validation
    # =========================================================

    if dataset.source == "true_ab":

        experiment_name = dataset.meta.get(
            "experiment_name"
        )

        if not experiment_name:
            errors.append(
                "Enter an experiment name."
            )

        variant_dimension = dataset.meta.get(
            "variant_dimension"
        )

        if not variant_dimension:
            errors.append(
                "Specify the GA4 variant dimension."
            )

        property_id = dataset.meta.get(
            "property_id"
        )

        if not property_id:
            errors.append(
                "Select a GA4 property."
            )

    # =========================================================
    # Historical validation
    # =========================================================

    if dataset.source == "historical":

        period_a = dataset.meta.get(
            "period_a",
            {}
        )

        period_b = dataset.meta.get(
            "period_b",
            {}
        )

        if not period_a.get("start"):
            errors.append(
                "Select Period A start date."
            )

        if not period_a.get("end"):
            errors.append(
                "Select Period A end date."
            )

        if not period_b.get("start"):
            errors.append(
                "Select Period B start date."
            )

        if not period_b.get("end"):
            errors.append(
                "Select Period B end date."
            )

    # =========================================================
    # Date validation
    # =========================================================

    if dataset.source in ["historical", "true_ab"]:

        if dataset.source == "true_ab":

            start = dataset.meta.get(
                "start_date"
            )

            end = dataset.meta.get(
                "end_date"
            )

            if start and end and start > end:

                errors.append(
                    "Experiment start date cannot be "
                    "after the end date."
                )

    # =========================================================
    # Final result
    # =========================================================

    return (
        len(errors) == 0,
        errors,
    )