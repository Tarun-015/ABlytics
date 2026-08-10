"""
Two-proportion z-test for a single ratio metric (e.g. Conversion Rate, CTR,
Bounce Rate, New User Rate — anything expressible as successes/trials).

Design decisions, stated explicitly (the original spec listed "Z-test" as a
bullet point with no statement of which variance estimate or which tail is
used — that ambiguity is exactly what produces a dashboard where the CI and
the significance decision silently disagree with each other):

  - HYPOTHESIS TEST uses the POOLED proportion. H0: p_A = p_B, so under the
    null both variants are assumed to share one true rate — the standard
    error should reflect that shared assumption, not each variant's own
    (different) observed rate. This is the textbook-correct choice for a
    two-proportion z-test used to accept/reject H0.
  - The CONFIDENCE INTERVAL (statistics/confidence.py) uses the UNPOOLED
    standard error instead, because a CI describes the plausible range of
    the *actual* difference assuming no such equality — pooling there would
    misstate the CI's width. This is why ztest.py and confidence.py compute
    two different standard errors on purpose; that's correct, not a bug.
  - TWO-SIDED by default. A one-sided test would be appropriate if you can
    only ever act on "B beat A" and would treat "B worse than A" identically
    to "no difference" — most product decisions don't actually work that
    way (a worse variant is still actionable information), so two-sided is
    the safer default. `alternative="larger"` is available for callers who
    deliberately want one-sided.
"""

import math
from scipy.stats import norm


def two_proportion_ztest(
    successes_a: float, trials_a: float,
    successes_b: float, trials_b: float,
    alternative: str = "two-sided",
) -> dict:
    if trials_a <= 0 or trials_b <= 0:
        return {"z_stat": None, "p_value": None, "significant": None,
                "error": "Both variants need at least 1 trial (visitor/impression/session)."}

    p_a = successes_a / trials_a
    p_b = successes_b / trials_b

    pooled_p = (successes_a + successes_b) / (trials_a + trials_b)

    se_pooled = math.sqrt(pooled_p * (1 - pooled_p) * (1 / trials_a + 1 / trials_b))

    if se_pooled == 0:
        return {"z_stat": None, "p_value": None, "significant": None,
                "error": "Standard error is 0 (identical, extreme, or degenerate rates)."}

    z_stat = (p_b - p_a) / se_pooled

    if alternative == "two-sided":
        p_value = 2 * (1 - norm.cdf(abs(z_stat)))
    elif alternative == "larger":  # H1: p_b > p_a
        p_value = 1 - norm.cdf(z_stat)
    elif alternative == "smaller":  # H1: p_b < p_a
        p_value = norm.cdf(z_stat)
    else:
        raise ValueError("alternative must be 'two-sided', 'larger', or 'smaller'")

    return {
        "z_stat": z_stat,
        "p_value": p_value,
        "p_a": p_a,
        "p_b": p_b,
        "pooled_p": pooled_p,
        "se_pooled": se_pooled,
        "alternative": alternative,
        "error": None,
    }
