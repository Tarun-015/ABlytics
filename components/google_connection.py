import streamlit as st

from ga4.auth import get_credentials
from ga4.client import GA4Client


def connect_google_analytics():

    st.subheader("Google Analytics")

    if "ga4_properties" not in st.session_state:

        st.session_state.ga4_properties = None

    if st.session_state.ga4_properties is None:

        if st.button(
            "Connect Google Analytics",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "Connecting to Google Analytics..."
                ):

                    credentials = get_credentials()

                    client = GA4Client(credentials)

                    properties = client.list_properties()

                    st.session_state.ga4_properties = properties
                    st.session_state.ga4_credentials = credentials

                    st.success(
                        "Google Analytics connected successfully."
                    )

                    st.rerun()

            except Exception as e:

                st.error(
                    f"Google Analytics connection failed: {e}"
                )

        return None

    st.success("Google Analytics connected")

    return st.session_state.ga4_properties