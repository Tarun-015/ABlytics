"""
Real funnel calculation (previously this file just echoed the raw variant
dicts back unchanged and called it a "funnel").

Requires dataset.funnel_steps: an ordered list of FunnelStep(name, count_a,
count_b), first step = entry, last step = conversion. Completion rate =
last-step count / first-step count. Drop-off rate per step = (prev - curr) /
prev; "max_dropoff_rate" is the single worst step, since "Drop-off Rate" as
a platform-level metric needs to collapse a per-step list into one number.
"""


def calculate_funnel(dataset) -> dict:
    steps = dataset.funnel_steps

    if not steps or len(steps) < 2:
        return {
            "variant_a": {"completion_rate": None, "max_dropoff_rate": None, "steps": []},
            "variant_b": {"completion_rate": None, "max_dropoff_rate": None, "steps": []},
        }

    def build(variant_key: str):
        counts = [getattr(s, variant_key) for s in steps]
        first, last = counts[0], counts[-1]

        completion_rate = (last / first * 100) if first else None

        step_drops = []
        max_drop = 0.0
        for i in range(1, len(counts)):
            prev, curr = counts[i - 1], counts[i]
            drop = ((prev - curr) / prev * 100) if prev else 0.0
            step_drops.append({
                "from": steps[i - 1].name,
                "to": steps[i].name,
                "dropoff_rate": drop,
            })
            max_drop = max(max_drop, drop)

        return {
            "completion_rate": completion_rate,
            "max_dropoff_rate": max_drop,
            "steps": step_drops,
        }

    return {
        "variant_a": build("count_a"),
        "variant_b": build("count_b"),
    }
