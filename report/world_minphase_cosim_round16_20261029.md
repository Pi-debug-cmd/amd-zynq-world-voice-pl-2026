# WORLD 最小相位融合 Round16 RTL 协同仿真

任务 `PL-20261027-01`，Hardware-A / Codex，2026-10-29。本轮继续 2026-10-27 暂停的短路径工程；未操作板卡或音频服务。

## 结果

Vitis HLS 2026.1 为 `xc7z020clg400-2` 生成 Verilog，XSIM 完成全部 24 组 WORLD 黄金样例。C 后处理检查得到最大相对 L2 误差 `8.53141669198e-7`，结果为 `passed=true`。生成的协同仿真报告记录为 `Pass`，延迟 `32231..32232` 个周期，启动间隔 `32245..32246` 个周期，24 次事务总计 `773889` 个周期。

HLS 估算结果为：目标频率 100 MHz、估算时钟周期 7.300 ns、10007 LUT、7732 FF、8 个 BRAM18K 和 38 个 DSP。这些是综合估算值，不是整机布线结果。

## 复现

```powershell
$env:WORLD_HLS_PROJECT='D:/wpl_20261027_r16/m'
& 'D:/USER_Software/vivado/2026.1/Vitis/bin/vitis-run.bat' --mode hls --tcl --input_file 'build/generated/run_minphase_cosim_round15.tcl'
```

被忽略的包装脚本将 WORLD 0.3.5 源码参数设为 `C:/Users/World/Desktop/2026_FPGA/build/generated/world_source_v035/pyworld-0.3.5/lib/World`，并加载 `build/cosim_world_minphase_hls.tcl`。所需源码哈希和生成报告哈希记录在相邻 JSON 文件中。

## 剩余风险

XSIM 依赖监视器针对显式 `DEPENDENCE inter false` 指令后可能重叠的地址发出了 6720 条警告。24 组数值测试通过，因此目前没有证据表明存在数据错误，但这仍是签核风险，必须在报告中保留。下一阶段是 OOC 实现以及布线时序/资源检查；当时尚不适合加载到板卡。

本轮没有录音、播放、试听、加载位流、修改启动配置或进行板端测试。
