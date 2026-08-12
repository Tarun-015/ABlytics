import streamlit as st

from config.constants import PRIMARY_METRICS
from core.schema import StandardDataset, VariantData
from ga4.auth import get_credentials
from ga4.fetcher import GA4Fetcher
from ga4.parser import GA4Parser


def historical_configuration(app) -> StandardDataset:

    st.subheader("Historical Comparison")

    st.info(
        "Compare two GA4 date ranges. "
        "This is a historical comparison, not a simultaneous A/B experiment."
    )

    # -------------------------------------------------
    # GA4 Property
    # -------------------------------------------------

    ga4_property = app.get("ga4")

    if not ga4_property:

        st.warning(
            "Connect Google Analytics and select a GA4 property first."
        )

        return StandardDataset(
            source="historical",
            selected_metrics=[],
            variant_a=VariantData(),
            variant_b=VariantData()
        )

    property_id = ga4_property["property_id"]

    st.success(
        f"Connected property: "
        f"{ga4_property['property_name']} "
        f"({property_id})"
    )

    # -------------------------------------------------
    # Date Ranges
    # -------------------------------------------------

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

    # -------------------------------------------------
    # Metrics
    # -------------------------------------------------

    st.divider()

    selected_metrics = st.multiselect(
        "Select Metrics",
        PRIMARY_METRICS,
        default=["Conversion Rate"],
        key="historical_metrics"
    )

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    if start_a > end_a:

        st.error(
            "Period A start date cannot be after its end date."
        )

    if start_b > end_b:

        st.error(
            "Period B start date cannot be after its end date."
        )

    # -------------------------------------------------
    # Fetch GA4 Data
    # -------------------------------------------------

    if st.button(
        "Fetch GA4 Data",
        use_container_width=True
    ):

        if start_a > end_a or start_b > end_b:

            st.error(
                "Please correct the date ranges before fetching data."
            )

            st.stop()

        if not selected_metrics:

            st.error(
                "Select at least one metric."
            )

            st.stop()

        try:

            with st.spinner("Fetching GA4 data..."):

                credentials = app.get("ga4_credentials")

                if credentials is None:
                    credentials = get_credentials()

                fetcher = GA4Fetcher(
                    credentials=credentials,
                    property_id=property_id
                )

                parser = GA4Parser()

                # -----------------------------------------
                # GA4 metrics
                # -----------------------------------------

                metric_names = [
                    "sessions",
                    "totalUsers",
                    "newUsers",
                    "conversions",
                    "bounceRate",
                    "averageSessionDuration",
                    "totalRevenue",
                ]

                # -----------------------------------------
                # Period A
                # -----------------------------------------

                response_a = fetcher.run_report(
                    start_date=start_a.isoformat(),
                    end_date=end_a.isoformat(),
                    dimensions=[],
                    metrics=metric_names
                )

                # -----------------------------------------
                # Period B
                # -----------------------------------------

                response_b = fetcher.run_report(
                    start_date=start_b.isoformat(),
                    end_date=end_b.isoformat(),
                    dimensions=[],
                    metrics=metric_names
                )

                # -----------------------------------------
                # Convert responses
                # -----------------------------------------

                variant_a = parser.build_variant_data(
                    response=response_a,
                    metric_names=metric_names
                )

                variant_b = parser.build_variant_data(
                    response=response_b,
                    metric_names=metric_names
                )

                # -----------------------------------------
                # Convert GA4 names to schema names
                # -----------------------------------------

                # variant_a.bounces = int(
                #     variant_a.sessions * variant_a.bounceRate
                # )

                # variant_b.bounces = int(
                #     variant_b.sessions * variant_b.bounceRate
                # )

                # -----------------------------------------
                # Save in session state
                # -----------------------------------------

                app["historical_variants"] = {
                    "variant_a": variant_a,
                    "variant_b": variant_b
                }

                st.success(
                    "GA4 data fetched successfully."
                )

                st.rerun()

        except Exception as e:

            st.error(
                f"Unable to fetch GA4 data: {e}"
            )

    # -------------------------------------------------
    # Existing fetched data
    # -------------------------------------------------

    historical_data = app.get(
        "historical_variants"
    )

    if historical_data:

        variant_a = historical_data["variant_a"]
        variant_b = historical_data["variant_b"]

        st.divider()

        st.markdown("### Retrieved Data")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### Period A")

            st.metric(
                "Sessions",
                f"{variant_a.sessions:,}"
            )

            st.metric(
                "Users",
                f"{variant_a.users:,}"
            )

            st.metric(
                "Conversions",
                f"{variant_a.conversions:,}"
            )

        with col2:

            st.markdown("#### Period B")

            st.metric(
                "Sessions",
                f"{variant_b.sessions:,}"
            )

            st.metric(
                "Users",
                f"{variant_b.users:,}"
            )

            st.metric(
                "Conversions",
                f"{variant_b.conversions:,}"
            )

    else:

        variant_a = VariantData()
        variant_b = VariantData()

    # -------------------------------------------------
    # Standard Dataset
    # -------------------------------------------------

    return StandardDataset(

        source="historical",

        selected_metrics=selected_metrics,

        variant_a=variant_a,

        variant_b=variant_b,

        project_name=app.get(
            "project_name",
            ""
        ),

        variant_a_label=(
            f"Period A "
            f"({start_a} to {end_a})"
        ),

        variant_b_label=(
            f"Period B "
            f"({start_b} to {end_b})"
        ),

        meta={

            "period_a": {
                "start": start_a,
                "end": end_a
            },

            "period_b": {
                "start": start_b,
                "end": end_b
            },

            "property_id": property_id,

            "property_name": (
                ga4_property["property_name"]
            )
        }
    )