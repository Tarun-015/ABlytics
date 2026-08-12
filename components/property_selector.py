import streamlit as st


def show_property_selector(properties):

    if not properties:
        st.warning(
            "No GA4 properties were found for this Google account."
        )
        return None

    st.subheader("Select GA4 Property")

    options = {
        f"{item['property_name']} "
        f"({item['account_name']})": item
        for item in properties
    }

    selected_label = st.selectbox(
        "GA4 Property",
        options=list(options.keys())
    )

    selected = options[selected_label]

    st.caption(
        f"Property ID: {selected['property_id']}"
    )

    return selected