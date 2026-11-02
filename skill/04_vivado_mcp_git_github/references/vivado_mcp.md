# Vivado MCP 调用

## 使用仓库客户端

项目客户端为 `tools/mcp_vivado.py`，使用 Python 标准库实现。必要时它会启动 MCP 守护进程，并提供以下操作：

```powershell
python tools/mcp_vivado.py status
python tools/mcp_vivado.py start
python tools/mcp_vivado.py exec "puts [version -short]"
python tools/mcp_vivado.py raw vivado_execute '{"session_id":"<session-id>","command":"puts [version -short]"}'
python tools/mcp_vivado.py stop <session-id>
```

`status` 列出会话，并可能启动守护进程。`start` 创建 Tcl 模式的 Vivado 会话。`exec` 是便捷封装，会选择第一个匹配的 Vivado 会话；如果有多个会话运行或需要明确会话所有权，应通过 `raw vivado_execute` 指定会话 ID。只停止本任务创建的会话。共享环境中不得使用影响整个守护进程的 `--kill-all`。

每次启动会话后、构建前，先确认工具版本、器件和工程上下文：

```powershell
python tools/mcp_vivado.py exec "puts [version -short]"
python tools/mcp_vivado.py exec "puts PARTS=[llength [get_parts xc7z020clg400-2]]"
```

本项目已核对的环境使用 Vivado 2026.1 和 `xc7z020clg400-2`。应在本机确认实际安装位置；历史 Windows 路径 `D:\USER_Software\vivado\2026.1\Vivado\bin\vivado.bat` 仅适用于特定机器。该主机上的路径多一层 `Vivado` 目录。除非有独立证据排除，否则 `Vivado binary not found` 应先按路径/配置问题排查。

## Tcl 与构建处理

- Tcl 表达式应尽量简单，避免再用一层 Tcl 双引号包住方括号替换。例如使用 `puts N=[llength [get_parts]]`，不要写成 `puts "N=[llength [get_parts]]"`。
- 可复现构建应使用项目 Tcl 脚本。曾经通过 MCP/Web 服务器后备通道发送较长 Tcl 脚本时发生卡住；交互诊断应拆成短命令，可复现构建则使用仓库内的 Tcl 脚本。
- 记录会话 ID、工具版本、器件型号、时钟约束、源码版本、命令/脚本、输出路径和相关报告。检查工具报错及生成报告，不要只看客户端进程退出码。
- 在当前会话中确认请求的器件确实存在。曾有不完整的器件安装导致器件列表为空并报 `Could not get a valid part`；修复器件数据后需要重启 Vivado 会话，因为旧会话缓存了空器件注册表。
- HLS/IP 生成遇到 Windows 路径长度错误时，可使用较短的任务专属构建根目录，例如 `D:/wpl_<date>_<round>/...`；不要移动或覆盖仓库中的源码。记录外部构建路径及所有源码/测试平台/脚本哈希，便于其他工程师复现。
- 本项目环境中，xsim 曾在工作区文件筛选驱动下崩溃。可将仿真产物放在经批准的外部临时目录（历史路径为 `D:/xsim_work/<task>`），并将源码向量和复现命令留在仓库。采用历史解决方法前，先核对当前机器策略。
- 综合/实现前检查许可证是否可用。版本查询和基础 Tcl 表达式不能证明综合许可证或器件安装可用。

## 故障定位

1. 保存准确的请求、响应、会话 ID 和相关 MCP/Vivado 日志。
2. 区分客户端/服务端/会话错误、Vivado 命令错误，以及安装/许可证错误。
3. 在同一会话中运行最小诊断（`version`、`get_parts`，再按需执行最小读取/综合/仿真检查）。
4. 每次只修改一个可能原因。保留失败日志，并在同一任务轮次记录解决过程。
5. 如果会话共享或所有者不明确，应检查会话列表并协调；不要猜测性地停止或重置会话。

## 证据边界

RTL 仿真只能证明设计符合其测试平台。OOC 实现只能证明计算核级别的实现结果。完整 Block Design 和顶层布线只能证明在所列约束下的系统集成/时序结果。位流已加载或 `fpga_manager` 处于活动状态，并不能证明预期加速器正在被调用。板端计数器、数据对比、实时音频、用户试听和长时稳定性都需要各自独立的证据。
