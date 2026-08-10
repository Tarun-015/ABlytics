import streamlit as st


def show_loader(message="Loading..."):

    return st.spinner(message)