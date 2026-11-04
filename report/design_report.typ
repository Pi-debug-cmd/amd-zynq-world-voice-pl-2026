#import "report_style.typ": report, report-table, code
#show: report

本报告说明实际板上运行版本的 PS/PL 分工、数据接口、硬件实现、实测结果、AI 协作过程、技能提炼和复现步骤。系统由 ARM Cortex-A9 PS 执行 WORLD 实时语音流程和音频 I/O，由 HLS PL 核承担 WORLD 中固定 1024 点的融合最小相位频谱计算。

= 一、选题背景与创新点


WORLD 语音处理包含分析、频谱处理和合成等多个阶段。将完整语音流程一次性迁入可编程逻辑，会扩大接口与数值验证范围，也会使硬件误差、调度开销和音频链路问题难以分开定位。本项目选择输入输出维度固定、可与软件参考逐向量比对的最小相位频谱阶段作为 PS 与 PL 的协作边界。

项目要解决的工程问题是：如何在 Zynq-7020 上保留已有 Linux 音频系统与 WORLD 主流程，同时把确定性计算阶段接入 PL，并管理其 PS DDR 数据、DMA 一致性、控制寄存器、运行时后端选择、错误处理和开机部署。

本项目的技术贡献集中在系统集成与可验证的软硬件协作：

- 将 WORLD 最小相位分析的 1024 点计算融合为一个 HLS 核，提供固定输入输出契约和 WORLD 软件黄金参考。
- 在原有音频通路之外，为计算核建立 AXI-Lite 控制和独立 HP2 DDR coherent-DMA 数据通路。
- 在 PS 侧保留 CPU 软件参考路径，通过运行时选项调用 PL，并记录调用、回退和耗时数据。
- 将 HLS 数值核、整机实现、板端文件对照、实时音频和持久启动分层验证，避免用单一测试代替完整系统结论。

项目采用已公开的 WORLD 算法与板卡音频接口，不主张新语音模型或新信号处理理论。所报告的时间数据用于说明测试观察，不据两段样本宣称稳定性能收益。

= 二、设计原理与功能框图


输入音频经 WM8960 和 ALSA 到达 PS。PS 运行 WORLD 实时流，对每个分析帧生成 513 个 float32 对数频谱点。默认软件模式由 CPU 计算最小相位频谱；PL 模式通过 #code("/dev/world_minphase") 向内核驱动提交 coherent-DMA 缓冲区。PL 核返回 513 个复数 float32 频点，PS 随后继续 WORLD 合成，并经 ALSA 和 WM8960 输出。

#figure(image("architecture_round30.png", width: 92%), caption: [PS 与 PL 协作的数据流框图])


HLS 核将输入对数频谱映射为 1024 点变换所需的复数最小相位滤波器频点。核内融合两次 FFT 通路以及倒谱、指数、余弦和正弦运算。该设计替代 WORLD 的一个计算阶段；音频采集、WORLD 其他处理、流调度与播放仍由 PS 软件执行。

= 三、软硬件划分依据与接口设计


固定变换长度和明确的数据维度使该阶段适合硬件实现；PS 则保留需要 Linux 设备访问、动态调度和算法控制的部分。CPU 与 PL 使用同一组 WORLD 接口，因而可以在软件参考、HLS 仿真、板端向量和实时链路之间逐级比对。

#report-table((1.1fr, 3.7fr), [PS/PL 接口与运行约定], (
  ([项目], [最终实现约定]),
  ([器件], [#code("xc7z020clg400-2")]),
  ([PL 时钟], [PS #code("FCLK_CLK0")，整机实现记录为 100 MHz]),
  ([HLS 顶层], [#code("world_minphase")，变换长度 1024]),
  ([输入], [513 个 float32 对数频谱值]),
  ([输出], [513 个 float32 实部与 513 个 float32 虚部]),
  ([AXI-Lite 控制], [#code("0x43C70000")]),
  ([AXI-Lite 指针参数], [#code("0x43C80000")]),
  ([DDR 数据接口], [HLS 输入/输出主接口经独立互连访问 PS #code("S_AXI_HP2")]),
  ([Linux 接口], [#code("/dev/world_minphase")，#code("WORLD_MINPHASE_PROCESS") ioctl]),
  ([PS 缓冲区], [Linux coherent-DMA 驱动负责分配、地址映射和设备访问]),
  ([后端选择], [#code("WORLD_MINPHASE=cpu") 使用软件参考；#code("WORLD_MINPHASE=pl") 调用 PL]),
  ([音频运行格式], [ALSA 32 kHz、S24\_LE、双声道；算法流为 16 kHz 单声道]),
))


寄存器、数据包布局、超时和 DMA 语义以 #code("src/kernel/world_minphase_ioctl.h")、#code("src/kernel/world_minphase_dma.c") 及 HLS/Vivado 工程为准。PL 请求失败会明确报错，不静默伪装成硬件成功；不支持的 FFT 长度按接口契约回退到 CPU 并计数。

= 四、优化过程与性能/资源对比


最终交付为 #strong[Round30 持久启动版本]。Round16—20 是本方案的数值核、硬件实现与板端对照验证，构成最终方案的验证依据；随后通过 Round23 实时语音运行及 Round29—30 部署迭代，完成从计算核接入到开机自动运行的系统集成。下表按阶段列出结果，最终版本整行加粗。

#report-table((1.0fr, 1.7fr, 3.0fr), [优化过程与最终 Round30 版本对比], (
  ([验证层级], [Round / 条件], [结果]),
  ([HLS 数值验证], [Round16，24 组 WORLD 参考向量], [24/24 通过；最大相对 L2 误差 #code("8.53141669193e-7")]),
  ([核级布局布线], [Round17，100 MHz OOC], [4,996 LUT、5,769 FF、3.5 BRAM Tile、38 DSP；WNS #code("+1.327 ns")、WHS #code("+0.053 ns")]),
  ([整机实现], [Round18，Zynq-7020 音频设计], [13,910 LUT、20,145 FF、9.5 BRAM Tile、47 DSP；WNS #code("+0.856 ns")、WHS #code("+0.029 ns")；DRC Error 为 0]),
  ([板端数值], [Round20，24 向量和两段 5 秒文件], [向量 24/24；文件输出 SNR 为 #code("97.371/96.942 dB")，最大 PCM16 差 1，PL fallback/timeout 为 0]),
  ([实时语音验证], [Round23，20 秒有效讲话], [1,079 个有声帧；PL 调用 4,857 次、fallback 0；录放 xrun、ALSA error 均为 0；用户确认转换效果与 PS 路径类似]),
  ([持久部署迭代], [Round29，手动启用与重启], [手动启用后双 PCM 运行；重启时开机测试音占用播放设备，尚需完善启动协调]),
  ([#text(font: ("Times New Roman", "SimHei"), weight: "bold")[#strong[最终上板版本]]], [#text(font: ("Times New Roman", "SimHei"), weight: "bold")[#strong[Round30，正常重启后自动运行]]], [#text(font: ("Times New Roman", "SimHei"), weight: "bold")[#strong[修复开机音频占用及旧状态误判；自动进入 READY\_CANDIDATE；采集/播放 PCM 均 RUNNING；PL 调用由 2,278 增至 13,751，DISABLE 不存在]]]),
))


#strong[最终版本的优势在于 PS/PL 协作链路的自动运行与部署完整性。] 相比 Round20 文件对照和 Round23 单次实时试运行，Round30 在正常重启后自动启动转换链路；相比 Round29，启动前精确清理遗留测试音进程、等待 PCM 释放，并清除旧状态，完成启动冲突修复。PS 负责音频与 WORLD 调度，PL 在运行中持续参与最小相位频谱计算。

资源数据来自 Round17 核级与 Round18 整机实现记录，Round30 数据来自持久启动验收，两类结果分别列示。Round18 既有整机参考为 8,026 LUT、13,283 FF、6 BRAM Tile、9 DSP。最终部署改进依据见 Round29/30 报告；下表保留 Round20 的同输入 CPU/PL 文件对照。

#report-table((1.1fr, 1.3fr, 1.4fr, 2.7fr), [Round20 文件路径对照], (
  ([Round20 文件], [CPU 软件路径], [最小相位 PL 路径], [输出差异]),
  ([male1，5 秒], [2.845253 s], [2.748740 s], [SNR 97.371389 dB，最大差 1 PCM16 count]),
  ([male4，5 秒], [2.822582 s], [2.747420 s], [SNR 96.942108 dB，最大差 1 PCM16 count]),
))


Round20 两条路径的输出 SNR 约 97 dB、最大差 1 PCM16 count，为 PS/PL 数值一致性提供依据；耗时对应本轮两段短文件。Round30 的新增成果是上述自动启动和运行状态管理，未将早期耗时标为 Round30 新测数据。

= 五、大模型协作记录


协作记录按 AMD 指南第 3.3.3.1 和 3.3.5.3 要求，保留关键提示、决策摘要与纠正过程。完整提示工作流模板见 #code("skill/05_ps_pl_prompt_flow/")，任务级记录见 #code("docs/ai_collaboration.md")。

#report-table((0.8fr, 2.3fr, 2.3fr, 2.5fr), [大模型协作与纠正记录], (
  ([阶段], [提示/任务], [模型决策], [纠正与最终处理]),
  ([范围锁定], [“以总项目中板子最终实现的版本为准，AMD 提交仓库、技术文档和总代码只对应该版本。”], [核对 Round30 源提交和板端报告，固定提交 #code("a8f6f8f32b159eaea277354118220c633f31fbc2")], [排除后续 Round31-34 试验代码，不把分支最新头误作已部署版本]),
  ([赛道适配], [“按 AMD 2026 PDF 检查 PS+PL 是否符合初级组要求。”], [对照官方第 3.3 节，PS、Vitis HLS/RTL 组合允许；PYNQ 为推荐方向], [报告明确实际使用 Linux/PetaLinux C++ PS + HLS PL，不写成 PYNQ 项目]),
  ([性能表述], [“不体现性能收益，技术点放在 PS 与 PL 协作。”], [说明数据通路、接口、DMA 和分层验证], [保留 Round20 的条件与原始耗时，不依据两段样本宣称稳定加速]),
  ([结果裁定], [用户确认 Round9 五项指标、Round10 主观音色和原始听感通过], [将这些结果与 Round23/30 板端证据分层记录], [不把音色验收、有限时实时运行、重启持久启动混成同一个测试结论]),
  ([提交整理], [“总代码只关于在板子最终实现的那个版本。”], [逐项检查编译脚本引用、补齐最终路径所需源码和 RTL], [收敛构建入口到 Round30 的最小相位 PL 路径，补入缺失的 HLS/驱动探针源码]),
))


= 六、技能包的提炼过程


技能包从项目中的可核查观察提炼，分别说明适用范围、操作方法、失效条件和证据。它们不替代目标器件上的新一轮仿真、实现或上板检查。

#report-table((1.0fr, 2.6fr, 2.4fr, 2.6fr), [技能包提炼与适用边界], (
  ([技能], [观察与提炼规则], [项目内验证], [适用范围与边界]),
  ([板级 bring-up], [先确认器件、系统状态、启动基线和恢复路径，再开始现场动作], [Round30 重启后候选就绪、PCM 运行、原始启动文件哈希匹配], [适用于有明确板级恢复流程的 Zynq Linux 工程；换镜像或板卡须重新核实]),
  ([DMA coherency], [明确 CPU/设备缓冲区所有权、地址、对齐、同步、超时和恢复语义], [Round20 24 向量板端对照和驱动调用统计], [适用于 Linux coherent-DMA；迁移到其他驱动/缓存策略需重验]),
  ([Golden compare], [固定输入和软件参考，报告误差、调用、fallback 与超时], [Round16 RTL 24 向量、Round20 板端向量和文件回归], [数值误差门通过不代表主观音质通过]),
  ([Vivado MCP / GitHub], [以 Tcl 和日志为构建入口，按任务编号记录提交，PR 核对变更和证据], [本项目 Vivado/HLS 脚本、Round17/18 报告及协作记录], [MCP 会话与 GitHub 策略依赖具体环境，迁移时需核验版本和权限]),
  ([PS/PL 提示词流], [按需求划分、实现、验证、现场测试和失败复核顺序组织模型任务], [本项目 Round16-30 的接口与证据链], [模板本身尚无独立团队前向复用记录；不能把提示词输出当作验证结果]),
))


技能原始文件位于 #code("skill/")。测试流程保留有效语音帧检查、Round29/30 进程归属确认和 PCM 释放处理，保证验收结论对应实际运行状态。

= 七、复现说明


== 7.1 主机端构建


+ 克隆本仓库并核对源实现基线与当前提交。安装 Vivado/Vitis HLS 2026.1、#code("xc7z020clg400-2") 器件库和对应 ARM hard-float 交叉编译器。
+ 获取 WORLD 0.3.5 源码。构建脚本核对 #code("src/common.cpp") SHA-256；将 #code("WORLD_HLS_PROJECT") 指向短路径。
+ 依次运行 #code("build/probe_world_minphase_hls.tcl") 创建 HLS 工程并综合，#code("build/cosim_world_minphase_hls.tcl") 执行 C/RTL 验证，再运行 #code("build/impl_world_minphase_hls.tcl") 导出 IP。
+ 设置 #code("WORLD_MINPHASE_IP_REPO") 和 #code("WORLD_MINPHASE_PROJECT")，运行 #code("build/create_world_exp_20261027.tcl -tclargs minphase") 生成整机工程，再运行 #code("build/implement_world_minphase_20261029.tcl") 执行综合、实现和报告导出。
+ 运行 #code("build/build_world_minphase.ps1 -WorldRoot <WORLD目录> -Target arm -Compiler <ARM-G++> -MinphasePl") 构建板端 PS 程序和最小相位 DMA 探针。省略 #code("-MinphasePl") 可构建 CPU 软件参考。
+ 使用与目标板内核完全匹配的 PetaLinux kernel source/build 目录，运行 #code("build/build_world_minphase_driver.sh") 构建 Linux 驱动。

== 7.2 板端运行与验收


板端环境为野火 PetaLinux 2022.2。PetaLinux SDK 获取入口为 #link("https://www.amd.com/zh-cn/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html")[AMD 官方 PetaLinux 页面]。将生成的驱动、PS 程序、HLS/PL 位流及配置按 #code("board/") 内 manifest、安装和恢复说明部署。任何写启动配置的动作前都要核对板卡身份、工厂文件 SHA-256 和回退条件；录音、播放或试听需由现场操作者确认准备。

== 7.3 回归命令和证据


#raw("python -m unittest sim.test_world_minphase_boot -v\npython metrics/scripts/validate_metrics.py\nsh -n board/world_minphase_autostart.sh board/world_minphase_init.sh board/world_minphase_control.sh", block: true)


数值核结果见 Round16/17/18/20 报告，Round23 记录 20 秒有效语音运行，Round30 记录正常重启后的 #code("READY_CANDIDATE")、采集/播放 PCM 状态和 PL 调用增长。Round9/10 的音色验收按项目最终确认信息列示：身份、P10、泄漏、UTMOS、CER 分别为 #code("0.5200")、#code("0.4719")、#code("0.0591")、#code("3.0789")、#code("0.1020")；Round10 主观音色与原始听感通过。

按项目最终验收口径，Round23 的有效语音运行记录与 Round30 的重启后持续调用和双 PCM 运行记录作为实时性、稳定性及启动通过的依据。报告中的数值严格对应原始记录；本项目不将未采集的 P95/P99 值写成实测数据。
