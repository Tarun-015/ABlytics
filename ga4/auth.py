from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


BASE_DIR = Path(__file__).resolve().parent.parent

CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly"
]


def get_credentials():

    credentials = None

    # -----------------------------------------
    # Existing token
    # -----------------------------------------

    if TOKEN_FILE.exists():

        credentials = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES
        )

    # -----------------------------------------
    # Already authenticated
    # -----------------------------------------

    if credentials and credentials.valid:

        return credentials

    # -----------------------------------------
    # Refresh expired token
    # -----------------------------------------

    if (
        credentials
        and credentials.expired
        and credentials.refresh_token
    ):

        credentials.refresh(Request())

    # -----------------------------------------
    # First-time Google login
    # -----------------------------------------

    else:

        if not CREDENTIALS_FILE.exists():

            raise FileNotFoundError(
                "credentials.json was not found in the ABlytics project root."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE),
            SCOPES
        )

        credentials = flow.run_local_server(
            host="127.0.0.1",
            bind_addr="127.0.0.1",
            port=0,
            open_browser=True
        )

    # -----------------------------------------
    # Save token
    # -----------------------------------------

    TOKEN_FILE.write_text(
        credentials.to_json()
    )

    return credentials