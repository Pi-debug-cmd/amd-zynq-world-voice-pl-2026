# PS/PL 接口说明

## 硬件接口约定

| 项目 | 取值 |
| --- | --- |
| HLS 顶层函数 | `world_minphase` |
| 目标器件 | `xc7z020clg400-2` |
| 输入 | 513 个 `float32` 对数频谱点 |
| 输出 | 513 个 `float32` 实部和 513 个 `float32` 虚部滤波器频点 |
| 变换长度 | 1024 点 |
| 控制寄存器窗口 | `0x43C70000` |
| 指针参数窗口 | `0x43C80000` |
| DDR 通路 | HLS 主接口经 `minphase_mem` 连接至 PS `S_AXI_HP2` |
| 时钟 | PS `FCLK_CLK0`；集成记录中为 100 MHz |
| 完成信号 | HLS 控制/中断；记录路径中的 Linux 驱动使用有界轮询 |
| Linux 接口 | `/dev/world_minphase`，ioctl `WORLD_MINPHASE_PROCESS` |

权威的寄存器和数据包布局见 `src/kernel/world_minphase_ioctl.h`、`src/kernel/world_minphase_dma.c` 和 `src/ps/world_minphase_pl.cpp`。修改实现时不要仅凭本摘要推断寄存器偏移。

## 运行时选择

`WORLD_MINPHASE=cpu` 选择软件实现。`WORLD_MINPHASE=pl` 要求存在 `/dev/world_minphase`；设备打开或 ioctl 调用失败时进程会终止。实现会统计调用、回退、复制、设备处理、解包和互斥锁等待时间。请求的 FFT 长度不是 1024 时会走 CPU 回退路径，并增加回退计数。

端到端音频运行时还依赖源项目中的 WORLD 0.3.5、16 kHz 内部单声道 PCM 处理，以及板卡现有的 ALSA/编解码器配置。记录的物理接口为 ALSA 32 kHz、S24_LE、双声道，运行时会显式进行格式转换。
