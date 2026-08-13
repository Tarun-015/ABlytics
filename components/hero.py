import streamlit as st


def show_hero(title, description):
    st.markdown(
        f"""
        <div class="ab-hero">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )