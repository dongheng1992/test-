# Water Quality Simulator

该项目提供一个简单的“进水 → 出水水质模拟”小程序，使用可配置的经验去除率模型，快速估算出水 COD、NH4-N、TN。

## 功能说明

- 支持命令行参数输入：`COD_in`、`NH4N_in`、`TN_in`
- 无参数时自动进入交互输入
- 去除率参数存放在 `config.json`

## 运行方式

```bash
python water_quality_simulator.py --COD_in 300 --NH4N_in 40 --TN_in 60
```

若不提供参数，则会提示交互输入：

```bash
python water_quality_simulator.py
```

## 示例输出

```
=== 进水 -> 出水水质模拟结果 ===
COD_in  : 300.00 mg/L
NH4N_in : 40.00 mg/L
TN_in   : 60.00 mg/L
---
COD_out : 195.00 mg/L
NH4N_out: 22.00 mg/L
TN_out  : 42.00 mg/L
```

## 配置参数

`config.json` 中的 `removal_rates` 为去除率（0~1），可根据工艺调整。
