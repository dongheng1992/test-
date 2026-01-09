#!/usr/bin/env python3
"""Water quality simulator for influent to effluent conversion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

CONFIG_PATH = Path(__file__).with_name("config.json")


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Dict[str, float]]:
    """读取配置文件并返回配置字典。"""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_args() -> argparse.Namespace:
    """解析命令行参数，允许用户直接提供进水浓度。"""
    parser = argparse.ArgumentParser(description="Influent to effluent water quality simulator")
    parser.add_argument("--COD_in", type=float, help="Influent COD (mg/L)")
    parser.add_argument("--NH4N_in", type=float, help="Influent NH4-N (mg/L)")
    parser.add_argument("--TN_in", type=float, help="Influent TN (mg/L)")
    return parser.parse_args()


def prompt_for_value(label: str) -> float:
    """交互式提示用户输入数值，直到输入合法。"""
    while True:
        raw = input(f"请输入 {label} (mg/L): ").strip()
        try:
            return float(raw)
        except ValueError:
            print("输入无效，请输入数字。")


def get_inputs(args: argparse.Namespace) -> Dict[str, float]:
    """汇总进水参数，缺失值通过交互式输入补齐。"""
    values = {
        "COD_in": args.COD_in,
        "NH4N_in": args.NH4N_in,
        "TN_in": args.TN_in,
    }
    for key, value in list(values.items()):
        if value is None:
            # 命令行未提供的项目转为交互式输入
            values[key] = prompt_for_value(key)
    return values


def simulate(inputs: Dict[str, float], removal_rates: Dict[str, float]) -> Dict[str, float]:
    """根据去除率计算出水浓度。"""
    # 模型假设：进水到出水采用简化的一阶/经验去除率模型，
    # 即出水浓度 = 进水浓度 * (1 - 去除率)。
    # 去除率为经验参数，默认不随时间、温度与水力条件变化。
    return {
        "COD_out": inputs["COD_in"] * (1 - removal_rates["COD"]),
        "NH4N_out": inputs["NH4N_in"] * (1 - removal_rates["NH4N"]),
        "TN_out": inputs["TN_in"] * (1 - removal_rates["TN"]),
    }


def main() -> None:
    """入口函数：读取配置、获取输入并输出模拟结果。"""
    args = parse_args()
    inputs = get_inputs(args)
    config = load_config()
    removal_rates = config.get("removal_rates", {})
    outputs = simulate(inputs, removal_rates)

    print("\n=== 进水 -> 出水水质模拟结果 ===")
    print(f"COD_in  : {inputs['COD_in']:.2f} mg/L")
    print(f"NH4N_in : {inputs['NH4N_in']:.2f} mg/L")
    print(f"TN_in   : {inputs['TN_in']:.2f} mg/L")
    print("---")
    print(f"COD_out : {outputs['COD_out']:.2f} mg/L")
    print(f"NH4N_out: {outputs['NH4N_out']:.2f} mg/L")
    print(f"TN_out  : {outputs['TN_out']:.2f} mg/L")


if __name__ == "__main__":
    main()
