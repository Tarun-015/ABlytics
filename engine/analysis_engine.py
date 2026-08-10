"""
Orchestrates the full pipeline: metrics -> comparison -> funnel -> statistics
-> decision.

Previously this also called purchase_metrics() unconditionally and bundled
its permanent "{available: False}" stub into the result as if it were a real
computed output. It's been dropped from the pipeline — a stub that always
returns "not available" doesn't belong wired into the engine's contract; it
belongs in the roadmap, not in the result dict the dashboard renders.
"""

from analytics.metrics import calculate_metrics
from analytics.comparison import compare_variants
from analytics.funnel import calculate_funnel
from stats_engine.decision import run_statistical_analysis
from config.constants import METRIC_SPECS, DEFAULT_ALPHA, DEFAULT_TARGET_POWER


class AnalysisEngine:

    def __init__(self, dataset, alpha: float = DEFAULT_ALPHA, target_power: float = DEFAULT_TARGET_POWER):
        self.dataset = dataset
        self.alpha = alpha
        self.target_power = target_power

    def run(self) -> dict:
        metrics = calculate_metrics(self.dataset)

        comparison = compare_variants(metrics)

        funnel = None
        if any(METRIC_SPECS[m].kind == "funnel" for m in self.dataset.selected_metrics if m in METRIC_SPECS):
            funnel = calculate_funnel(self.dataset)

        statistics_result = run_statistical_analysis(
            self.dataset, alpha=self.alpha, target_power=self.target_power
        )

        return {
            "dataset": self.dataset,
            "metrics": metrics,
            "comparison": comparison,
            "funnel": funnel,
            "statistics": statistics_result,
        }
