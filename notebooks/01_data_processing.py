from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "YRBS_2007.csv"
PROCESSED_FILE = PROJECT_ROOT / "data" / "processed" / "computer_sleep_clean.csv"
SUMMARY_FILE = PROJECT_ROOT / "outputs" / "summary" / "data_processing_summary.txt"

COMPUTER_LABELS = {
    1: "0 小時",
    2: "少於 1 小時",
    3: "1 小時",
    4: "2 小時",
    5: "3 小時",
    6: "4 小時",
    7: "5 小時以上",
}

# 睡眠原始題目是區間。為了進行 ANOVA，將兩端開放區間近似為 4 與 10 小時。
SLEEP_HOURS = {
    1: 4,
    2: 5,
    3: 6,
    4: 7,
    5: 8,
    6: 9,
    7: 10,
}


def main() -> None:
    print("=" * 60)
    print("步驟 1：讀取原始資料")
    print("=" * 60)

    df = pd.read_csv(RAW_FILE)
    print(f"原始資料筆數：{len(df):,}")
    print(f"原始欄位數：{df.shape[1]}")
    print("本次使用欄位：ComputerUse、Sleep")

    selected = df[["ComputerUse", "Sleep"]].copy()

    print("\n原始缺失值數量：")
    print(selected.isna().sum())

    print("\nComputerUse 原始次數分配：")
    print(selected["ComputerUse"].value_counts(dropna=False).sort_index())

    print("\nSleep 原始次數分配：")
    print(selected["Sleep"].value_counts(dropna=False).sort_index())

    print("\n" + "=" * 60)
    print("步驟 2：清理與重新編碼")
    print("=" * 60)

    clean = selected.dropna().copy()
    clean["ComputerUse"] = clean["ComputerUse"].astype(int)
    clean["Sleep"] = clean["Sleep"].astype(int)

    # 僅保留合法代碼
    clean = clean[
        clean["ComputerUse"].isin(COMPUTER_LABELS)
        & clean["Sleep"].isin(SLEEP_HOURS)
    ].copy()

    clean["computer_use_group"] = clean["ComputerUse"].map(COMPUTER_LABELS)
    clean["sleep_hours"] = clean["Sleep"].map(SLEEP_HOURS)

    order = list(COMPUTER_LABELS.values())
    clean["computer_use_group"] = pd.Categorical(
        clean["computer_use_group"],
        categories=order,
        ordered=True,
    )

    # 保留可追溯的原始代碼與分析用欄位
    clean = clean[
        ["ComputerUse", "Sleep", "computer_use_group", "sleep_hours"]
    ]

    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    clean.to_csv(PROCESSED_FILE, index=False, encoding="utf-8-sig")

    print(f"清理後有效樣本數：{len(clean):,}")
    print(f"刪除筆數：{len(selected) - len(clean):,}")
    print(f"處理後資料已儲存：{PROCESSED_FILE}")

    print("\n清理後各組樣本數：")
    group_counts = (
        clean.groupby("computer_use_group", observed=False)
        .size()
        .rename("n")
    )
    print(group_counts)

    summary_text = "\n".join([
        "資料處理摘要",
        f"原始樣本數：{len(df):,}",
        f"分析有效樣本數：{len(clean):,}",
        f"刪除筆數：{len(selected) - len(clean):,}",
        "",
        "各組樣本數：",
        group_counts.to_string(),
    ])
    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_FILE.write_text(summary_text, encoding="utf-8")

    print("\n資料前 10 列：")
    print(clean.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
