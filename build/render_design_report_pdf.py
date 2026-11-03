#!/usr/bin/env python3
"""Render the Chinese design report as a searchable PDF."""

from __future__ import annotations

import argparse
from html import escape
import math
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
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


INK = colors.HexColor("#20272A")
BLUE = colors.HexColor("#173B45")
RULE = colors.HexColor("#AAC0C4")
HEADER_FILL = colors.HexColor("#E9F0F1")


class ArchitectureDiagram(Flowable):
    """Draw the report's PS/PL data path from its Mermaid architecture block."""

    def __init__(self):
        super().__init__()
        self.width = 174 * mm
        self.height = 57 * mm

    def _box(self, c, x, y, w, h, label, fill, font_size=7.1):
        c.setFillColor(fill)
        c.setStrokeColor(colors.HexColor("#66858C"))
        c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
        c.setFillColor(BLUE)
        c.setFont("Deng-Bold", font_size)
        lines = label.split("\n")
        line_h = font_size + 2
        start_y = y + (h + (len(lines) - 1) * line_h) / 2 - font_size * 0.35
        for i, line in enumerate(lines):
            c.drawCentredString(x + w / 2, start_y - i * line_h, line)

    def _arrow(self, c, x1, y1, x2, y2, label=None):
        c.setStrokeColor(colors.HexColor("#52727A"))
        c.setFillColor(colors.HexColor("#52727A"))
        c.setLineWidth(1)
        c.line(x1, y1, x2, y2)
        angle = math.atan2(y2 - y1, x2 - x1)
        size = 4
        points = [
            (x2, y2),
            (x2 - size * math.cos(angle - 0.45), y2 - size * math.sin(angle - 0.45)),
            (x2 - size * math.cos(angle + 0.45), y2 - size * math.sin(angle + 0.45)),
        ]
        p = c.beginPath()
        p.moveTo(*points[0])
        p.lineTo(*points[1])
        p.lineTo(*points[2])
        p.close()
        c.drawPath(p, fill=1, stroke=0)
        if label:
            c.setFont("Deng", 6.3)
            c.setFillColor(colors.HexColor("#52676D"))
            c.drawCentredString((x1 + x2) / 2, (y1 + y2) / 2 + 4, label)

    def draw(self):
        c = self.canv
        input_fill = colors.HexColor("#EEF3F4")
        ps_fill = colors.HexColor("#E5F0EB")
        pl_fill = colors.HexColor("#E8EEF7")
        x = [4, 127, 250, 374]
        w = 105
        top_y = 119
        h = 31
        self._box(c, x[0], top_y, w, h, "麦克风 / WM8960", input_fill)
        self._box(c, x[1], top_y, w, h, "PS ALSA 采集", ps_fill)
        self._box(c, x[2], top_y, w, h, "WORLD 分析 (PS)", ps_fill)
        self._box(c, x[3], top_y, w, h, "最小相位接口 (PS)", ps_fill)
        self._arrow(c, x[0] + w, top_y + h / 2, x[1], top_y + h / 2)
        self._arrow(c, x[1] + w, top_y + h / 2, x[2], top_y + h / 2)
        self._arrow(c, x[2] + w, top_y + h / 2, x[3], top_y + h / 2)

        mid_y = 63
        self._box(c, 72, mid_y, 87, 30, "CPU 参考/回退", input_fill, 6.7)
        self._box(c, 193, mid_y, 105, 30, "Linux DMA 驱动", ps_fill, 6.7)
        self._box(c, 325, mid_y, 79, 30, "AXI HP2 / DDR", input_fill, 6.7)
        self._box(c, 423, mid_y, 70, 30, "HLS 核 (PL)", pl_fill, 6.5)
        self._arrow(c, 400, top_y, 251, mid_y + 30, "PL 调用")
        self._arrow(c, 383, top_y, 159, mid_y + 20, "CPU 模式")
        self._arrow(c, 298, mid_y + 15, 325, mid_y + 15)
        self._arrow(c, 404, mid_y + 15, 423, mid_y + 15)
        self._arrow(c, 423, mid_y + 7, 404, mid_y + 7)
        self._arrow(c, 423, mid_y + 23, 404, mid_y + 23)

        bot_y = 8
        self._box(c, 190, bot_y, 105, 30, "WORLD 合成 (PS)", ps_fill, 6.7)
        self._box(c, 324, bot_y, 79, 30, "PS ALSA 播放", ps_fill, 6.7)
        self._box(c, 423, bot_y, 70, 30, "WM8960 输出", input_fill, 6.5)
        self._arrow(c, 458, mid_y, 295, bot_y + 30, "计算结果")
        self._arrow(c, 295, bot_y + 15, 324, bot_y + 15)
        self._arrow(c, 403, bot_y + 15, 423, bot_y + 15)
        self._arrow(c, 114, mid_y, 190, bot_y + 25, "CPU 结果")


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
        "list": ParagraphStyle(
            "List", fontName="Deng", fontSize=9.4, leading=14.4,
            textColor=INK, alignment=TA_JUSTIFY, leftIndent=15, firstLineIndent=0,
            bulletIndent=0, bulletFontName="Deng", bulletFontSize=8.8,
            spaceAfter=5, wordWrap="CJK", splitLongWords=1,
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


def table_column_widths(column_count: int) -> list[float]:
    weights = {
        2: [1.0, 2.2],
        3: [1.0, 1.0, 2.2],
        4: [1.0, 1.1, 1.2, 1.7],
        5: [1.0, 1.0, 1.1, 1.4, 1.5],
    }.get(column_count, [1.0] * column_count)
    total_weight = sum(weights)
    available_width = 174 * mm
    return [available_width * weight / total_weight for weight in weights]


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
        elif kind == "list":
            ordered = token.get("attrs", {}).get("ordered", False)
            for index, item in enumerate(children, start=1):
                item_nodes = item.get("children", [])
                text_nodes = []
                for child in item_nodes:
                    if child.get("type") in ("block_text", "paragraph"):
                        text_nodes.extend(child.get("children", []))
                bullet = f"{index}." if ordered else "-"
                story.append(
                    Paragraph(
                        render_inline(text_nodes, branch), styles["list"],
                        bulletText=bullet,
                    )
                )
        elif kind == "block_code" and token.get("attrs", {}).get("info") == "mermaid":
            story.append(ArchitectureDiagram())
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
                rows, colWidths=table_column_widths(len(rows[0])),
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
