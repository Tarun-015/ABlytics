import streamlit as st

from config.constants import METRIC_SPECS


def show_statistics_panel(statistics_result: dict):
    st.markdown("### Statistical Results")

    correction = statistics_result["multiple_testing_correction"]
    if correction.get("note"):
        st.info(correction["note"])

    per_metric = statistics_result["per_metric"]

    for metric_name, result in per_metric.items():
        spec = METRIC_SPECS.get(metric_name)
        with st.container(border=True):
            st.markdown(f"**{metric_name}**")

            if not result.get("tested"):
                st.caption(result.get("reason", "Not tested."))
                continue

            sig = result["significant"]
            badge = "🟢 Significant" if sig else "⚪ Not significant"
            st.write(f"{badge} — p = {result['p_value']:.4f} (α = {result['alpha_used']:.4f})")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.caption("Z-statistic")
                st.write(f"{result['z_stat']:.3f}")
            with c2:
                ci = result["confidence_interval"]
                st.caption(f"{int(ci['confidence_level'] * 100)}% CI (diff)")
                if ci["lower"] is not None:
                    st.write(f"[{ci['lower']:+.2%}, {ci['upper']:+.2%}]")
                if ci.get("warning"):
                    st.caption(f"⚠️ {ci['warning']}")
            with c3:
                eff = result["effect_size"]
                st.caption("Effect size (Cohen's h)")
                if eff["h"] is not None:
                    st.write(f"{eff['h']:.3f} ({eff['magnitude']})")

            power = result.get("power", {})
            if power.get("power") is not None:
                st.caption(f"Post-hoc power: {power['power']:.2%} — {power['note']}")
