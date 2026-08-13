import streamlit as st


def analysis_card(
    title,
    description,
    icon="",
):
    st.markdown(
        f"""
        <div class="ab-card">
            <div class="ab-card-icon">{icon}</div>
            <div class="ab-card-title">{title}</div>
            <div class="ab-card-description">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_card(label, value):
    st.markdown(
        f"""
        <div class="ab-stat-card">
            <div class="ab-stat-value">{value}</div>
            <div class="ab-stat-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )