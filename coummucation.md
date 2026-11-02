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
