# test-

## 水质模拟器

该脚本根据进水水质（COD、NH4-N、TN）与配置文件中的去除率，模拟出水水质。
模型假设为经验去除率模型：出水浓度 = 进水浓度 × (1 - 去除率)。

### 运行方式

#### 命令行参数

```bash
python water_quality_simulator.py --cod 300 --nh4n 35 --tn 45
```

#### 交互输入

```bash
python water_quality_simulator.py
```

### 配置文件

去除率配置位于 `config.json` 中，示例：

```json
{
  "removal_rates": {
    "COD": 0.85,
    "NH4N": 0.75,
    "TN": 0.7
  }
}
```

### 示例输出

```
模拟出水水质（mg/L）：
COD_out: 45.00
NH4N_out: 8.75
TN_out: 13.50
```
