from dataclasses import dataclass


@dataclass
class InfluentQuality:
    """进水水质参数（单位仅作示例，实际可按需要调整）。"""

    cod: float
    bod: float
    tss: float
    nh3_n: float
    tp: float


@dataclass
class TreatmentEfficiency:
    """处理效率（0-1 之间，代表去除比例）。"""

    cod: float
    bod: float
    tss: float
    nh3_n: float
    tp: float


@dataclass
class EffluentQuality:
    """出水水质参数。"""

    cod: float
    bod: float
    tss: float
    nh3_n: float
    tp: float


def simulate_effluent(
    influent: InfluentQuality, efficiency: TreatmentEfficiency
) -> EffluentQuality:
    """根据进水水质和处理效率模拟出水水质。"""
    return EffluentQuality(
        cod=influent.cod * (1 - efficiency.cod),
        bod=influent.bod * (1 - efficiency.bod),
        tss=influent.tss * (1 - efficiency.tss),
        nh3_n=influent.nh3_n * (1 - efficiency.nh3_n),
        tp=influent.tp * (1 - efficiency.tp),
    )


def main() -> None:
    # 示例进水水质（mg/L）
    influent = InfluentQuality(cod=300.0, bod=150.0, tss=200.0, nh3_n=35.0, tp=4.0)

    # 示例处理效率（去除率）
    efficiency = TreatmentEfficiency(
        cod=0.85, bod=0.9, tss=0.88, nh3_n=0.75, tp=0.6
    )

    # 模拟出水水质
    effluent = simulate_effluent(influent, efficiency)

    print("模拟出水水质（mg/L）：")
    print(f"COD: {effluent.cod:.2f}")
    print(f"BOD: {effluent.bod:.2f}")
    print(f"TSS: {effluent.tss:.2f}")
    print(f"NH3-N: {effluent.nh3_n:.2f}")
    print(f"TP: {effluent.tp:.2f}")


if __name__ == "__main__":
    main()
