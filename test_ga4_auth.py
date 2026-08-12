from ga4.auth import get_credentials


print("Starting Google authentication...")

credentials = get_credentials()

print()
print("================================")
print("GA4 AUTHENTICATION SUCCESSFUL")
print("================================")
print()

print("Token available:", credentials.token is not None)
print("Credentials valid:", credentials.valid)