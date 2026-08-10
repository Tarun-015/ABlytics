"""
Multiple-comparisons correction.

The original spec let a user select several metrics at once and implied
each gets its own independent significance test — that inflates the
experiment-wide false-positive rate well past the nominal 5% (with 5
independent tests at alpha=0.05, the chance of at least one false positive
is ~23%, not 5%). This module is the fix: it's called once per analysis run
with however many significance-eligible metrics were selected, and returns
the per-test alpha every individual z-test should actually use.

Bonferroni is used because it's simple, conservative, and defensible for the
small number of tests (typically 1-5) this platform runs per experiment.
Benjamini-Hochberg (controlling false discovery rate rather than family-wise
error) would be less conservative and is worth adding if this platform ever
needs to run many simultaneous metric comparisons — noted here rather than
silently deferred.
"""


def bonferroni_correction(alpha: float, num_tests: int) -> dict:
    if num_tests <= 0:
        return {"adjusted_alpha": alpha, "num_tests": 0}

    adjusted = alpha / num_tests

    return {
        "adjusted_alpha": adjusted,
        "original_alpha": alpha,
        "num_tests": num_tests,
        "note": (
            f"{num_tests} metric(s) were tested simultaneously, so the "
            f"significance threshold was tightened from {alpha} to "
            f"{adjusted:.4f} per metric (Bonferroni correction) to control "
            f"the experiment-wide false-positive rate."
        ) if num_tests > 1 else None,
    }
