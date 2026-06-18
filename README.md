# project-individual: Computer Use Time and Sleep Hours ANOVA

## Members
**111370210 李采軒**

---

## Research Question

Do high school students with different levels of computer use time have different average sleep hours?

- **Grouping variable:** `ComputerUse`  
- **Response variable:** `Sleep`  
- **Method:** One-way ANOVA  
- **Post-hoc test:** Tukey HSD  

---

## Project Structure

```text
PROJECT-INDIVIDUAL/
└── project-individual/
    ├── data/
    │   ├── raw/
    │   │   └── YRBS_2007.csv
    │   └── processed/
    │
    ├── notebooks/
    │   ├── 01_data_processing.py
    │   └── 02_anova_analysis.py
    │
    ├── outputs/
    │   ├── figures/
    │   ├── tables/
    │   └── summary/
    │
    ├── references/
    │   └── source_note.txt
    │
    ├── report/
    │   └── cycle individual anova summary.png
    │
    ├── .gitignore
    ├── README.md
    └── requirements.txt

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

## 結論

本研究使用單因子 ANOVA 分析不同電腦使用時間組別與睡眠時數之間的差異。

結果顯示：

不同電腦使用時間組別之間的平均睡眠時數存在統計上顯著差異（p < .05）
整體趨勢顯示：電腦使用時間較長的組別，其平均睡眠時數較低
然而效果量（η²）較小，表示實際影響程度有限

因此，電腦使用時間與睡眠時數之間呈現「弱但顯著」的關聯。

## 解讀注意事項

1. ANOVA 只能顯示組別平均數是否有差異。
2. 不能直接說電腦使用「造成」睡眠變少。
3. 樣本數很大時，小差異也可能達到統計顯著。
4. 應同時報告平均數、95% 信賴區間與效果量。
5. YRBS 是複雜抽樣資料；本專案採一般未加權 ANOVA，適合作為課堂教學版本。
