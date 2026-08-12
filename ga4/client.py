from google.analytics.admin_v1beta import AnalyticsAdminServiceClient
from google.oauth2.credentials import Credentials


class GA4Client:

    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self.client = AnalyticsAdminServiceClient(
            credentials=credentials
        )

    def list_properties(self):
        """
        Return GA4 properties accessible to the authenticated user.
        """

        properties = []

        for account in self.client.list_account_summaries():

            for property_summary in account.property_summaries:

                properties.append({
                    "account_name": account.display_name,
                    "account_id": account.name,
                    "property_name": property_summary.display_name,
                    "property_id": property_summary.property.split("/")[-1],
                    "property_resource": property_summary.property,
                })

        return properties