"""
Standard Data Model.

This is the contract every analysis mode (Manual, Historical GA4, True A/B
GA4) must produce, and the only shape the Analytics Engine and Statistics
Engine are allowed to consume. Previously this "standard model" existed only
as an implicit, unvalidated dict — three different producers could each
drift from it silently and the failure would only surface as a KeyError deep
inside calculate_metrics(). Making it an explicit dataclass means:

  1. A mode that doesn't conform fails loudly and immediately (TypeError on
     construction), not later inside the engine.
  2. The engine, validator, and dashboard can all type-check against one
     definition instead of trusting a dict shape by convention.
  3. Adding a new source (e.g. a future CSV import mode) only requires
     mapping its raw output into a StandardDataset — nothing downstream
     changes.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FunnelStep:
    name: str
    count_a: int
    count_b: int


@dataclass
class VariantData:
    """Raw counts/values for one variant. Only the fields relevant to the
    selected metrics need to be populated; everything else defaults to 0."""
    visitors: int = 0
    conversions: int = 0
    impressions: int = 0
    clicks: int = 0
    sessions: int = 0
    bounces: int = 0
    revenue: float = 0.0
    users: int = 0
    new_users: int = 0
    session_duration: float = 0.0

    def get(self, field_name: str, default=0):
        return getattr(self, field_name, default)


@dataclass
class StandardDataset:
    """The one shape every analysis mode must normalize into."""
    source: str  # "manual" | "historical" | "true_ab"
    selected_metrics: list[str]
    variant_a: VariantData
    variant_b: VariantData
    funnel_steps: list[FunnelStep] = field(default_factory=list)
    project_name: str = ""
    variant_a_label: str = "Variant A"
    variant_b_label: str = "Variant B"
    meta: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "StandardDataset":
        """Builds a StandardDataset from the dict shape the Streamlit config
        pages produce. Raises TypeError/KeyError immediately if the producer
        drifted from the contract, instead of failing silently downstream."""
        va = d.get("variant_a", {}) or {}
        vb = d.get("variant_b", {}) or {}
        steps = [
            FunnelStep(**s) if not isinstance(s, FunnelStep) else s
            for s in d.get("funnel_steps", [])
        ]
        return cls(
            source=d.get("source", "manual"),
            selected_metrics=list(d.get("selected_metrics", [])),
            variant_a=VariantData(**va) if not isinstance(va, VariantData) else va,
            variant_b=VariantData(**vb) if not isinstance(vb, VariantData) else vb,
            funnel_steps=steps,
            project_name=d.get("project_name", ""),
            variant_a_label=d.get("variant_a_label", "Variant A"),
            variant_b_label=d.get("variant_b_label", "Variant B"),
            meta={k: v for k, v in d.items() if k not in {
                "source", "selected_metrics", "variant_a", "variant_b",
                "funnel_steps", "project_name", "variant_a_label", "variant_b_label",
            }},
        )
