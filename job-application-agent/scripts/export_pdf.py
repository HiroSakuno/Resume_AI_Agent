#!/usr/bin/env python3
"""
Export Markdown files to PDF using markdown2 + weasyprint.
Falls back to reportlab if weasyprint is unavailable.

Usage:
    python scripts/export_pdf.py <resume.md> <cover_letter.md> <output_dir>
"""

import sys
from pathlib import Path


CSS_STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Calibri&display=swap');

body {
    font-family: "Calibri", "Arial", sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #000000;
    margin: 0;
    padding: 0;
}

@page {
    margin: 0.75in 0.9in;
    size: letter;
}

h1 {
    font-size: 18pt;
    color: #1F297A;
    margin-bottom: 4pt;
    border-bottom: 1px solid #1F297A;
    padding-bottom: 4pt;
}

h2 {
    font-size: 13pt;
    color: #1F297A;
    margin-top: 12pt;
    margin-bottom: 4pt;
    border-bottom: 0.5px solid #cccccc;
}

h3 {
    font-size: 11pt;
    font-weight: bold;
    margin-top: 8pt;
    margin-bottom: 2pt;
}

ul {
    margin-top: 4pt;
    margin-bottom: 4pt;
    padding-left: 18pt;
}

li {
    margin-bottom: 3pt;
}

p {
    margin-bottom: 6pt;
}

hr {
    border: none;
    border-top: 1px solid #cccccc;
    margin: 8pt 0;
}

strong {
    font-weight: bold;
}

em {
    font-style: italic;
}
"""


def export_with_weasyprint(md_path: Path, pdf_path: Path):
    """Convert markdown to PDF via weasyprint."""
    import markdown2
    from weasyprint import HTML, CSS

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert markdown to HTML
    html_content = markdown2.markdown(
        md_text,
        extras=["tables", "fenced-code-blocks", "strike", "header-ids"]
    )
    full_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>{html_content}</body>
</html>"""

    HTML(string=full_html).write_pdf(
        str(pdf_path),
        stylesheets=[CSS(string=CSS_STYLES)]
    )
    print(f"  Exported: {pdf_path.name}")


def export_with_reportlab_fallback(md_path: Path, pdf_path: Path):
    """Fallback: simple plain-text PDF via reportlab."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.enums import TA_LEFT
    import re

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=0.9 * inch,
        leftMargin=0.9 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    styles = getSampleStyleSheet()
    story = []

    for line in md_text.split("\n"):
        line = line.rstrip()
        if not line:
            story.append(Spacer(1, 6))
            continue
        if line.startswith("# ") and not line.startswith("## "):
            story.append(Paragraph(line[2:], styles["Title"]))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], styles["Heading2"]))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], styles["Heading3"]))
        elif line.startswith("- ") or line.startswith("* "):
            # Strip inline markdown for reportlab
            text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line[2:])
            story.append(Paragraph(f"• {text}", styles["Normal"]))
        elif line.strip() in ("---", "***"):
            story.append(Spacer(1, 4))
        else:
            text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
            story.append(Paragraph(text, styles["Normal"]))

    doc.build(story)
    print(f"  Exported (reportlab fallback): {pdf_path.name}")


def export_md_to_pdf(md_path: Path, pdf_path: Path):
    """Try weasyprint first, fall back to reportlab."""
    try:
        export_with_weasyprint(md_path, pdf_path)
    except ImportError:
        print("  weasyprint not available, using reportlab fallback...")
        try:
            export_with_reportlab_fallback(md_path, pdf_path)
        except ImportError:
            print("  ERROR: Neither weasyprint nor reportlab is installed.")
            print("  Run: pip install weasyprint  OR  pip install reportlab")
            raise


def main():
    if len(sys.argv) < 4:
        print("Usage: export_pdf.py <resume.md> <cover_letter.md> <output_dir>")
        sys.exit(1)

    resume_md = Path(sys.argv[1])
    cover_md = Path(sys.argv[2])
    output_dir = Path(sys.argv[3])

    if resume_md.exists():
        export_md_to_pdf(resume_md, output_dir / "resume.pdf")
    else:
        print(f"  WARNING: {resume_md} not found, skipping PDF export for resume.")

    if cover_md.exists():
        export_md_to_pdf(cover_md, output_dir / "cover_letter.pdf")
    else:
        print(f"  WARNING: {cover_md} not found, skipping PDF export for cover letter.")


if __name__ == "__main__":
    main()
