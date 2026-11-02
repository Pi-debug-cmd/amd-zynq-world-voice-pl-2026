#!/usr/bin/env python3
"""Render the Chinese design report as a searchable PDF."""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import posixpath
from urllib.parse import quote

import mistune
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


INK = colors.HexColor("#20272A")
BLUE = colors.HexColor("#173B45")
RULE = colors.HexColor("#AAC0C4")
HEADER_FILL = colors.HexColor("#E9F0F1")


def make_styles():
    return {
        "title": ParagraphStyle(
            "Title", fontName="Deng-Bold", fontSize=20, leading=27,
            alignment=TA_CENTER, textColor=BLUE, spaceAfter=17,
        ),
        "h2": ParagraphStyle(
            "H2", fontName="Deng-Bold", fontSize=13.5, leading=19,
            textColor=BLUE, spaceBefore=13, spaceAfter=6, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body", fontName="Deng", fontSize=9.6, leading=15.2,
            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=6,
            wordWrap="CJK", splitLongWords=1,
        ),
        "cell": ParagraphStyle(
            "Cell", fontName="Deng", fontSize=7.7, leading=11.1,
            textColor=INK, alignment=TA_LEFT, wordWrap="CJK", splitLongWords=1,
        ),
        "headcell": ParagraphStyle(
            "HeadCell", fontName="Deng-Bold", fontSize=7.8, leading=11.2,
            textColor=BLUE, alignment=TA_LEFT, wordWrap="CJK",
        ),
    }


def github_href(url: str, branch: str) -> str:
    if url.startswith(("https://", "http://", "mailto:")):
        return url
    path, _, fragment = url.partition("#")
    repo_path = posixpath.normpath(posixpath.join("report", path))
    suffix = f"#{fragment}" if fragment else ""
    return (
        "https://github.com/Pi-debug-cmd/amd-zynq-world-voice-pl-2026/blob/"
        f"{branch}/{quote(repo_path, safe='/')}{suffix}"
    )


def render_inline(nodes, branch: str) -> str:
    output = []
    for node in nodes or []:
        kind = node.get("type")
        children = node.get("children", [])
        if kind == "text":
            output.append(escape(node.get("raw", "")))
        elif kind == "codespan":
            output.append(
                '<font name="Courier" color="#214D56">'
                + escape(node.get("raw", ""))
                + "</font>"
            )
        elif kind == "strong":
            output.append(f"<b>{render_inline(children, branch)}</b>")
        elif kind == "emphasis":
            output.append(f"<i>{render_inline(children, branch)}</i>")
        elif kind == "link":
            url = github_href(node.get("attrs", {}).get("url", ""), branch)
            output.append(
                f'<link href="{escape(url, quote=True)}" color="#176C78">'
                f"{render_inline(children, branch)}</link>"
            )
        elif kind in ("softbreak", "linebreak"):
            output.append("<br/>")
        else:
            output.append(render_inline(children, branch))
    return "".join(output)


def make_story(source: Path, styles, branch: str):
    tokens = mistune.create_markdown(renderer="ast", plugins=["table"])(
        source.read_text(encoding="utf-8")
    )
    story = []
    for token in tokens:
        kind = token.get("type")
        children = token.get("children", [])
        if kind == "heading":
            text = render_inline(children, branch)
            if token.get("attrs", {}).get("level") == 1:
                story.append(Paragraph(text, styles["title"]))
            else:
                story.append(Paragraph(text, styles["h2"]))
                rule = Table([ [""] ], colWidths=[174 * mm], rowHeights=[0.45])
                rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), RULE)]))
                story.extend([rule, Spacer(1, 5)])
        elif kind == "paragraph":
            story.append(Paragraph(render_inline(children, branch), styles["body"]))
        elif kind == "table":
            head = next((row for row in children if row.get("type") == "table_head"), None)
            body = next((row for row in children if row.get("type") == "table_body"), None)
            rows = []
            if head:
                rows.append([
                    Paragraph(render_inline(cell.get("children", []), branch), styles["headcell"])
                    for cell in head.get("children", [])
                ])
            if body:
                for row in body.get("children", []):
                    rows.append([
                        Paragraph(render_inline(cell.get("children", []), branch), styles["cell"])
                        for cell in row.get("children", [])
                    ])
            table = Table(
                rows, colWidths=[35 * mm, 34 * mm, 105 * mm],
                repeatRows=1, hAlign="LEFT", splitByRow=1,
            )
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), HEADER_FILL),
                ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#B8C4C7")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([Spacer(1, 3), table, Spacer(1, 7)])
    return story


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, A4[1] - 15 * mm, A4[0] - 18 * mm, A4[1] - 15 * mm)
    canvas.setFont("Deng", 7.5)
    canvas.setFillColor(colors.HexColor("#52676D"))
    canvas.drawString(18 * mm, A4[1] - 12 * mm, "WORLD 最小相位 PS+PL 设计报告")
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("report/DESIGN_REPORT.md"))
    parser.add_argument("--output", type=Path, default=Path("output/pdf/design_report_cn.pdf"))
    parser.add_argument("--font-regular", type=Path, required=True, help="Chinese TrueType regular font")
    parser.add_argument("--font-bold", type=Path, required=True, help="Chinese TrueType bold font")
    parser.add_argument("--github-branch", default="main", help="branch used for report links")
    args = parser.parse_args()

    pdfmetrics.registerFont(TTFont("Deng", str(args.font_regular), subfontIndex=0))
    pdfmetrics.registerFont(TTFont("Deng-Bold", str(args.font_bold), subfontIndex=0))
    pdfmetrics.registerFontFamily(
        "Deng", normal="Deng", bold="Deng-Bold", italic="Deng", boldItalic="Deng-Bold"
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(args.output), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=21 * mm, bottomMargin=17 * mm,
        title="WORLD 最小相位 PS+PL 设计报告", author="项目组",
    )
    doc.build(
        make_story(args.input, make_styles(), args.github_branch),
        onFirstPage=draw_page, onLaterPages=draw_page,
    )
    print(f"Created {args.output} ({args.output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
