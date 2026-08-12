from typing import Any

from core.schema import VariantData


class GA4Parser:

    def parse_rows(self, response) -> list[dict[str, Any]]:
        """Convert GA4 response rows into simple dictionaries."""

        rows = []

        for row in response.rows:

            dimensions = [
                value.value
                for value in row.dimension_values
            ]

            metrics = [
                value.value
                for value in row.metric_values
            ]

            rows.append({
                "dimensions": dimensions,
                "metrics": metrics
            })

        return rows

    def parse_metric_report(
        self,
        response,
        metric_names: list[str]
    ) -> list[dict[str, Any]]:

        parsed = []

        for row in response.rows:

            values = {}

            for index, metric_name in enumerate(metric_names):

                raw_value = row.metric_values[index].value

                try:
                    value = float(raw_value)
                except (ValueError, TypeError):
                    value = raw_value

                values[metric_name] = value

            parsed.append(values)

        return parsed

    def parse_dimension_metric_report(
        self,
        response,
        dimension_names: list[str],
        metric_names: list[str]
    ) -> list[dict[str, Any]]:

        parsed = []

        for row in response.rows:

            record = {}

            for index, name in enumerate(dimension_names):
                record[name] = row.dimension_values[index].value

            for index, name in enumerate(metric_names):

                raw_value = row.metric_values[index].value

                try:
                    value = float(raw_value)
                except (ValueError, TypeError):
                    value = raw_value

                record[name] = value

            parsed.append(record)

        return parsed

    # =================================================
    # GA4 → VariantData
    # =================================================

    def build_variant_data(
        self,
        response,
        metric_names: list[str]
    ) -> VariantData:

        """
        Convert one aggregated GA4 response into VariantData.
        """

        data = VariantData()

        if not response.rows:
            return data

        row = response.rows[0]

        values = {}

        for index, metric_name in enumerate(metric_names):

            raw_value = row.metric_values[index].value

            try:
                values[metric_name] = float(raw_value)
            except (ValueError, TypeError):
                values[metric_name] = 0

        data.sessions = int(
            values.get("sessions", 0)
        )

        data.users = int(
            values.get("totalUsers", 0)
        )

        data.new_users = int(
            values.get("newUsers", 0)
        )

        data.conversions = int(
            values.get("conversions", 0)
        )

        data.revenue = float(
            values.get("totalRevenue", 0)
        )

        data.session_duration = float(
            values.get("averageSessionDuration", 0)
        )

        bounce_rate = float(
            values.get("bounceRate", 0)
        )

        data.bounces = int(
            data.sessions * bounce_rate
        )

        return data

    # =================================================
    # GA4 → A/B VariantData
    # =================================================

    def build_variant_data_from_rows(
        self,
        response,
        variant_a_label: str,
        variant_b_label: str,
        metric_names: list[str]
    ) -> tuple[VariantData, VariantData]:

        """
        Convert a GA4 dimension-based report into
        Variant A and Variant B.
        """

        variant_a = VariantData()
        variant_b = VariantData()

        for row in response.rows:

            if not row.dimension_values:
                continue

            variant_name = row.dimension_values[0].value

            values = {}

            for index, metric_name in enumerate(metric_names):

                raw_value = row.metric_values[index].value

                try:
                    values[metric_name] = float(raw_value)
                except (ValueError, TypeError):
                    values[metric_name] = 0

            data = VariantData()

            data.sessions = int(
                values.get("sessions", 0)
            )

            data.users = int(
                values.get("totalUsers", 0)
            )

            data.new_users = int(
                values.get("newUsers", 0)
            )

            data.conversions = int(
                values.get("conversions", 0)
            )

            data.revenue = float(
                values.get("totalRevenue", 0)
            )

            data.session_duration = float(
                values.get("averageSessionDuration", 0)
            )

            bounce_rate = float(
                values.get("bounceRate", 0)
            )

            data.bounces = int(
                data.sessions * bounce_rate
            )

            if variant_name == variant_a_label:

                variant_a = data

            elif variant_name == variant_b_label:

                variant_b = data

        return variant_a, variant_b