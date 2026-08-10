import streamlit as st


def show_summary_panel(dataset):
    with st.container(border=True):
        st.markdown("### Experiment Summary")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.caption("Project")
            st.write(dataset.project_name or "Untitled")
        with c2:
            st.caption("Mode")
            st.write({"manual": "Manual Analysis", "historical": "Historical Comparison",
                      "true_ab": "True A/B Experiment"}.get(dataset.source, dataset.source))
        with c3:
            st.caption("Metrics Analyzed")
            st.write(", ".join(dataset.selected_metrics) or "—")
