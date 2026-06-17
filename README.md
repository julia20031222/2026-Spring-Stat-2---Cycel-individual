# project-individual：電腦使用時間與睡眠時數 ANOVA

## 研究問題

不同「非課業電腦／電玩使用時間」的高中生，其平均睡眠時數是否存在差異？

- 分組變數：`ComputerUse`
- 結果變數：`Sleep`
- 方法：單因子 ANOVA
- 事後比較：Tukey HSD

## 專案結構

```text
project-individual/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── YRBS_2007.csv
│   └── processed/
├── notebooks/
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── summary/
├── report/
├── references/
└── src/
    ├── 01_data_processing.py
    ├── 02_anova_analysis.py
    └── run_all.py
```

## 1. 開啟終端機並進入專案

```bash
cd project-individual
```

## 2. 建立虛擬環境

Windows：

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. 安裝套件

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. 執行資料處理

```bash
python src/01_data_processing.py
```

終端機會印出：

- 原始資料筆數
- 缺失值數量
- 原始次數分配
- 清理後有效樣本數
- 各組樣本數
- 清理後資料前 10 列

處理後檔案會出現在：

```text
data/processed/computer_sleep_clean.csv
outputs/summary/data_processing_summary.txt
```

## 5. 執行 ANOVA

```bash
python src/02_anova_analysis.py
```

終端機會印出：

- 描述統計
- Levene 變異數同質性檢定
- 單因子 ANOVA
- eta squared 效果量
- Tukey HSD 事後比較
- 輸出檔案位置

## 6. 一次執行全部流程

```bash
python src/run_all.py
```

## 7. 查看輸出

```text
outputs/
├── figures/
│   └── computer_use_sleep_mean_ci.png
├── tables/
│   ├── descriptive_statistics.csv
│   ├── anova_result.csv
│   └── tukey_hsd.csv
└── summary/
    ├── data_processing_summary.txt
    └── analysis_summary.txt
```

## 編碼說明

### ComputerUse

| 原始代碼 | 分組 |
|---:|---|
| 1 | 0 小時 |
| 2 | 少於 1 小時 |
| 3 | 1 小時 |
| 4 | 2 小時 |
| 5 | 3 小時 |
| 6 | 4 小時 |
| 7 | 5 小時以上 |

### Sleep

| 原始代碼 | 分析用時數 |
|---:|---:|
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |
| 4 | 7 |
| 5 | 8 |
| 6 | 9 |
| 7 | 10 |

兩端是開放區間：「4 小時以下」與「10 小時以上」。本教學為方便 ANOVA，分別近似為 4 與 10 小時。

## 報告中可使用的假設

- H0：不同電腦使用時間組別的平均睡眠時數相同。
- H1：至少一個電腦使用時間組別的平均睡眠時數不同。

## 解讀注意事項

1. ANOVA 只能顯示組別平均數是否有差異。
2. 不能直接說電腦使用「造成」睡眠變少。
3. 樣本數很大時，小差異也可能達到統計顯著。
4. 應同時報告平均數、95% 信賴區間與效果量。
5. YRBS 是複雜抽樣資料；本專案採一般未加權 ANOVA，適合作為課堂教學版本。
