import streamlit as st


def analysis_card(icon, title, description):

    with st.container(border=True):

        st.markdown(f"### {icon} {title}")

        st.write(description)


def metric_card(title, value, subtitle=""):

    with st.container(border=True):

        st.caption(title)

        st.markdown(
            f"## {value}"
        )

        if subtitle:
            st.caption(subtitle)