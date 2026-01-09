import geopandas as gpd
import matplotlib.pyplot as plt


def load_world_map(shapefile_path: str) -> gpd.GeoDataFrame:
    """加载世界地图的 shapefile 数据。"""
    return gpd.read_file(shapefile_path)


def mark_highlight_countries(
    world: gpd.GeoDataFrame, highlight_countries: list[str]
) -> gpd.GeoDataFrame:
    """为需要高亮的国家添加标记列。"""
    world["highlight"] = world["name"].apply(
        lambda name: "highlight" if name in highlight_countries else "other"
    )
    return world


def plot_world_map(world: gpd.GeoDataFrame, title: str) -> None:
    """绘制世界地图，并高亮指定国家。"""
    fig, ax = plt.subplots(figsize=(10, 6))
    world[world["highlight"] == "highlight"].plot(ax=ax, color="green")
    world[world["highlight"] == "other"].plot(ax=ax, color="lightgrey")
    ax.set_title(title)
    plt.show()


def main() -> None:
    # 设置 shapefile 文件路径（替换为本地下载的文件路径）
    shapefile_path = "D:/path/to/naturalearth_lowres.shp"

    # 读取地图数据
    world = load_world_map(shapefile_path)

    # 定义需要高亮的国家
    highlight_countries = ["United States", "China", "India", "Brazil"]

    # 为高亮国家打标记
    world = mark_highlight_countries(world, highlight_countries)

    # 绘制地图
    plot_world_map(world, "World Map with Highlighted Countries")


if __name__ == "__main__":
    main()
