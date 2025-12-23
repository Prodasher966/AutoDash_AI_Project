import numpy as np
import pandas as pd

def generate_insights(df: pd.DataFrame) -> list:
    insights = []

    # -----------------------------
    # Numeric Column Insights
    # -----------------------------
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        series = df[col].dropna()
        if series.empty:
            continue

        mean = series.mean()
        median = series.median()
        skew = series.skew()

        # ---- Skewness Insight ----
        if abs(skew) >= 0.5:
            severity = (
                "info" if abs(skew) < 1
                else "warning" if abs(skew) < 1.5
                else "critical"
            )

            insights.append({
                "title": f"Skewed Distribution in '{col}'",
                "severity": severity,
                "technical": {
                    "method": "Skewness Analysis",
                    "details": f"Skewness = {skew:.2f}",
                    "stats": {
                        "mean": round(mean, 2),
                        "median": round(median, 2)
                    }
                },
                "interpretation": (
                    "The data is asymmetrically distributed, "
                    "which may affect averages and model assumptions."
                )
            })

        # ---- Outlier Insight (IQR) ----
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers = series[(series < q1 - 1.5 * iqr) | (series > q3 + 1.5 * iqr)]
        ratio = len(outliers) / len(series)

        if ratio > 0:
            severity = (
                "info" if ratio < 0.02
                else "warning" if ratio < 0.05
                else "critical"
            )

            insights.append({
                "title": f"Outliers Detected in '{col}'",
                "severity": severity,
                "technical": {
                    "method": "IQR Method",
                    "details": f"{len(outliers)} outliers detected",
                    "stats": {
                        "outlier_ratio": round(ratio * 100, 2)
                    }
                },
                "interpretation": (
                    "Extreme values may distort trends and should be "
                    "reviewed or treated before modeling."
                )
            })

    # -----------------------------
    # Missing Values Insight
    # -----------------------------
    for col in df.columns:
        missing_ratio = df[col].isna().mean()

        if missing_ratio == 0:
            continue

        severity = (
            "info" if missing_ratio < 0.05
            else "warning" if missing_ratio < 0.2
            else "critical"
        )

        insights.append({
            "title": f"Missing Values in '{col}'",
            "severity": severity,
            "technical": {
                "method": "Missing Value Ratio",
                "details": f"{missing_ratio:.2%} values missing",
                "stats": {
                    "missing_percentage": round(missing_ratio * 100, 2)
                }
            },
            "interpretation": (
                "Missing data may reduce reliability. "
                "Consider imputation or exclusion strategies."
            )
        })

    # -----------------------------
    # Categorical Dominance Insight
    # -----------------------------
    cat_cols = df.select_dtypes(exclude="number").columns

    for col in cat_cols:
        value_counts = df[col].value_counts(dropna=True)
        if value_counts.empty:
            continue

        top_ratio = value_counts.iloc[0] / value_counts.sum()

        if top_ratio > 0.8:
            severity = "warning" if top_ratio < 0.95 else "critical"

            insights.append({
                "title": f"Category Dominance in '{col}'",
                "severity": severity,
                "technical": {
                    "method": "Category Ratio",
                    "details": f"Top category = {top_ratio:.2%}",
                    "stats": {
                        "top_category_ratio": round(top_ratio * 100, 2)
                    }
                },
                "interpretation": (
                    "One category dominates the data, which may introduce bias "
                    "in analysis or models."
                )
            })

    return insights

# -----------------------------
# Calculate Health Score
# -----------------------------
def calculate_health_score(insights: list) -> int:
    score = 100

    for insight in insights:
        if insight["severity"] == "info":
            score -= 2
        elif insight["severity"] == "warning":
            score -= 5
        elif insight["severity"] == "critical":
            score -= 10

    return max(score, 0)

# -----------------------------
# Generate Executive Summary
# -----------------------------

def generate_executive_summary(insights: list, health_score: int) -> str:
    if not insights:
        return (
            "The dataset appears clean and well-structured with no major "
            "data quality or distribution issues detected."
        )

    total = len(insights)
    critical = sum(1 for i in insights if i["severity"] == "critical")
    warning = sum(1 for i in insights if i["severity"] == "warning")

    summary = (
        f"This dataset was analyzed automatically and produced {total} key insights. "
    )

    if critical > 0:
        summary += (
            f"{critical} critical issue(s) were identified that may significantly "
            "impact analysis reliability. "
        )

    if warning > 0:
        summary += (
            f"{warning} warning-level patterns were observed that require attention "
            "before deeper analysis. "
        )

    if health_score >= 80:
        summary += (
            "Overall, the dataset is in good condition and suitable for analysis "
            "with minor adjustments."
        )
    elif health_score >= 50:
        summary += (
            "Overall, the dataset is usable but requires careful preprocessing "
            "and validation."
        )
    else:
        summary += (
            "Overall, the dataset shows multiple quality concerns and should be "
            "used with caution."
        )

    return summary
