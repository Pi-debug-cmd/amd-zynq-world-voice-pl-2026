---
name: vivado-mcp-git-collaboration
description: 在本 FPGA 项目中通过仓库的 Vivado MCP 客户端开展 Vivado/Vitis 工作，以及执行按任务范围管理的 Git/GitHub 修改时使用。本技能记录已核对的 Windows/WSL 调用方式和近期 PS/PL 轮次经验。
---

# Vivado MCP 与 Git 协作

当任务涉及通过 MCP 使用 Vivado/Vitis、FPGA 构建证据，或本仓库的任务分支/提交/PR 时使用本技能。根目录 `AGENTS.md`、当前 `coummucation.md` 和任务所有权规则仍为权威依据；本技能说明如何在曾经失败的工作流程中落实这些规则。

开始操作前，检查工作树和未关闭的 PR。不要将无关或属于用户的改动带入任务提交。修改共享项目文件前，先在 `coummucation.md` 中认领任务。

只阅读当前工作所需的参考资料：

- 服务端/会话管理、Tcl 调用和工具故障见 [Vivado MCP](references/vivado_mcp.md)。
- 分支、任务认领、提交、推送和 PR 处理见 [Git 与 GitHub](references/git_github.md)。
- 近期 PS/PL 轮次的已核实故障和验收边界见[轮次经验](references/round_lessons.md)。

证据结论必须限定在实际测试范围内。Tcl 命令成功、C 仿真、OOC 实现、板卡启动、PL 计数器运行、音频进程运行和用户试听分别证明不同事项；不得拼接这些证据并作出超出其支持范围的结论。
