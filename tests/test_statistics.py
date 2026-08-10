"""
Unit tests for the statistics engine, cross-checked against scipy/statsmodels
reference implementations. This is the test suite the original project had
zero of — for a platform whose entire value proposition is "trust our
statistical verdict," this is the minimum bar before that claim is credible.

Run with: pytest tests/test_statistics.py -v
"""

import math
import pytest
from scipy.stats import norm
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

from stats_engine.ztest import two_proportion_ztest
from stats_engine.confidence import confidence_interval_diff
from stats_engine.effect_size import cohens_h
from stats_engine.power import achieved_power, required_sample_size
from stats_engine.multiple_testing import bonferroni_correction
from stats_engine.decision import run_statistical_analysis

from core.schema import StandardDataset, VariantData


# ---------------------------------------------------------------------------
# Z-test: matches statsmodels' proportions_ztest (which pools by default)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("succ_a,n_a,succ_b,n_b", [
    (250, 5000, 300, 5000),
    (1800, 4500, 1600, 4600),   # bounce-rate-shaped numbers
    (10, 100, 20, 100),         # larger effect, small n
    (4999, 5000, 5000, 5000),   # near-boundary rates
])
def test_ztest_matches_statsmodels(succ_a, n_a, succ_b, n_b):
    result = two_proportion_ztest(succ_a, n_a, succ_b, n_b)

    ref_z, ref_p = proportions_ztest(
        count=[succ_a, succ_b], nobs=[n_a, n_b], alternative="two-sided"
    )

    # statsmodels' z is (group1 - group2); ours is (b - a) = -(group1-group2)
    # when count/nobs order is [a, b] vs [b, a] respectively -- check sign-
    # invariant quantities instead of raw z to avoid a false failure from
    # convention differences.
    assert math.isclose(abs(result["z_stat"]), abs(ref_z), rel_tol=1e-6)
    assert math.isclose(result["p_value"], ref_p, rel_tol=1e-6)


def test_ztest_significant_case_is_flagged_correctly():
    # Large, clearly significant lift
    result = two_proportion_ztest(100, 1000, 200, 1000)
    assert result["p_value"] < 0.001
    assert result["p_b"] > result["p_a"]


def test_ztest_handles_zero_trials_without_crashing():
    result = two_proportion_ztest(0, 0, 10, 100)
    assert result["z_stat"] is None
    assert result["error"] is not None


def test_ztest_one_sided_alternative():
    result_two = two_proportion_ztest(250, 5000, 300, 5000, alternative="two-sided")
    result_larger = two_proportion_ztest(250, 5000, 300, 5000, alternative="larger")
    # one-sided p-value in the correct direction should be roughly half the two-sided value
    assert math.isclose(result_larger["p_value"], result_two["p_value"] / 2, rel_tol=1e-6)


# ---------------------------------------------------------------------------
# Confidence interval: matches a manually-computed Wald interval on the diff
# ---------------------------------------------------------------------------

def test_confidence_interval_matches_manual_wald_calc():
    succ_a, n_a, succ_b, n_b = 250, 5000, 300, 5000
    p_a, p_b = succ_a / n_a, succ_b / n_b

    se = math.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    z = norm.ppf(0.975)
    expected_lower = (p_b - p_a) - z * se
    expected_upper = (p_b - p_a) + z * se

    result = confidence_interval_diff(succ_a, n_a, succ_b, n_b, confidence_level=0.95)

    assert math.isclose(result["lower"], expected_lower, rel_tol=1e-9)
    assert math.isclose(result["upper"], expected_upper, rel_tol=1e-9)


def test_confidence_interval_flags_small_sample():
    result = confidence_interval_diff(1, 20, 2, 20)  # expected successes << 5
    assert result["warning"] is not None


def test_confidence_interval_consistent_with_significance():
    # If the z-test says significant at alpha=0.05, the 95% CI of the diff
    # should not contain 0. This is exactly the kind of dashboard-level
    # inconsistency the original design (pooled test, unspecified CI method)
    # risked producing.
    succ_a, n_a, succ_b, n_b = 100, 1000, 200, 1000
    z_result = two_proportion_ztest(succ_a, n_a, succ_b, n_b)
    ci_result = confidence_interval_diff(succ_a, n_a, succ_b, n_b)

    assert z_result["p_value"] < 0.05
    assert not (ci_result["lower"] <= 0 <= ci_result["upper"])


# ---------------------------------------------------------------------------
# Effect size (Cohen's h)
# ---------------------------------------------------------------------------

def test_cohens_h_identical_rates_is_zero():
    result = cohens_h(0.05, 0.05)
    assert math.isclose(result["h"], 0.0, abs_tol=1e-9)
    assert result["magnitude"] == "negligible"


def test_cohens_h_known_reference_value():
    # h between 0.10 and 0.20 is a textbook example, ~0.2838 (small-to-medium)
    result = cohens_h(0.10, 0.20)
    expected = 2 * math.asin(math.sqrt(0.20)) - 2 * math.asin(math.sqrt(0.10))
    assert math.isclose(result["h"], expected, rel_tol=1e-9)


def test_cohens_h_rejects_out_of_range_inputs():
    result = cohens_h(1.5, 0.2)
    assert result["error"] is not None


# ---------------------------------------------------------------------------
# Power
# ---------------------------------------------------------------------------

def test_achieved_power_is_between_0_and_1():
    result = achieved_power(0.05, 5000, 0.06, 5000, alpha=0.05)
    assert 0 <= result["power"] <= 1


def test_required_sample_size_increases_as_mde_shrinks():
    big_effect = required_sample_size(baseline_rate=0.05, minimum_detectable_effect=0.02)
    small_effect = required_sample_size(baseline_rate=0.05, minimum_detectable_effect=0.005)
    assert small_effect["n_per_variant"] > big_effect["n_per_variant"]


def test_required_sample_size_rejects_invalid_rates():
    result = required_sample_size(baseline_rate=1.5, minimum_detectable_effect=0.01)
    assert result["error"] is not None


# ---------------------------------------------------------------------------
# Multiple testing correction
# ---------------------------------------------------------------------------

def test_bonferroni_correction_divides_alpha():
    result = bonferroni_correction(0.05, 4)
    assert math.isclose(result["adjusted_alpha"], 0.0125, rel_tol=1e-9)
    assert result["note"] is not None


def test_bonferroni_correction_no_adjustment_for_single_test():
    result = bonferroni_correction(0.05, 1)
    assert math.isclose(result["adjusted_alpha"], 0.05, rel_tol=1e-9)
    assert result["note"] is None


# ---------------------------------------------------------------------------
# End-to-end decision engine
# ---------------------------------------------------------------------------

def _dataset(metrics, va, vb, funnel_steps=None):
    from core.schema import FunnelStep
    return StandardDataset(
        source="manual",
        selected_metrics=metrics,
        variant_a=VariantData(**va),
        variant_b=VariantData(**vb),
        funnel_steps=[FunnelStep(**s) for s in (funnel_steps or [])],
    )


def test_decision_engine_clear_win_for_b():
    dataset = _dataset(
        ["Conversion Rate"],
        {"visitors": 5000, "conversions": 250},
        {"visitors": 5000, "conversions": 400},
    )
    result = run_statistical_analysis(dataset)
    assert result["overall_verdict"] == "Variant B wins"
    assert "Conversion Rate" in result["significant_improvements"]


def test_decision_engine_no_difference():
    dataset = _dataset(
        ["Conversion Rate"],
        {"visitors": 5000, "conversions": 250},
        {"visitors": 5000, "conversions": 253},
    )
    result = run_statistical_analysis(dataset)
    assert result["overall_verdict"] == "No significant difference"


def test_decision_engine_non_testable_metric_only():
    dataset = _dataset(
        ["Revenue Per Session"],
        {"sessions": 4500, "revenue": 6500.0},
        {"sessions": 4600, "revenue": 7800.0},
    )
    result = run_statistical_analysis(dataset)
    assert result["overall_verdict"] == "Inconclusive — no testable metrics"


def test_decision_engine_mixed_results():
    dataset = _dataset(
        ["Conversion Rate", "Bounce Rate"],
        {"visitors": 5000, "conversions": 250, "sessions": 5000, "bounces": 1000},
        {"visitors": 5000, "conversions": 400, "sessions": 5000, "bounces": 1600},
    )
    result = run_statistical_analysis(dataset)
    # B has a much higher conversion rate (significant improvement) AND a
    # much higher bounce rate (significant regression, since lower is better)
    assert result["overall_verdict"] == "Mixed results"


def test_decision_engine_applies_bonferroni_across_selected_metrics():
    dataset = _dataset(
        ["Conversion Rate", "CTR", "Bounce Rate"],
        {"visitors": 5000, "conversions": 250, "impressions": 5000, "clicks": 800, "sessions": 5000, "bounces": 1000},
        {"visitors": 5000, "conversions": 253, "impressions": 5000, "clicks": 803, "sessions": 5000, "bounces": 1003},
    )
    result = run_statistical_analysis(dataset, alpha=0.05)
    assert result["multiple_testing_correction"]["num_tests"] == 3
    assert math.isclose(result["multiple_testing_correction"]["adjusted_alpha"], 0.05 / 3, rel_tol=1e-9)
