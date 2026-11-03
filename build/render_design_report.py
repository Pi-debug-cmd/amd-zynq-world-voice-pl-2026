#!/usr/bin/env python3
"""Fill the vendored modern-g7-32 report template and compile with Typst."""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report"


def quoted(value):
    return json.dumps(value, ensure_ascii=False)


def literal(value):
    return re.sub(r"([\\#*$@_<>{}\[\]])", r"\\\1", value)


def inline(value):
    tokens = re.split(r"(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\))", value)
    out = []
    for token in tokens:
        if token.startswith("`") and token.endswith("`"):
            out.append("#code(" + quoted(token[1:-1]) + ")")
        elif token.startswith("**") and token.endswith("**"):
            out.append("#strong[" + literal(token[2:-2]) + "]")
        elif re.fullmatch(r"\[[^\]]+\]\([^)]+\)", token):
            label, url = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", token).groups()
            out.append("#link(" + quoted(url) + ")[" + literal(label) + "]")
        else:
            out.append(literal(token))
    return "".join(out)


def generate():
    lines = (REPORT / "DESIGN_REPORT.md").read_text(encoding="utf-8").splitlines()
    first = next(i for i, line in enumerate(lines) if line.startswith("# 一、"))
    introduction = next(line for line in lines[:first] if line.startswith("本报告说明"))
    output = ['#import "report_style.typ": report, report-table, code\n#show: report', "", inline(introduction), ""]
    i = first
    table_index = 0
    widths = ["(1.1fr, 3.7fr)", "(1.0fr, 1.7fr, 3.0fr)", "(1.1fr, 1.3fr, 1.4fr, 2.7fr)", "(0.8fr, 2.3fr, 2.3fr, 2.5fr)", "(1.0fr, 2.6fr, 2.4fr, 2.6fr)"]
    captions = ["PS/PL 接口与运行约定", "数值验证与资源实现结果", "Round20 文件路径对照", "大模型协作与纠正记录", "技能包提炼与适用边界"]
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            output.append("#report-table(" + widths[table_index] + ", [" + captions[table_index] + "], (")
            for row in rows:
                output.append("  (" + ", ".join("[" + inline(c) + "]" for c in row) + "),")
            output.append("))\n")
            table_index += 1
            continue
        if line.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            output.append("#raw(" + quoted("\n".join(code)) + ", block: true)\n")
        elif line.startswith("!["):
            output.append('#figure(image("architecture_round30.png", width: 92%), caption: [PS 与 PL 协作的数据流框图])\n')
        elif line.startswith("## "):
            output.append("== " + inline(line[3:]) + "\n")
        elif line.startswith("# "):
            output.append("= " + inline(line[2:]) + "\n")
        elif line.startswith("- "):
            output.append("- " + inline(line[2:]))
        elif re.match(r"\d+\. ", line):
            output.append("+ " + inline(re.sub(r"^\d+\. ", "", line)))
        else:
            output.append(inline(line))
        i += 1
    assert table_index == 5, "Review table mapping after changing the report structure"
    destination = REPORT / "design_report.typ"
    destination.write_text("\n".join(output) + "\n", encoding="utf-8")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--typst", default="typst", help="Typst executable (0.15.1 used for the submitted PDF)")
    parser.add_argument("--source-only", action="store_true", help="Regenerate Typst source without compiling")
    args = parser.parse_args()
    source = generate()
    if not args.source_only:
        subprocess.run([args.typst, "compile", "--root", str(ROOT), str(source), str(REPORT / "design_report.pdf")], check=True)
    print(source)


if __name__ == "__main__":
    main()
