import os
import matplotlib.pyplot as plt
import pandas as pd


def safe_filename(name: str) -> str:
    return (
        name.replace("/", "_")
            .replace("\\", "_")
            .replace(" ", "_")
            .replace(":", "")
            .replace("*", "")
            .replace("?", "")
            .replace('"', "")
            .replace("<", "")
            .replace(">", "")
            .replace("|", "")
    )


# -----------------------------
# Global Visualization Settings
# -----------------------------
FIG_SIZE = (8, 4)

TITLE_STYLE = dict(
    fontsize=12,
    fontweight="bold",
    bbox=dict(
        boxstyle="round,pad=0.4",
        edgecolor="black",
        facecolor="#f2f2f2"
    )
)


def apply_layout(fig):
    """
    Applies a robust layout that works even
    when tight_layout fails due to long titles
    or rotated labels.
    """
    try:
        fig.tight_layout()
    except Exception:
        pass

    fig.subplots_adjust(top=0.85, bottom=0.25)


def generate_visualizations(df, numeric_columns, categorical_columns):
    output_dir = "outputs/plots"
    os.makedirs(output_dir, exist_ok=True)

    plot_paths = []

    # -----------------------------
    # Numeric Column Visualizations
    # -----------------------------
    for col in numeric_columns:
        if df[col].nunique() <= 1:
            continue

        safe_col = safe_filename(col)

        # Histogram
        fig, ax = plt.subplots(figsize=FIG_SIZE)
        ax.hist(df[col].dropna(), bins=30)
        ax.set_title(f"Distribution of {col}", **TITLE_STYLE)
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")

        apply_layout(fig)

        file_path = os.path.join(output_dir, f"{safe_col}_distribution.png")
        fig.savefig(file_path, dpi=100)
        plt.close(fig)
        plot_paths.append(file_path)

        # Boxplot
        fig, ax = plt.subplots(figsize=FIG_SIZE)
        ax.boxplot(df[col].dropna(), vert=False)
        ax.set_title(f"Outlier Analysis of {col}", **TITLE_STYLE)
        ax.set_xlabel(col)

        apply_layout(fig)

        file_path = os.path.join(output_dir, f"{safe_col}_boxplot.png")
        fig.savefig(file_path, dpi=100)
        plt.close(fig)
        plot_paths.append(file_path)

    # --------------------------------
    # Categorical Column Visualizations
    # --------------------------------
    for col in categorical_columns:
        unique_vals = df[col].nunique()
        if unique_vals <= 1:
            continue

        value_counts = df[col].value_counts().dropna()

        if unique_vals > 10:
            value_counts = value_counts.head(10)
            title_suffix = " (Top 10)"
        else:
            title_suffix = ""

        safe_col = safe_filename(col)

        fig, ax = plt.subplots(figsize=FIG_SIZE)
        value_counts.plot(kind="bar", ax=ax)
        ax.set_title(
            f"Category Distribution of {col}{title_suffix}",
            **TITLE_STYLE
        )
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=45)

        apply_layout(fig)

        file_path = os.path.join(output_dir, f"{safe_col}_categories.png")
        fig.savefig(file_path, dpi=100)
        plt.close(fig)
        plot_paths.append(file_path)

    return plot_paths
