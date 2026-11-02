# 数据与指标

本目录包含本次提交使用的精简文本测量索引，不包含人声、生成音频、模型权重及其他受控或生成数据。

- `metrics/metrics.csv` 将各项结果摘要链接到 `report/` 中的对应报告。
- `metrics/scripts/validate_metrics.py` 检查 CSV 格式，并验证所引用的证据报告均存在。

在仓库根目录运行校验脚本：

```sh
python data/metrics/scripts/validate_metrics.py
```
