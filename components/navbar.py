import streamlit as st


def show_navbar():

    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.markdown("### 🧪 ABlytics")

    with col2:
        st.write("Analytics")

    with col3:
        st.write("Documentation")

    st.divider()