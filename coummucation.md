# 参赛提交协作记录

## SUBMIT-20261103-01 报告模板与框图更新

- 日期：2026-11-03。
- 角色：Hardware-A / Codex，文档与交付整理。
- 状态：CLAIMED → ACCEPTED（本轮文档构建与排版核验通过）。
- 基准提交：参赛仓库 `ad8d8b9f1d71886746da952f8dd237352e263480`；板上实现仍为 Round30 源基线 `a8f6f8f32b159eaea277354118220c633f31fbc2`。
- 修改路径：`report/`、`build/render_design_report.py`、`README.md`、`LICENSE`。
- 操作：采用 GitHub modern-g7-32 报告模板和 draw.io 框图工具，统一表格左对齐和整表分页，更新 PDF、Word 编辑副本、Typst 源文件、框图源文件及清单。
- 复现命令：`python build/render_design_report.py --typst /path/to/typst`；框图导出命令见 `report/REPORT_BUILD.md`。
- 量化结果：正式 PDF 5 页；5 张表；Round20 两条数据同在第 3 页；逐段正文和逐单元格文本核对通过。完整检查见 `report/document_layout_review_20261103.md`。
- 限制：本轮仅核验文档构建、内容迁移和归档，不新增板测、音质或性能结论；Word 为正文编辑副本，正式 PDF 由 Typst 源文件构建。
- GitHub：沿用分支 `agent/Pi-debug-cmd/SUBMIT-20261103-01` 和 PR #2。
- 下一责任方：维护者审阅 PDF、PR 与 RAR 后选择提交材料。

## SUBMIT-20261103-01 封面样式更新

- 日期：2026-11-03；状态：ACCEPTED（封面与 PDF 重建核验通过）。
- 基准：`74f143bb4ec7304075d82bea939217804faef04c`；Round30 板端实现基线 `a8f6f8f32b159eaea277354118220c633f31fbc2`。
- 修改：按用户提供的参考封面更新 Typst 报告源，加入赛事抬头、居中标题、赛道说明、强调线、平台/软硬件/版本/日期信息表与报告范围。保留当前 WORLD PS/PL 项目名称和内容，不套用早期人声转换项目标题。
- 复现：`python build/render_design_report.py --typst /path/to/typst`。
- 核验：正式 PDF 5 页；正文 101 个表格单元格文本匹配；Round20 两条数据保持同在第 3 页；封面及全部页面已渲染检查。
- 交付：PR #2 更新至本轮提交；封面版 PDF 和 RAR 置于 `D:/嵌赛提交/`。
- 限制：仅更新文档封面和文档构建源，不涉及板测或实现变更。
