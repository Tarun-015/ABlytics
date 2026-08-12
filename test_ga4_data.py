from ga4.auth import get_credentials
from ga4.fetcher import GA4Fetcher


print("Authenticating...")

credentials = get_credentials()

PROPERTY_ID = "549575686"


fetcher = GA4Fetcher(
    credentials=credentials,
    property_id=PROPERTY_ID
)


print("Fetching GA4 data...")

response = fetcher.run_report(

    start_date="30daysAgo",

    end_date="yesterday",

    dimensions=[
        "date"
    ],

    metrics=[
        "sessions",
        "totalUsers",
        "conversions"
    ]
)


print()
print("GA4 DATA")
print("---------")


for row in response.rows:

    print(
        row.dimension_values[0].value,
        "|",
        row.metric_values[0].value,
        "|",
        row.metric_values[1].value,
        "|",
        row.metric_values[2].value
    )