from datetime import date, timedelta

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

from google.oauth2.credentials import Credentials


class GA4Fetcher:

    def __init__(
        self,
        credentials: Credentials,
        property_id: str
    ):

        self.property_id = property_id

        self.client = BetaAnalyticsDataClient(
            credentials=credentials
        )

    def run_report(
        self,
        start_date: str,
        end_date: str,
        dimensions: list[str],
        metrics: list[str]
    ):

        request = RunReportRequest(

            property=f"properties/{self.property_id}",

            dimensions=[
                Dimension(name=dimension)
                for dimension in dimensions
            ],

            metrics=[
                Metric(name=metric)
                for metric in metrics
            ],

            date_ranges=[
                DateRange(
                    start_date=start_date,
                    end_date=end_date
                )
            ]
        )

        return self.client.run_report(request)