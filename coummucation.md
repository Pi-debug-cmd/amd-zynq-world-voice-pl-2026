# 协作记录

## SUBMIT-20261101-02 - 2026-11-02 - 提交包整理

- 状态：PROPOSED
- 基准提交：`92b5ba4`（`round30-submission-20261101-v4`）
- 改动：按 AMD 指南将提交包整理为 `src/`、`sim/`、`build/`、`board/`、`data/`、`skill/` 和 `report/` 目录结构；更新链接、指标校验路径和制品忽略规则。
- 路径：`README.md`、`.gitignore`、`board/`、`data/`、`report/`、`coummucation.md`。
- 复现/检查：`python data/metrics/scripts/validate_metrics.py`；`python -m unittest sim.test_world_minphase_boot -v`；`git diff --check`。
- 结果：全部 23 行指标都能定位到现有证据；在主机能力允许的情况下启动逻辑测试通过（Windows 上跳过了两个依赖 Shell 的用例）。
- 限制：Windows 主机无法进行 POSIX Shell 语法检查；本次仅整理文档，没有运行硬件、音频、Vivado 或 PetaLinux 测试。
- 下一责任方：仓库维护者审查并合并更新后的提交 PR。

## DOC-20261102-01 - 2026-11-02 - 文档中文化

- 状态：PROPOSED
- 角色：Codex
- 基准提交：`7a4d069`
- 改动范围：将英文提交说明、设计/接口/复现/硬件报告、制品说明、指标说明和技能文档翻译为中文；保留命令、代码标识、路径、哈希、实测数据和原验收结论。
- 路径：`README.md`、`board/`、`coummucation.md`、`data/`、`report/`、`skill/`。
- 复现/检查：运行 `python data/metrics/scripts/validate_metrics.py`、`python -m unittest sim.test_world_minphase_boot -v`、`git diff --check`，并检查 Markdown 中是否仍有未翻译的说明性英文。
- 结果：提交包中原为英文的说明文档已改为中文；指标校验通过（23 行均有证据文件）；启动逻辑测试 2 项通过、2 项因 Windows 主机没有 POSIX `sh` 而跳过；`git diff --check` 通过。
- 限制：本轮仅修改文档，不涉及硬件、Vivado、PetaLinux 或音频测试；两个依赖 POSIX Shell 的用例未运行。
- 下一责任方：Codex 完成文档检查后，由仓库维护者审查。

## SUBMIT-20261101-02 - 2026-11-02 - 设计报告 PDF

- 状态：PROPOSED
- 角色：Codex
- 基准提交：`ada17d7`
- 改动：将 `report/DESIGN_REPORT.md` 排版生成可搜索的中文版 A4 PDF，并在项目 README 和提交清单中加入入口。
- 路径：`output/pdf/design_report_cn.pdf`、`README.md`、`report/SUBMISSION_CHECKLIST.md`、`coummucation.md`。
- 复现/检查：`uv pip install reportlab mistune`；`python build/render_design_report_pdf.py --font-regular C:/Windows/Fonts/Deng.ttf --font-bold C:/Windows/Fonts/Dengb.ttf --github-branch agent/Pi-debug-cmd/SUBMIT-20261101-02`；用 `pdfinfo`、PyMuPDF 文本提取和 Poppler 页面渲染检查。
- 结果：2 页 A4；PDF 179,075 字节；中文文本可提取；两页均已渲染检查，表格列宽、跨页表头、页眉和页码正常。
- 限制：当前构建环境使用 Windows DengXian 字体；字体文件由操作系统提供，不随本项目分发。
- 下一责任方：仓库维护者审查并合并 PR。

## SUBMIT-20261101-02 - 2026-11-03 - 设计报告按官方内容项修订

- 状态：PROPOSED
- 角色：Codex
- 基准提交：`28ef8df`
- 改动：扩充中文版设计报告，使 AMD 指南设计报告要求对应章节、工程数据和复现限制；修复 PDF 框图 Flowable 尺寸、按表列数分配正文宽度，并渲染 Markdown 有序/无序列表。
- 路径：`build/render_design_report_pdf.py`、`output/pdf/design_report_cn.pdf`、`report/DESIGN_REPORT.md`、`report/SUBMISSION_CHECKLIST.md`、`coummucation.md`。
- 复现/检查：使用 `tmp/pdfs/.venv/Scripts/python.exe build/render_design_report_pdf.py --font-regular C:/Windows/Fonts/Deng.ttf --font-bold C:/Windows/Fonts/Dengb.ttf --github-branch agent/Pi-debug-cmd/SUBMIT-20261101-02` 生成 PDF；`pdfinfo` 确认 7 页 A4；PyMuPDF 确认复现第 1/6 步和自评章节可提取，正文文字坐标在页边界内；Poppler 逐页渲染检查框图、表格、页眉和页码；`git diff --check`。
- 结果：PDF 正文包含官方要求的背景/创新、功能框图、原理与接口、资源/性能对照、AI 协作记录、Skill 提炼与验证、复现说明。报告明示现有项目材料不能从空机器重建完整板端运行环境，不声称端到端从零复现已经满足。
- 限制：PetaLinux 2022.2 工程/BSP、可启动镜像、驱动模块和 WORLD 运行时文件仍未提供；Vivado 完整源码包未在干净环境重新完成全流程布线。此轮仅验证 PDF 文档，不重新进行板卡测试。
- 下一责任方：Codex 更新并推送当前 PR；维护者审核。
