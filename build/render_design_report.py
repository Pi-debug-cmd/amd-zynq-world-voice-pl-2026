#!/usr/bin/env python3
"""Render report/DESIGN_REPORT.md into an editable Chinese DOCX."""
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "report" / "DESIGN_REPORT.md"
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "report" / "design_report.docx"


def set_font(run, name="Microsoft YaHei", size=10.5, bold=None, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)


def shade(cell, fill):
    properties = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    properties.append(shading)


def set_cell_text(cell, text, header=False):
    cell.text = ""
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    paragraph = cell.paragraphs[0]
    paragraph.paragraph_format.space_after = Pt(2)
    paragraph.paragraph_format.space_before = Pt(2)
    plain = re.sub(r"[`*_]", "", text.strip())
    run = paragraph.add_run(plain)
    set_font(run, size=8.5, bold=header, color=(255, 255, 255) if header else (38, 49, 62))
    if header:
        shade(cell, "245A73")


def add_page_field(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, end])
    set_font(run, size=9, color=(100, 110, 120))


def inline_text(paragraph, text):
    parts = re.split(r"(`[^`]+`|\*\*[^*]+\*\*)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            set_font(run, name="Consolas", size=9, color=(32, 89, 115))
        elif part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            set_font(run, bold=True)
        else:
            run = paragraph.add_run(part)
            set_font(run)


def parse_table(lines, start):
    rows = []
    index = start
    while index < len(lines) and lines[index].strip().startswith("|"):
        cells = [value.strip() for value in lines[index].strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-{3,}:?", value) for value in cells):
            rows.append(cells)
        index += 1
    return rows, index


def main():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(1.8)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)
    section.header_distance = Cm(0.9)
    section.footer_distance = Cm(0.9)
    add_page_field(section.footer.paragraphs[0])

    normal = doc.styles["Normal"]
    normal.font.name = "Microsoft YaHei"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.16
    for style_name, size, color in (("Heading 1", 16, (36, 82, 104)), ("Heading 2", 12.5, (36, 82, 104))):
        style = doc.styles[style_name]
        style.font.name = "Microsoft YaHei"
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(*color)
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.keep_with_next = True

    title = lines[0].removeprefix("# ").strip()
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(54)
    title_p.paragraph_format.space_after = Pt(22)
    set_font(title_p.add_run(title), size=24, bold=True, color=(27, 63, 83))

    meta = []
    idx = 1
    while idx < len(lines) and not lines[idx].startswith("## "):
        if lines[idx].strip():
            meta.append(lines[idx].replace("**", "").strip())
        idx += 1
    for line in meta:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(5)
        set_font(p.add_run(line), size=11, color=(72, 83, 92))
    doc.add_page_break()

    in_code = False
    code_lines = []
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(0.35)
                p.paragraph_format.space_after = Pt(6)
                for n, code_line in enumerate(code_lines):
                    if n:
                        p.add_run().add_break()
                    set_font(p.add_run(code_line), name="Consolas", size=8.5, color=(50, 63, 72))
                code_lines = []
                in_code = False
            else:
                in_code = True
            idx += 1
            continue
        if in_code:
            code_lines.append(line)
            idx += 1
            continue
        if stripped.startswith("|"):
            rows, idx = parse_table(lines, idx)
            if rows:
                table = doc.add_table(rows=len(rows), cols=max(map(len, rows)))
                table.style = "Table Grid"
                table.autofit = True
                for r, row in enumerate(rows):
                    row_properties = table.rows[r]._tr.get_or_add_trPr()
                    row_properties.append(OxmlElement("w:cantSplit"))
                    if r == 0:
                        repeat = OxmlElement("w:tblHeader")
                        repeat.set(qn("w:val"), "true")
                        row_properties.append(repeat)
                    for c in range(len(table.columns)):
                        set_cell_text(table.cell(r, c), row[c] if c < len(row) else "", header=(r == 0))
                doc.add_paragraph().paragraph_format.space_after = Pt(1)
            continue
        if not stripped:
            idx += 1
            continue
        if stripped.startswith("## "):
            p = doc.add_paragraph(style="Heading 1")
            inline_text(p, stripped[3:])
        elif stripped.startswith("### "):
            p = doc.add_paragraph(style="Heading 2")
            inline_text(p, stripped[4:])
        elif stripped.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
            inline_text(p, stripped[2:])
        elif re.match(r"\d+\. ", stripped):
            p = doc.add_paragraph(style="List Number")
            p.paragraph_format.space_after = Pt(2)
            inline_text(p, re.sub(r"^\d+\. ", "", stripped))
        else:
            p = doc.add_paragraph()
            inline_text(p, stripped)
        idx += 1

    doc.core_properties.title = title
    doc.core_properties.subject = "AMD 自主选题赛道 Round30 最终板上版本"
    doc.core_properties.keywords = "Zynq-7020, WORLD, PS, PL, Round30"
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
