import streamlit as st

from config.constants import METRIC_SPECS


def _fmt(value, is_percentage: bool):
    if value is None:
        return "—"
    return f"{value:.2f}%" if is_percentage else f"{value:,.2f}"


def show_metric_cards(comparison: list[dict]):
    st.markdown("### Metric Comparison")
    cols = st.columns(min(len(comparison), 4) or 1)

    for i, row in enumerate(comparison):
        spec = METRIC_SPECS.get(row["metric"])
        is_pct = spec.is_percentage if spec else False
        with cols[i % len(cols)]:
            with st.container(border=True):
                st.caption(row["metric"])
                st.markdown(f"**B: {_fmt(row['variant_b'], is_pct)}**")
                st.caption(f"A: {_fmt(row['variant_a'], is_pct)}")
                if row["percentage_change"] is not None:
                    arrow = "▲" if row["improved"] else ("▼" if row["improved"] is False else "•")
                    color = "green" if row["improved"] else ("red" if row["improved"] is False else "gray")
                    st.markdown(f":{color}[{arrow} {row['percentage_change']:+.1f}%]")
