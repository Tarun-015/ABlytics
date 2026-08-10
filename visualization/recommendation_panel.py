import streamlit as st

from stats_engine.power import required_sample_size


def show_recommendation_panel(statistics_result: dict, dataset):
    st.markdown("### Recommendation")

    with st.container(border=True):
        st.write(statistics_result["recommendation"])

        if statistics_result["overall_verdict"] == "No significant difference":
            st.divider()
            st.caption("Was this test adequately powered? Estimate required sample size:")
            c1, c2, c3 = st.columns(3)
            with c1:
                baseline = st.number_input("Baseline rate (%)", min_value=0.1, max_value=99.0, value=5.0, key="rec_baseline") / 100
            with c2:
                mde = st.number_input("Minimum detectable lift (pp)", min_value=0.1, max_value=50.0, value=1.0, key="rec_mde") / 100
            with c3:
                target_power = st.slider("Target power", 0.5, 0.99, 0.80, key="rec_power")

            result = required_sample_size(baseline, mde, target_power=target_power)
            if result.get("error"):
                st.caption(result["error"])
            else:
                st.write(
                    f"You'd need roughly **{result['n_per_variant']:,} visitors per variant** "
                    f"to reliably detect a move from {baseline:.1%} to {result['target_rate']:.1%} "
                    f"at {target_power:.0%} power."
                )
