import streamlit as st


def connect_google_analytics():
    """
    Connect to Google Analytics only when the user selects
    Historical Comparison or True A/B Experiment.

    The Home page and Manual A/B mode do not require GA4.
    """

    try:
        from ga4.auth import get_credentials
        from ga4.client import GA4Client

        credentials = get_credentials()

        client = GA4Client(credentials)

        return client.list_properties()

    except FileNotFoundError:
        st.warning(
            "Google Analytics is not configured yet. "
            "You can still use Manual A/B Analysis."
        )
        return None

    except Exception as e:
        st.error(
            f"Google Analytics connection failed: {e}"
        )
        return None