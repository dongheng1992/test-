import argparse
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class InfluentQuality:
    """进水水质参数（单位：mg/L）。"""

    cod: float
    nh4n: float
    tn: float


@dataclass
class RemovalConfig:
    """去除率参数（0-1 之间）。"""

    cod: float
    nh4n: float
    tn: float


@dataclass
class EffluentQuality:
    """出水水质参数（单位：mg/L）。"""

    cod: float
    nh4n: float
    tn: float


def load_config(config_path: str) -> RemovalConfig:
    """读取配置文件中的去除率参数。"""
    path = Path(config_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    removal = data.get("removal_rates", {})
    return RemovalConfig(
        cod=float(removal.get("COD", 0.0)),
        nh4n=float(removal.get("NH4N", 0.0)),
        tn=float(removal.get("TN", 0.0)),
    )


def validate_removal_rates(config: RemovalConfig) -> None:
    """校验去除率范围。"""
    for name, value in (("COD", config.cod), ("NH4N", config.nh4n), ("TN", config.tn)):
        if not 0 <= value <= 1:
            raise ValueError(f"{name} 去除率需在 0~1 之间，当前为 {value}")


def validate_influent(influent: InfluentQuality) -> None:
    """校验进水参数为非负值。"""
    for name, value in (("COD", influent.cod), ("NH4N", influent.nh4n), ("TN", influent.tn)):
        if value < 0:
            raise ValueError(f"{name} 进水浓度不能为负值，当前为 {value}")


def simulate_effluent(influent: InfluentQuality, config: RemovalConfig) -> EffluentQuality:
    """
    简化模型假设：
    1) 采用经验去除率表示处理工艺的总体去除效果；
    2) 出水 = 进水 × (1 - 去除率)，不考虑水量变化或反应动力学差异。
    """
    return EffluentQuality(
        cod=influent.cod * (1 - config.cod),
        nh4n=influent.nh4n * (1 - config.nh4n),
        tn=influent.tn * (1 - config.tn),
    )


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="进水到出水水质模拟器（简化模型）")
    parser.add_argument("--cod", type=float, help="进水 COD (mg/L)")
    parser.add_argument("--nh4n", type=float, help="进水 NH4-N (mg/L)")
    parser.add_argument("--tn", type=float, help="进水 TN (mg/L)")
    parser.add_argument("--config", default="config.json", help="配置文件路径")
    return parser.parse_args()


def prompt_for_value(label: str) -> float:
    """交互式读取进水参数。"""
    while True:
        raw = input(f"请输入 {label} (mg/L): ").strip()
        try:
            value = float(raw)
        except ValueError:
            print("输入无效，请输入数字。")
            continue
        if value < 0:
            print("数值不能为负，请重新输入。")
            continue
        return value


def get_influent_from_inputs(args: argparse.Namespace) -> InfluentQuality:
    """从命令行参数或交互输入获取进水参数。"""
    cod = args.cod if args.cod is not None else prompt_for_value("COD")
    nh4n = args.nh4n if args.nh4n is not None else prompt_for_value("NH4-N")
    tn = args.tn if args.tn is not None else prompt_for_value("TN")
    return InfluentQuality(cod=cod, nh4n=nh4n, tn=tn)


def print_effluent(effluent: EffluentQuality) -> None:
    """输出出水结果。"""
    print("模拟出水水质（mg/L）：")
    print(f"COD_out: {effluent.cod:.2f}")
    print(f"NH4N_out: {effluent.nh4n:.2f}")
    print(f"TN_out: {effluent.tn:.2f}")


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    validate_removal_rates(config)

    influent = get_influent_from_inputs(args)
    validate_influent(influent)

    effluent = simulate_effluent(influent, config)
    print_effluent(effluent)


if __name__ == "__main__":
    main()
