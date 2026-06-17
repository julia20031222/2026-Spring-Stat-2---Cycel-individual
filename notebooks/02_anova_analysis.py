from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


# ============================================================
# 專案路徑設定
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "computer_sleep_clean.csv"
)

TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"
SUMMARY_DIR = PROJECT_ROOT / "outputs" / "summary"


# ============================================================
# 電腦使用時間的正確順序
# ============================================================

GROUP_ORDER = [
    "0 小時",
    "少於 1 小時",
    "1 小時",
    "2 小時",
    "3 小時",
    "4 小時",
    "5 小時以上",
]


# ============================================================
# 中文字型設定
# ============================================================

def setup_chinese_font() -> None:
    """
    自動尋找電腦中可用的中文字型，
    避免 Matplotlib 中文顯示成方框。
    """

    candidate_fonts = [
        "Microsoft JhengHei",
        "Microsoft YaHei",
        "Noto Sans CJK TC",
        "Noto Sans TC",
        "PingFang TC",
        "Heiti TC",
        "Arial Unicode MS",
        "SimHei",
    ]

    available_fonts = {
        font.name
        for font in font_manager.fontManager.ttflist
    }

    for font_name in candidate_fonts:
        if font_name in available_fonts:
            plt.rcParams["font.family"] = font_name
            plt.rcParams["axes.unicode_minus"] = False

            print(f"使用中文字型：{font_name}")
            return

    # Windows 常見字型檔案的備援方案
    windows_font_paths = [
        Path("C:/Windows/Fonts/msjh.ttc"),
        Path("C:/Windows/Fonts/msjhbd.ttc"),
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/msyhbd.ttc"),
    ]

    for font_path in windows_font_paths:
        if font_path.exists():
            font_manager.fontManager.addfont(str(font_path))

            font_property = font_manager.FontProperties(
                fname=str(font_path)
            )
            font_name = font_property.get_name()

            plt.rcParams["font.family"] = font_name
            plt.rcParams["axes.unicode_minus"] = False

            print(f"使用中文字型檔案：{font_path}")
            print(f"字型名稱：{font_name}")
            return

    print("警告：找不到中文字型，圖表中文可能顯示成方框。")
    print("建議確認 Windows 是否有微軟正黑體。")


# ============================================================
# 計算 Eta Squared 效果量
# ============================================================

def eta_squared(df: pd.DataFrame) -> float:
    """
    計算單因子 ANOVA 的 eta squared 效果量。
    """

    overall_mean = df["sleep_hours"].mean()

    ss_between = sum(
        len(group)
        * (
            group["sleep_hours"].mean()
            - overall_mean
        ) ** 2
        for _, group in df.groupby(
            "computer_use_group",
            observed=False,
        )
    )

    ss_total = (
        (
            df["sleep_hours"]
            - overall_mean
        ) ** 2
    ).sum()

    return float(ss_between / ss_total)


# ============================================================
# 主程式
# ============================================================

def main() -> None:
    # 設定中文字型
    setup_chinese_font()

    # 建立輸出資料夾
    TABLE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    FIGURE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    SUMMARY_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # 步驟 1：讀取處理後資料
    # --------------------------------------------------------

    print("=" * 60)
    print("步驟 1：讀取處理後資料")
    print("=" * 60)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"找不到處理後資料：{DATA_FILE}\n"
            "請先執行 src/01_data_processing.py"
        )

    df = pd.read_csv(DATA_FILE)

    # 將分組變數重新設定成有順序的類別
    # CSV 不會保留 pandas categorical 的順序，
    # 所以讀取後必須重新指定。
    df["computer_use_group"] = pd.Categorical(
        df["computer_use_group"],
        categories=GROUP_ORDER,
        ordered=True,
    )

    # 移除不在合法類別中的資料
    df = df.dropna(
        subset=[
            "computer_use_group",
            "sleep_hours",
        ]
    ).copy()

    print(f"有效樣本數：{len(df):,}")

    print("\n資料前 5 列：")
    print(
        df.head().to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # 步驟 2：描述統計
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("步驟 2：描述統計")
    print("=" * 60)

    descriptive = (
        df.groupby(
            "computer_use_group",
            observed=False,
        )["sleep_hours"]
        .agg(
            n="count",
            mean="mean",
            std="std",
            median="median",
        )
        .reset_index()
    )

    # 計算標準誤
    descriptive["se"] = (
        descriptive["std"]
        / np.sqrt(descriptive["n"])
    )

    # 計算 95% 信賴區間
    descriptive["ci95_lower"] = (
        descriptive["mean"]
        - 1.96 * descriptive["se"]
    )

    descriptive["ci95_upper"] = (
        descriptive["mean"]
        + 1.96 * descriptive["se"]
    )

    print(
        descriptive
        .round(3)
        .to_string(index=False)
    )

    descriptive.to_csv(
        TABLE_DIR
        / "descriptive_statistics.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # --------------------------------------------------------
    # 步驟 3：ANOVA 前提檢查
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("步驟 3：ANOVA 前提檢查")
    print("=" * 60)

    groups = [
        group["sleep_hours"].to_numpy()
        for _, group in df.groupby(
            "computer_use_group",
            observed=False,
        )
        if len(group) > 0
    ]

    levene = stats.levene(
        *groups,
        center="median",
    )

    print(
        f"Levene 檢定："
        f"W = {levene.statistic:.4f}, "
        f"p = {levene.pvalue:.6g}"
    )

    if levene.pvalue < 0.05:
        print(
            "解讀：各組變異數可能不完全相等，"
            "需保守解讀傳統 ANOVA。"
        )
    else:
        print(
            "解讀：沒有足夠證據認為"
            "各組變異數不同。"
        )

    # --------------------------------------------------------
    # 步驟 4：單因子 ANOVA
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("步驟 4：單因子 ANOVA")
    print("=" * 60)

    anova = stats.f_oneway(*groups)

    eta2 = eta_squared(df)

    number_of_groups = len(groups)
    df_between = number_of_groups - 1
    df_within = len(df) - number_of_groups

    print(f"F = {anova.statistic:.4f}")
    print(f"p = {anova.pvalue:.6g}")
    print(f"自由度 = ({df_between}, {df_within})")
    print(f"eta squared = {eta2:.4f}")

    if anova.pvalue < 0.05:
        conclusion = (
            "不同電腦使用時間組別的平均睡眠時數"
            "存在統計上顯著差異。"
        )
    else:
        conclusion = (
            "沒有足夠證據顯示不同電腦使用時間組別的"
            "平均睡眠時數存在差異。"
        )

    print(f"結論：{conclusion}")

    print(
        "提醒：統計顯著不代表差異很大，"
        "仍需搭配效果量與各組平均數判讀。"
    )

    anova_table = pd.DataFrame(
        [
            {
                "df_between": df_between,
                "df_within": df_within,
                "F": anova.statistic,
                "p_value": anova.pvalue,
                "eta_squared": eta2,
                "n": len(df),
            }
        ]
    )

    anova_table.to_csv(
        TABLE_DIR / "anova_result.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # --------------------------------------------------------
    # 步驟 5：Tukey HSD 事後比較
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("步驟 5：Tukey HSD 事後比較")
    print("=" * 60)

    # Tukey 使用文字形式的組別，
    # 避免 categorical 類型造成顯示問題。
    tukey_groups = (
        df["computer_use_group"]
        .astype("string")
    )

    tukey = pairwise_tukeyhsd(
        endog=df["sleep_hours"],
        groups=tukey_groups,
        alpha=0.05,
    )

    print(tukey)

    tukey_df = pd.DataFrame(
        tukey.summary().data[1:],
        columns=tukey.summary().data[0],
    )

    tukey_df.to_csv(
        TABLE_DIR / "tukey_hsd.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # --------------------------------------------------------
    # 步驟 6：繪製平均數與 95% 信賴區間
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("步驟 6：繪圖")
    print("=" * 60)

    plot_df = descriptive.copy()

    # 移除沒有資料的類別
    plot_df = plot_df[
        plot_df["n"] > 0
    ].copy()

    plt.figure(
        figsize=(12, 7)
    )

    plt.errorbar(
        plot_df["computer_use_group"].astype(str),
        plot_df["mean"],
        yerr=1.96 * plot_df["se"],
        fmt="o-",
        capsize=5,
        linewidth=2,
        markersize=7,
    )

    plt.xlabel(
        "每天非課業電腦／電玩使用時間",
        fontsize=12,
    )

    plt.ylabel(
        "平均睡眠時數",
        fontsize=12,
    )

    plt.title(
        "不同電腦使用時間組別的平均睡眠時數（95% CI）",
        fontsize=15,
        pad=15,
    )

    plt.xticks(
        rotation=25,
        ha="right",
    )

    plt.grid(
        axis="y",
        alpha=0.25,
    )

    plt.tight_layout()

    figure_path = (
        FIGURE_DIR
        / "computer_use_sleep_mean_ci.png"
    )

    plt.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"圖表已儲存：{figure_path}")

    # --------------------------------------------------------
    # 步驟 7：輸出文字摘要
    # --------------------------------------------------------

    summary = f"""研究題目：
不同非課業電腦使用時間的高中生，其平均睡眠時數是否存在差異？

有效樣本數：{len(df):,}

單因子 ANOVA：
F({df_between}, {df_within}) = {anova.statistic:.4f}
p = {anova.pvalue:.6g}
eta squared = {eta2:.4f}

Levene 變異數同質性檢定：
W = {levene.statistic:.4f}
p = {levene.pvalue:.6g}

結論：
{conclusion}

注意事項：
1. ComputerUse 與 Sleep 都來自學生自陳問卷。
2. Sleep 的「4 小時以下」與「10 小時以上」分別近似編碼為 4 與 10。
3. 本分析只能顯示變數之間的關聯，不能推論電腦使用造成睡眠改變。
4. YRBS 是複雜抽樣資料；本教學採用一般未加權單因子 ANOVA。
5. 樣本數較大時，小幅差異也可能達到統計顯著，需同時參考效果量。
"""

    summary_path = (
        SUMMARY_DIR
        / "analysis_summary.txt"
    )

    summary_path.write_text(
        summary,
        encoding="utf-8",
    )

    print(f"分析摘要已儲存：{summary_path}")

    print("\n" + "=" * 60)
    print("分析完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
