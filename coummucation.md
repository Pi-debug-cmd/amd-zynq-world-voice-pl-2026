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

## SUBMIT-20261103-01 Round30 纯代码归档

- 日期：2026-11-03；角色：Hardware-A / Codex；状态：CLAIMED → ACCEPTED（源码归档完整性核验通过）。
- 基准提交：参赛仓库 `270fb76`；总项目板端版本 `a8f6f8f32b159eaea277354118220c633f31fbc2`。
- 改动路径：`board/vendor_inputs/`、`report/code_archive_round30_20261103.md`、`coummucation.md`；RAR 交付文件位于 `D:/嵌赛提交/`，不纳入 Git。
- 复现命令：`Rar.exe t D:/嵌赛提交/AMD_Zynq_PS_PL_Round30_总代码.rar`；解压后逐一比较包内文件和参赛仓库文件的 SHA-256。
- 量化结果：58 个源码、脚本、配置及许可证文件；110,434 字节；SHA-256 `a46799c0e2ff8d8c596952e23b7779b5695873eae45499cc966565eab288f762`；解压校验差异 0。
- 限制：未重新执行板测或硬件构建；技术报告、PDF/Word、音频、商家基础工程 ZIP、位流及镜像均不在总代码 RAR 中。
- 报告链接：`report/code_archive_round30_20261103.md`。
- 下一责任方：维护者分别审阅总代码 RAR 和单独提交的设计报告。

## DOCS-20261104-01 用户指定封面标题

- 日期：2026-11-04；角色：Hardware-A / Codex；状态：CLAIMED。
- 基准提交：`fb47daf27f6fec91b32f3fd9215b63d462e1f417`。
- 改动路径：`report/report_style.typ`、`report/DESIGN_REPORT.md`、`report/design_report.pdf`、`report/REPORT_BUILD.md`；仅更新报告标题及相关说明。
- 复现命令：`python build/render_design_report.py --typst /path/to/typst`。
- 量化结果：待核验标题、页数及正文页面与改名前的一致性。
- 限制：不涉及算法、板卡测试；总代码 RAR 不重打。
- 下一责任方：Codex 导出 PDF 并核验封面。
- 状态更新：ACCEPTED（封面核验完成）；PDF 5 页，正文 4 页渲染图逐页哈希一致；新标题与 PDF 元数据一致。
- 报告链接：`report/document_layout_review_20261103.md` 的 2026-11-04 核验条目。
- 交付：`report/design_report.pdf`，并复制到 `D:/嵌赛提交/基于 ZYNQ-7020 的低延迟固定目标人物人声转换系统设计报告.pdf`。
- 下一责任方：维护者审阅现有 PR #2。

## DOCS-20261104-02 最终版本优化对比

- 日期：2026-11-04；角色：Hardware-A / Codex；状态：CLAIMED。
- 基准提交：`5640423`；实现基线仍为 Round30。
- 改动路径：`report/DESIGN_REPORT.md`、生成的 Typst/PDF、报告构建脚本的表题及排版核验记录。
- 任务：第四章加入 Round23、Round29 与最终 Round30 对比，最终行加粗；以已有板端记录说明自动启动、PCM 释放及状态管理改进。
- 复现：`python build/render_design_report.py --typst /path/to/typst`，Poppler 渲染核验。
- 量化结果：待 PDF 校验；不产生新板测或性能数据。
- 下一责任方：Codex 完成内容与排版核验后更新 PR #2。
- 状态更新：ACCEPTED（内容与排版核验通过）。PDF 5 页；新增三行对比，Round30 整行加粗；第 1—2 页渲染一致，其他章节文本一致。
- 证据：`report/document_layout_review_20261103.md` 的最终版本对比核验条目；数值来自现有 Round23/29/30 报告。
- 交付：仓库 PDF 与提交目录的“基于 ZYNQ-7020 的低延迟固定目标人物人声转换系统设计报告_最终版本对比修订版.pdf”已同步；原中文 PDF 被阅读器映射占用，保留原文件。源码 RAR 哈希保持不变，不新增板测结论。
- 下一责任方：维护者审阅 PR #2。
