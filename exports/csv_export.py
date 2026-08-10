"""CSV export of the variant comparison table — the flat, spreadsheet-ready
subset of the results (not the full nested statistics detail, which doesn't
fit a flat table well; that's what JSON/PDF export are for)."""

import csv
import io


def export_csv(comparison: list[dict]) -> bytes:
    buffer = io.StringIO()
    fieldnames = ["metric", "variant_a", "variant_b", "difference", "percentage_change", "improved"]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in comparison:
        writer.writerow({k: row.get(k) for k in fieldnames})
    return buffer.getvalue().encode("utf-8")
