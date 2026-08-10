import streamlit as st

from exports.csv_export import export_csv
from exports.json_export import export_json
from exports.pdf_export import export_pdf


def show_export_panel(results: dict):
    st.markdown("### Export")

    dataset = results["dataset"]
    c1, c2, c3 = st.columns(3)

    with c1:
        st.download_button(
            "⬇ CSV (comparison table)",
            data=export_csv(results["comparison"]),
            file_name="ablytics_comparison.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "⬇ JSON (full results)",
            data=export_json(results),
            file_name="ablytics_results.json",
            mime="application/json",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            "⬇ PDF (summary report)",
            data=export_pdf(dataset.project_name, results["statistics"], results["comparison"]),
            file_name="ablytics_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
