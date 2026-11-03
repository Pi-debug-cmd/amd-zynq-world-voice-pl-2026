# 设计报告构建与版式来源

正式提交使用 `design_report.pdf`。正文在 `DESIGN_REPORT.md` 中维护，PDF 由 Typst 模板编译；`design_report.docx` 是同步正文、表格对齐和框图的 Word 编辑副本，其分页不作为 PDF 的构建来源。

封面采用用户选定的竞赛报告样式：赛事名称、居中项目标题、赛道说明、强调线、硬件与版本信息表以及报告范围。封面保留 Round30 PS/PL 项目的准确名称和事实，不沿用与本项目不符的早期“固定目标人物人声转换”标题。

## GitHub 项目

以下星数为 2026-11-03 查询结果，仅用于选型参考。

| 用途 | 项目与版本 | GitHub 星数 | 许可证 |
| --- | --- | --- | --- |
| PDF 排版与编译 | [Typst](https://github.com/typst/typst)，0.15.1 | 56,963 | Apache-2.0 |
| 技术报告模板 | [modern-g7-32](https://github.com/typst-gost/modern-g7-32)，0.2.0，源提交 `6fe1cb2ef8f09b1947b241c58b47e7858598f3ce` | 297 | GPL-3.0-only |
| 可编辑系统框图 | [draw.io](https://github.com/jgraph/drawio)，桌面版 32.6.1 | 9,155 | Apache-2.0 |

模板原始代码随项目放在 `template/modern-g7-32/`，上游文件保持原样，许可证全文一并保留。中文标题、字体、表格和图注设置集中在 `report_style.typ` 中。模板的 GPL 许可独立于项目自有代码的 MIT 许可。

## 编译 PDF

安装 Typst 0.15.1；本次使用 Windows 的 Times New Roman、宋体、黑体、Consolas 和 Microsoft YaHei 字体。在仓库根目录执行：

```sh
python build/render_design_report.py --typst /path/to/typst
```

脚本从 `report/DESIGN_REPORT.md` 填充模板，更新 `report/design_report.typ` 并编译 `report/design_report.pdf`。若 Typst 已在 PATH，可省略 `--typst`。也可对已填充的 Typst 源文件直接编译：

```sh
typst compile --root . report/design_report.typ report/design_report.pdf
```

## 修改框图

使用 draw.io 打开 `architecture_round30.drawio`。框图采用软件中的标准矩形、容器与正交连接线，文字作为可编辑标签保存。修改后由 draw.io 导出 PNG 和 SVG；PDF 使用 2 倍比例导出的 PNG，避免不同 SVG 查看器对 HTML 标签的兼容差异。

```sh
draw.io --export --format png --scale 2 --output report/architecture_round30.png report/architecture_round30.drawio
draw.io --export --format svg --output report/architecture_round30.svg report/architecture_round30.drawio
```

## 版式约定

五张表的表头和数据单元格统一左对齐，取消首行缩进和两端对齐。每张表及其标题保持在同一页；Round20 两段数据整表排放。框图分清 PS 软件、PS DDR 和 PL HLS 核，区分数据与控制连接。正文保留 Round30 源基线及原有测试结果，不新增性能收益结论。
