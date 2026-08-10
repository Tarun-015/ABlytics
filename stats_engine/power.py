"""
Statistical power for a two-proportion comparison.

Two genuinely different questions live here, and conflating them is a
common error in A/B testing tools (the original spec's "Statistical Power"
bullet didn't distinguish between them):

  1. ACHIEVED / POST-HOC POWER — "given the sample size and effect I
     observed, what was my power to detect it?" This number is a
     deterministic (monotonic) function of the p-value: a significant
     result always shows "high" post-hoc power, and a non-significant one
     always shows "low" post-hoc power. It provides no information beyond
     what the p-value already told you. It's included here ONLY as a
     descriptive, clearly-labeled number — never as something the decision
     engine reasons about — precisely because treating it as meaningful
     evidence is a known statistical error.

  2. REQUIRED SAMPLE SIZE — "given a baseline rate and the smallest lift I
     care about detecting (MDE), how many visitors per variant do I need?"
     This is the number that's actually decision-relevant: it tells you,
     BEFORE or AFTER running the test, whether your sample was even large
     enough to have a fair chance of detecting the effect size you cared
     about. A non-significant result next to "your test was underpowered
     to detect a 2pp lift" is a materially different conclusion than a
     non-significant result next to "you had 95% power to detect a 2pp
     lift and still saw nothing" — the former means "inconclusive", the
     latter means "genuinely no meaningful difference".

Both are computed via statsmodels' NormalIndPower, which implements the
standard normal-approximation power formula for two-proportion tests —
reimplementing it by hand risks a subtle sign/tail error that's easy to get
wrong and hard to notice. See tests/test_statistics.py for a cross-check
against statsmodels' own reference values.
"""

from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

_power_solver = NormalIndPower()


def achieved_power(p_a: float, n_a: float, p_b: float, n_b: float, alpha: float = 0.05) -> dict:
    if n_a <= 0 or n_b <= 0:
        return {"power": None, "error": "Both variants need at least 1 trial."}

    effect_size = proportion_effectsize(p_b, p_a)
    ratio = n_b / n_a

    power = _power_solver.power(
        effect_size=abs(effect_size), nobs1=n_a, alpha=alpha, ratio=ratio,
    )

    return {
        "power": power,
        "note": (
            "Post-hoc power is descriptive only — it is mathematically "
            "determined by the p-value and adds no independent evidence. "
            "Use 'required sample size' below to judge whether this test "
            "was adequately powered."
        ),
        "error": None,
    }


def required_sample_size(
    baseline_rate: float, minimum_detectable_effect: float,
    alpha: float = 0.05, target_power: float = 0.80,
) -> dict:
    """baseline_rate and minimum_detectable_effect are both in [0, 1]
    (e.g. baseline_rate=0.05, mde=0.01 -> detect a move from 5% to 6%)."""
    if not (0 < baseline_rate < 1):
        return {"n_per_variant": None, "error": "baseline_rate must be between 0 and 1."}

    target_rate = baseline_rate + minimum_detectable_effect
    if not (0 < target_rate < 1):
        return {"n_per_variant": None, "error": "baseline_rate + MDE must be between 0 and 1."}

    effect_size = proportion_effectsize(target_rate, baseline_rate)

    n = _power_solver.solve_power(
        effect_size=abs(effect_size), alpha=alpha, power=target_power, ratio=1.0,
    )

    return {
        "n_per_variant": int(round(n)),
        "baseline_rate": baseline_rate,
        "target_rate": target_rate,
        "alpha": alpha,
        "target_power": target_power,
        "error": None,
    }
