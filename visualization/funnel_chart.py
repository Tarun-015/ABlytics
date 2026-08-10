import streamlit as st
import pandas as pd


def show_funnel_chart(funnel_result: dict):
    if not funnel_result:
        return

    st.markdown("### Funnel")

    va, vb = funnel_result["variant_a"], funnel_result["variant_b"]
    if va.get("completion_rate") is None:
        st.caption("Funnel steps not configured.")
        return

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Variant A completion rate", f"{va['completion_rate']:.1f}%")
        for step in va["steps"]:
            st.caption(f"{step['from']} → {step['to']}: {step['dropoff_rate']:.1f}% drop-off")
    with c2:
        st.metric("Variant B completion rate", f"{vb['completion_rate']:.1f}%")
        for step in vb["steps"]:
            st.caption(f"{step['from']} → {step['to']}: {step['dropoff_rate']:.1f}% drop-off")
