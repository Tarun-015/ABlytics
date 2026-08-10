"""
Per-metric and overall verdicts.

Runs the full statistical pipeline (z-test -> CI -> effect size -> power)
for every significance-eligible metric that was selected, applies the
Bonferroni-adjusted alpha from multiple_testing.py, and rolls the per-metric
verdicts into one overall experiment verdict.

Overall verdict logic is deliberately conservative:
  - "Variant B wins"   -> at least one significance-eligible metric is
                          significant AND improved, and none of the
                          significance-eligible metrics are significant
                          AND worse.
  - "Variant A wins"   -> mirror case.
  - "Mixed results"    -> significant improvements on some metrics and
                          significant regressions on others.
  - "No significant difference" -> nothing reached significance.
  - "Inconclusive — no testable metrics" -> none of the selected metrics
                          support a significance test (e.g. only Revenue Per
                          Session or Average Session Duration were selected).
"""

from config.constants import METRIC_SPECS
from stats_engine.ztest import two_proportion_ztest
from stats_engine.confidence import confidence_interval_diff
from stats_engine.effect_size import cohens_h
from stats_engine.power import achieved_power
from stats_engine.multiple_testing import bonferroni_correction


def run_statistical_analysis(dataset, alpha: float = 0.05, target_power: float = 0.80) -> dict:
    testable = [m for m in dataset.selected_metrics if METRIC_SPECS.get(m) and METRIC_SPECS[m].supports_significance_test]
    correction = bonferroni_correction(alpha, len(testable))
    adjusted_alpha = correction["adjusted_alpha"]

    per_metric = {}

    for metric_name in dataset.selected_metrics:
        spec = METRIC_SPECS.get(metric_name)
        if spec is None:
            continue

        if not spec.supports_significance_test:
            per_metric[metric_name] = {
                "tested": False,
                "reason": spec.significance_note or "Significance test not applicable to this metric.",
            }
            continue

        if spec.kind == "ratio":
            succ_a, trials_a = dataset.variant_a.get(spec.numerator), dataset.variant_a.get(spec.denominator)
            succ_b, trials_b = dataset.variant_b.get(spec.numerator), dataset.variant_b.get(spec.denominator)
        elif spec.kind == "funnel" and metric_name == "Funnel Completion Rate":
            steps = dataset.funnel_steps
            if not steps or len(steps) < 2:
                per_metric[metric_name] = {"tested": False, "reason": "Funnel steps not configured."}
                continue
            trials_a, succ_a = steps[0].count_a, steps[-1].count_a
            trials_b, succ_b = steps[0].count_b, steps[-1].count_b
        else:
            per_metric[metric_name] = {"tested": False, "reason": "Unsupported metric kind for significance testing."}
            continue

        ztest_result = two_proportion_ztest(succ_a, trials_a, succ_b, trials_b)
        if ztest_result.get("error"):
            per_metric[metric_name] = {"tested": False, "reason": ztest_result["error"]}
            continue

        ci_result = confidence_interval_diff(succ_a, trials_a, succ_b, trials_b)
        effect_result = cohens_h(ztest_result["p_a"], ztest_result["p_b"])
        power_result = achieved_power(ztest_result["p_a"], trials_a, ztest_result["p_b"], trials_b, alpha=adjusted_alpha)

        is_significant = ztest_result["p_value"] < adjusted_alpha
        improved = (ztest_result["p_b"] > ztest_result["p_a"]) if spec.higher_is_better else (ztest_result["p_b"] < ztest_result["p_a"])

        per_metric[metric_name] = {
            "tested": True,
            "z_stat": ztest_result["z_stat"],
            "p_value": ztest_result["p_value"],
            "alpha_used": adjusted_alpha,
            "significant": is_significant,
            "improved": improved if is_significant else None,
            "confidence_interval": ci_result,
            "effect_size": effect_result,
            "power": power_result,
        }

    significant_improvements = [m for m, r in per_metric.items() if r.get("significant") and r.get("improved")]
    significant_regressions = [m for m, r in per_metric.items() if r.get("significant") and r.get("improved") is False]
    any_tested = any(r.get("tested") for r in per_metric.values())

    if not any_tested:
        overall = "Inconclusive — no testable metrics"
        recommendation = (
            "None of the selected metrics support a significance test with the "
            "data provided. Add a proportion-based metric (Conversion Rate, CTR, "
            "Bounce Rate, or New User Rate) to get a statistical verdict."
        )
    elif significant_improvements and not significant_regressions:
        overall = "Variant B wins"
        recommendation = f"Ship Variant B — statistically significant improvement on: {', '.join(significant_improvements)}."
    elif significant_regressions and not significant_improvements:
        overall = "Variant A wins"
        recommendation = f"Keep Variant A — Variant B was statistically significantly worse on: {', '.join(significant_regressions)}."
    elif significant_improvements and significant_regressions:
        overall = "Mixed results"
        recommendation = (
            f"Variant B improved {', '.join(significant_improvements)} but regressed "
            f"{', '.join(significant_regressions)} — this is a trade-off decision, not "
            f"a statistical one. Weigh which metric matters more before shipping."
        )
    else:
        overall = "No significant difference"
        recommendation = (
            "No metric reached statistical significance at the corrected threshold. "
            "This does not prove the variants perform identically — check the "
            "required-sample-size figures below to see if the test was adequately "
            "powered before concluding 'no effect'."
        )

    return {
        "per_metric": per_metric,
        "multiple_testing_correction": correction,
        "overall_verdict": overall,
        "recommendation": recommendation,
        "significant_improvements": significant_improvements,
        "significant_regressions": significant_regressions,
    }
