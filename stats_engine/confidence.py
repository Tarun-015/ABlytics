"""
Confidence interval for the difference in proportions (p_B - p_A).

Uses the UNPOOLED standard error deliberately — see the docstring in
ztest.py for why this differs from the SE used in the hypothesis test.
Uses a Wald interval (the standard asymptotic-normal CI). Wald intervals are
known to perform poorly for small samples or rates near 0%/100% — the
Wilson score interval is more robust in those regions but isn't implemented
here; flagged as a known limitation rather than silently shipping something
that looks precise but isn't, for small/extreme samples.
"""

import math
from scipy.stats import norm


def confidence_interval_diff(
    successes_a: float, trials_a: float,
    successes_b: float, trials_b: float,
    confidence_level: float = 0.95,
) -> dict:
    if trials_a <= 0 or trials_b <= 0:
        return {"lower": None, "upper": None, "error": "Both variants need at least 1 trial."}

    p_a = successes_a / trials_a
    p_b = successes_b / trials_b
    diff = p_b - p_a

    se_unpooled = math.sqrt(
        (p_a * (1 - p_a) / trials_a) + (p_b * (1 - p_b) / trials_b)
    )

    alpha = 1 - confidence_level
    z_crit = norm.ppf(1 - alpha / 2)

    margin = z_crit * se_unpooled

    small_sample_warning = None
    min_expected = min(trials_a * p_a, trials_a * (1 - p_a), trials_b * p_b, trials_b * (1 - p_b))
    if min_expected < 5:
        small_sample_warning = (
            "Sample size is small relative to the observed rate (fewer than 5 "
            "expected successes/failures in one group). The normal-approximation "
            "interval may be unreliable here."
        )

    return {
        "diff": diff,
        "lower": diff - margin,
        "upper": diff + margin,
        "se_unpooled": se_unpooled,
        "confidence_level": confidence_level,
        "warning": small_sample_warning,
        "error": None,
    }
