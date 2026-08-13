import streamlit as st


def show_navbar():
    col1, col2, col3 = st.columns([5, 1, 1])

    with col1:
        st.markdown(
            '<div class="ab-brand">🧪 ABlytics</div>',
            unsafe_allow_html=True,
        )

    with col2:
        if st.button(
            "Analytics",
            key="nav_analytics",
            use_container_width=True,
        ):
            st.session_state.app["page"] = "analytics"
            st.rerun()

    with col3:
        if st.button(
            "Documentation",
            key="nav_documentation",
            use_container_width=True,
        ):
            st.session_state.app["page"] = "documentation"
            st.rerun()

    st.divider()