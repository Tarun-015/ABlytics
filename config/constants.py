"""
Central metric registry.

Every metric ABlytics knows about is defined ONCE here: how it's computed,
what raw fields it needs, how it's labeled in the UI, whether it's a true
binomial proportion (and therefore eligible for a two-proportion z-test),
and its default demo values.

This is the single source of truth that analytics/metrics.py,
experiments/manual.py, and validation/validator.py all read from — instead
of each file re-implementing the same per-metric branching independently
(which is what this file replaced).
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class MetricSpec:
    name: str
    kind: str  # "ratio" | "direct" | "funnel"
    is_percentage: bool
    higher_is_better: bool
    supports_significance_test: bool
    description: str

    # "ratio" kind fields (e.g. conversions / visitors)
    numerator: Optional[str] = None
    denominator: Optional[str] = None
    numerator_label: Optional[str] = None
    denominator_label: Optional[str] = None
    numerator_is_float: bool = False
    numerator_min: float = 0.0
    denominator_min: float = 1.0

    # "direct" kind fields (e.g. average session duration)
    field_name: Optional[str] = None
    field_label: Optional[str] = None

    default_a: tuple = field(default_factory=tuple)
    default_b: tuple = field(default_factory=tuple)

    significance_note: Optional[str] = None


METRIC_SPECS: dict[str, MetricSpec] = {

    "Conversion Rate": MetricSpec(
        name="Conversion Rate",
        kind="ratio",
        numerator="conversions", denominator="visitors",
        numerator_label="Conversions", denominator_label="Visitors",
        is_percentage=True, higher_is_better=True,
        supports_significance_test=True,
        description="Share of visitors who completed the target action.",
        default_a=(5000, 250), default_b=(5000, 300),
    ),

    "CTR": MetricSpec(
        name="CTR",
        kind="ratio",
        numerator="clicks", denominator="impressions",
        numerator_label="Clicks", denominator_label="Impressions",
        is_percentage=True, higher_is_better=True,
        supports_significance_test=True,
        description="Share of impressions that resulted in a click.",
        default_a=(5000, 800), default_b=(5000, 900),
    ),

    "Bounce Rate": MetricSpec(
        name="Bounce Rate",
        kind="ratio",
        numerator="bounces", denominator="sessions",
        numerator_label="Bounces", denominator_label="Sessions",
        is_percentage=True, higher_is_better=False,
        supports_significance_test=True,
        description="Share of sessions with no meaningful interaction.",
        default_a=(4500, 1800), default_b=(4600, 1600),
    ),

    "New User Rate": MetricSpec(
        name="New User Rate",
        kind="ratio",
        numerator="new_users", denominator="users",
        numerator_label="New Users", denominator_label="Users",
        is_percentage=True, higher_is_better=True,
        supports_significance_test=True,
        description="Share of users who were first-time visitors.",
        default_a=(4200, 1600), default_b=(4300, 1800),
    ),

    "Revenue Per Session": MetricSpec(
        name="Revenue Per Session",
        kind="ratio",
        numerator="revenue", denominator="sessions",
        numerator_label="Revenue", denominator_label="Sessions",
        numerator_is_float=True,
        is_percentage=False, higher_is_better=True,
        supports_significance_test=False,
        description="Average revenue generated per session.",
        default_a=(4500, 6500.0), default_b=(4600, 7800.0),
        significance_note=(
            "Revenue is continuous, not a count of successes/failures, so a "
            "two-proportion z-test does not apply. A valid significance test "
            "needs per-session revenue values (for a t-test) rather than a "
            "single aggregate total. Shown as descriptive comparison only."
        ),
    ),

    "Average Session Duration": MetricSpec(
        name="Average Session Duration",
        kind="direct",
        field_name="session_duration", field_label="Average Session Duration (seconds)",
        is_percentage=False, higher_is_better=True,
        supports_significance_test=False,
        description="Average time users spent per session, in seconds.",
        default_a=(142,), default_b=(156,),
        significance_note=(
            "This is already an aggregate average with no underlying sample "
            "size or variance provided, so no significance test can be run "
            "on it here. Shown as descriptive comparison only."
        ),
    ),

    "Funnel Completion Rate": MetricSpec(
        name="Funnel Completion Rate",
        kind="funnel",
        is_percentage=True, higher_is_better=True,
        supports_significance_test=True,
        description="Share of users at the first funnel step who reached the last step.",
    ),

    "Drop-off Rate": MetricSpec(
        name="Drop-off Rate",
        kind="funnel",
        is_percentage=True, higher_is_better=False,
        supports_significance_test=False,
        description="Largest single-step drop-off percentage within the funnel.",
        significance_note=(
            "Drop-off rate is derived per funnel step rather than as a single "
            "proportion, so it is shown as descriptive comparison only."
        ),
    ),
}

PRIMARY_METRICS = list(METRIC_SPECS.keys())

RATIO_METRICS = [m for m, s in METRIC_SPECS.items() if s.kind == "ratio"]
FUNNEL_METRICS = [m for m, s in METRIC_SPECS.items() if s.kind == "funnel"]
SIGNIFICANCE_ELIGIBLE_METRICS = [m for m, s in METRIC_SPECS.items() if s.supports_significance_test]

DEFAULT_ALPHA = 0.05
DEFAULT_CONFIDENCE_LEVEL = 0.95
DEFAULT_TARGET_POWER = 0.80
