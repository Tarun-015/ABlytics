import streamlit as st


def primary_button(label, key=None):

    return st.button(
        label,
        key=key,
        type="primary",
        use_container_width=True
    )


def secondary_button(label, key=None):

    return st.button(
        label,
        key=key,
        use_container_width=True
    )