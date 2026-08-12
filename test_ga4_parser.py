from ga4.auth import get_credentials
from ga4.fetcher import GA4Fetcher
from ga4.parser import GA4Parser


PROPERTY_ID = "549575686"


print("Authenticating...")

credentials = get_credentials()

fetcher = GA4Fetcher(
    credentials=credentials,
    property_id=PROPERTY_ID
)

parser = GA4Parser()


print("Fetching GA4 data...")

response = fetcher.run_report(
    start_date="30daysAgo",
    end_date="yesterday",
    dimensions=[],
    metrics=[
        "sessions",
        "totalUsers",
        "conversions"
    ]
)


variant = parser.build_variant_data(
    response=response,
    metric_names=[
        "sessions",
        "users",
        "conversions"
    ]
)


print()
print("Parsed VariantData")
print("------------------")

print("Sessions:", variant.sessions)
print("Users:", variant.users)
print("Conversions:", variant.conversions)