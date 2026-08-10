"""
Effect size for two proportions: Cohen's h.

Cohen's h exists specifically because a raw percentage-point difference
isn't comparable across different baseline rates (a 2pp lift on a 5% base
rate is a much bigger relative change than a 2pp lift on a 50% base rate).
It applies the arcsine variance-stabilizing transform to both proportions
before differencing, which is why it's the standard effect size for
proportions rather than Cohen's d (which is for continuous means).

This matters because p-values alone don't tell you if a statistically
significant result is *practically* meaningful — with a large enough
sample, a trivial 0.1pp lift can still be "significant" (p < 0.05). Effect
size answers "how big is this, actually", which the significance test
cannot.
"""

import math


def cohens_h(p_a: float, p_b: float) -> dict:
    if not (0 <= p_a <= 1) or not (0 <= p_b <= 1):
        return {"h": None, "magnitude": None, "error": "Proportions must be between 0 and 1."}

    phi_a = 2 * math.asin(math.sqrt(p_a))
    phi_b = 2 * math.asin(math.sqrt(p_b))
    h = phi_b - phi_a

    abs_h = abs(h)
    if abs_h < 0.2:
        magnitude = "negligible"
    elif abs_h < 0.5:
        magnitude = "small"
    elif abs_h < 0.8:
        magnitude = "medium"
    else:
        magnitude = "large"

    return {"h": h, "magnitude": magnitude, "error": None}
