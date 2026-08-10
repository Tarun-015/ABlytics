"""One-page PDF summary: verdict, recommendation, and the metric comparison
table. Uses reportlab (already in requirements.txt)."""

import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def export_pdf(project_name: str, statistics_result: dict, comparison: list[dict]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"ABlytics Experiment Report — {project_name or 'Untitled'}", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Verdict: {statistics_result['overall_verdict']}", styles["Heading2"]))
    story.append(Paragraph(statistics_result["recommendation"], styles["BodyText"]))
    story.append(Spacer(1, 12))

    table_data = [["Metric", "Variant A", "Variant B", "% Change", "Improved"]]
    for row in comparison:
        table_data.append([
            row["metric"],
            f"{row['variant_a']:.2f}" if row["variant_a"] is not None else "—",
            f"{row['variant_b']:.2f}" if row["variant_b"] is not None else "—",
            f"{row['percentage_change']:.1f}%" if row["percentage_change"] is not None else "—",
            "Yes" if row["improved"] else ("No" if row["improved"] is False else "—"),
        ])

    table = Table(table_data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
    ]))
    story.append(table)

    doc.build(story)
    return buffer.getvalue()
