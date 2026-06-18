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

## Report Hypotheses

- H0: The mean sleep hours are the same across different computer use time groups.
- H1: At least one computer use time group has a different mean sleep duration.
  
## Conclusion

This study used one-way ANOVA to analyze differences between computer use time groups and sleep duration.

The results show:

There is a statistically significant difference in mean sleep hours across computer use time groups (p < .05).
The overall trend shows that groups with higher computer use time tend to have lower average sleep hours.
However, the effect size (η²) is small, indicating that the practical impact is limited.

Therefore, the relationship between computer use time and sleep hours is weak but statistically significant.

## Interpretation Notes
1. ANOVA only indicates whether group means differ.
2. It does not imply that computer use causes changes in sleep duration.
3. With large sample sizes, small differences may still be statistically significant.
4. Mean values, 95% confidence intervals, and effect sizes should be reported together.
5. YRBS is a complex survey dataset; this project uses an unweighted ANOVA as a classroom-level analysis.
