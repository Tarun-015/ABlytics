import streamlit as st

_VERDICT_STYLE = {
    "Variant B wins": "success",
    "Variant A wins": "info",
    "Mixed results": "warning",
    "No significant difference": "warning",
    "Inconclusive — no testable metrics": "warning",
}


def show_verdict_banner(statistics_result: dict):
    verdict = statistics_result["overall_verdict"]
    style = _VERDICT_STYLE.get(verdict, "info")

    render = {"success": st.success, "warning": st.warning, "info": st.info}[style]
    render(f"**{verdict}**")

    note = statistics_result.get("multiple_testing_correction", {}).get("note")
    if note:
        st.caption(note)
