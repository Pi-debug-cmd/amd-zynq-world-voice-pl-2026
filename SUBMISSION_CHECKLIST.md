# AMD 自主选题赛道提交核对表

依据《FPGA 创新设计赛道选题指南（AMD）》第 3.3.2 至 3.3.5 节。项目按 Round30 最终板上实现组织；本表用于定位材料和核对工程内容。

| 官方要求 | 提交材料 | 核对位置 |
| --- | --- | --- |
| 声明器件型号并完成板级验证 | Wildfire Zynq-7020，`xc7z020clg400-2` | `README.md`、`docs/hardware_setup.md`、Round23/30 报告 |
| 完整工程源码，按实际实现方式提交 | HLS、PS、Linux 驱动、RTL、Vivado/HLS 脚本 | `src/`、`build/`、`board/` |
| 仿真或验证结果 | 24 组 WORLD 参考向量、板端数值对照、运行态检查 | `sim/`、`report/`、`metrics/` |
| 综合与实现报告、资源、时钟和性能数据 | 核级 OOC 与整机实现摘要；板端测试条件和运行数据 | `report/world_minphase_ooc_round17_20261029.md`、`report/world_minphase_integration_round18_20261029.md`、`metrics/metrics.csv` |
| 上板工程、运行脚本、实测输出与参考结果对比 | 安装/启动/恢复脚本、24 向量与两段文件数值比较、Round23 实时运行和 Round30 开机记录 | `board/`、Round20/23/30 报告 |
| 可复现构建脚本 | HLS、Vivado、ARM 与驱动构建入口，外部依赖及步骤 | `build/`、`docs/reproduction.md` |
| Skill 包及适用范围、方法、失效条件和项目证据 | 板级启动、DMA 一致性、黄金参考、Vivado MCP/GitHub、PS/PL 提示词流 | `skill/` |
| 设计报告规定章节 | 背景与创新、功能框图、软硬件划分、优化对比、AI 协作、Skill 提炼、复现步骤 | `report/DESIGN_REPORT.md`、`docs/design_report.pdf` |
| 大模型协作记录 | 需求提示、模型决策摘要、纠错与证据链接 | `docs/ai_collaboration.md` |
| 开源协议 | MIT 项目代码许可及第三方许可边界 | `LICENSE`、`src/ps/world_v23/LICENSE.txt` |
| 仓库路径/文件名使用英文 | 英文目录和文件名，正文允许中文 | 仓库树 |

提交清单说明：AMD 第 3.3.5 节要求可复现的工程、源码、报告、上板运行脚本和测量证据；没有将 `.xsa` 或 PetaLinux 镜像列为独立文件格式要求。仓库内的供应商基础 XSA 属于原始野火工程输入，不是 Round30 导出平台。当前不提供 Round30 重新导出的 `.bit/.xsa` 和 PetaLinux 镜像，复现者按 `docs/reproduction.md` 使用给定工具/源码及官方 PetaLinux 获取入口生成或获取所需运行环境。摘要与关键文件 SHA-256 见 `report/submission_manifest_round30_20261103.json`。

## 实现边界

最终板上数据通路由 PS 运行 WORLD 主流程和音频 I/O，PL 执行其中固定 1024 点的融合最小相位频谱计算。代码包不把该核描述为完整 WORLD 算法，也不把少量文件测试的墙钟差异当作系统性能收益。

Round9/10 音色验收、Round23 有效语音运行和 Round30 持久启动是不同验收环节，报告分别列出其证据来源和数据范围。当前项目验收结论依据用户指定的已有通过记录；数值只按对应日志实际记录，不补造未采集的延迟分位数或测试时长。

Vivado 生成物、板端 PetaLinux 镜像和运行二进制由复现者按说明获取或生成，不作为源码归档内容。该处理不改变已保存的板端验收记录。
