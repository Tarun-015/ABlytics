import streamlit as st
import pandas as pd

from config.constants import METRIC_SPECS


def show_comparison_table(comparison: list[dict]):
    st.markdown("### Variant Comparison")

    rows = []
    for row in comparison:
        spec = METRIC_SPECS.get(row["metric"])
        is_pct = spec.is_percentage if spec else False
        suffix = "%" if is_pct else ""
        rows.append({
            "Metric": row["metric"],
            "Variant A": f"{row['variant_a']:.2f}{suffix}" if row["variant_a"] is not None else "—",
            "Variant B": f"{row['variant_b']:.2f}{suffix}" if row["variant_b"] is not None else "—",
            "Difference": f"{row['difference']:+.2f}{suffix}" if row["difference"] is not None else "—",
            "% Change": f"{row['percentage_change']:+.1f}%" if row["percentage_change"] is not None else "—",
            "Direction": "Improved" if row["improved"] else ("Declined" if row["improved"] is False else "—"),
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
