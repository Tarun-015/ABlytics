import streamlit as st


def show_footer():
    st.markdown(
        """
        <div class="ab-footer">
            ABlytics · Experiment Analytics Platform
            <br>
            Measure. Compare. Decide.
        </div>
        """,
        unsafe_allow_html=True,
    )