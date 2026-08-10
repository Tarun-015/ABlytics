"""JSON export of the full analysis result (metrics, comparison, statistics,
verdict). Dataclass instances (StandardDataset, VariantData, FunnelStep)
aren't JSON-serializable by default, so this walks the result and converts
them explicitly rather than crashing on json.dumps()."""

import json
import dataclasses


def _to_jsonable(obj):
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {k: _to_jsonable(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_jsonable(v) for v in obj]
    return obj


def export_json(results: dict) -> bytes:
    payload = _to_jsonable(results)
    return json.dumps(payload, indent=2, default=str).encode("utf-8")
