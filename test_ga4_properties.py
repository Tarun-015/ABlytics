from ga4.auth import get_credentials
from ga4.client import GA4Client


print("Connecting to Google Analytics...")

credentials = get_credentials()

client = GA4Client(credentials)

properties = client.list_properties()

print()
print("GA4 properties available to this account:")
print("------------------------------------------")

if not properties:
    print("No accessible GA4 properties found.")

else:

    for property_data in properties:

        print()
        print(f"Account   : {property_data['account_name']}")
        print(f"Property  : {property_data['property_name']}")
        print(f"Property ID: {property_data['property_id']}")
        print(f"Resource  : {property_data['property_resource']}")