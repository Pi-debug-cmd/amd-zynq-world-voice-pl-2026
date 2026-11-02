# 指标说明

`metrics.csv` 是竞赛格式的精简测量结果和验收门槛索引。每个数据项都链接到 `report/` 中的对应技术证据。根据用户确认，稳定性和延迟依据已有 Round23 实时测试与 Round30 持久启动证据标记为通过；Round24 没有有效语音，因此不纳入判定。

运行以下命令，检查 CSV 格式及所有证据路径是否存在：

```sh
python data/metrics/scripts/validate_metrics.py
```

历史报告保留每轮测试的准确范围。项目层面的验收依据是 Round23 和 Round30 证据的组合，不会改写各轮原始测试记录。
