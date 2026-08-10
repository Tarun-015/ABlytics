import streamlit as st


def show_hero(title, description):

    with st.container(border=True):

        st.title(title)

        st.write(description)