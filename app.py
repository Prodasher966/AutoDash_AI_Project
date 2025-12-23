import streamlit as st
import pandas as pd
import os

from eda_engine.analyzer import analyze_dataset
from eda_engine.visualizer import generate_visualizations
from eda_engine.insights import (
    generate_insights,
    calculate_health_score,
    generate_executive_summary
)

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="AutoDash AI",
    layout="wide"
)

# ----------------------------------
# Sidebar
# ----------------------------------
st.sidebar.title("⚙️ AutoDash Controls")
st.sidebar.markdown("Upload a CSV file to begin analysis")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "AutoDash AI automatically analyzes your dataset and "
    "generates insights & visualizations — no coding required."
)

# ----------------------------------
# Main Title
# ----------------------------------
st.title("📊 AutoDash AI")
st.subheader("AI-powered automatic data analysis dashboard")

# ----------------------------------
# Severity Badge Helper
# ----------------------------------
def severity_badge(level: str) -> str:
    badges = {
        "info": "🟢 INFO",
        "warning": "🟡 WARNING",
        "critical": "🔴 CRITICAL"
    }
    return badges.get(level, "ℹ️")

SEVERITY_ORDER = {
    "critical": 0,
    "warning": 1,
    "info": 2
}
# ----------------------------------
# Main Logic
# ----------------------------------
if uploaded_file is not None:
    try:
        # Load data
        df = pd.read_csv(uploaded_file)

        analysis = analyze_dataset(df)

        # ------------------------------
        # Dataset Overview
        # ------------------------------
        st.markdown("## 📌 Dataset Overview")
        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", analysis["num_rows"])
        col2.metric("Columns", analysis["num_columns"])
        col3.metric("Duplicate Rows", analysis["duplicate_rows"])

        # ------------------------------
        # Column Types
        # ------------------------------
        st.markdown("## 🧠 Column Types")
        st.json(analysis["column_types"])

        # ------------------------------
        # Missing Values
        # ------------------------------
        st.markdown("## ❗ Missing Values")
        missing_df = pd.DataFrame(
            analysis["missing_values"].items(),
            columns=["Column", "Missing Values"]
        )
        st.dataframe(missing_df, use_container_width=True)

        # ------------------------------
        # Dataset Preview
        # ------------------------------
        with st.expander("📄 Dataset Preview (First 50 Rows)"):
            st.dataframe(df.head(50), use_container_width=True)

        # ------------------------------
        # Generate Insights (MUST COME FIRST)
        # ------------------------------
        insights = generate_insights(df)

        # ------------------------------
        # Dataset Health Score
        # ------------------------------
        health_score = calculate_health_score(insights)

        st.markdown("## 🩺 Dataset Health Score")

        st.metric(
            label="Overall Health",
            value=f"{health_score} / 100"
        )

        # Visual cue
        if health_score >= 80:
            st.success("Dataset is in good condition.")
        elif health_score >= 50:
            st.warning("Dataset requires preprocessing attention.")
        else:
            st.error("Dataset has significant quality issues.")

        # ------------------------------
        # Executive Summary
        # ------------------------------
        st.markdown("## 🧾 Executive Summary")

        summary = generate_executive_summary(insights, health_score)
        st.write(summary)
        
        # ------------------------------
        # AI-Generated Insights
        # ------------------------------
        st.markdown("## 🤖 Automated Insights")

        insights = generate_insights(df)
        insights = sorted(
        insights,
        key=lambda x: SEVERITY_ORDER.get(x["severity"], 99)
    )

        if not insights:
            st.info("No significant insights detected for this dataset.")
        else:
            for insight in insights:
                with st.container():
                    st.markdown(
                        f"""
                        **{severity_badge(insight['severity'])}  
                        {insight['title']}**
                        """
                    )

                    # Human-readable interpretation
                    st.write(insight["interpretation"])

                    # Technical details
                    with st.expander("🔍 Technical details"):
                        st.markdown(f"**Method:** {insight['technical']['method']}")
                        st.markdown(f"**Details:** {insight['technical']['details']}")
                        st.json(insight["technical"]["stats"])

                    st.divider()

        # ------------------------------
        # Automatic Visualizations
        # ------------------------------
        st.markdown("## 📊 Automatic Visualizations")

        plots = generate_visualizations(
            df,
            analysis["numeric_columns"],
            analysis["categorical_columns"]
        )

        if plots:
            cols = st.columns(2)
            for idx, plot_path in enumerate(plots):
                if os.path.exists(plot_path):
                    cols[idx % 2].image(plot_path, use_container_width=True)

            with st.expander("📈 Visualization Details"):
                st.write(f"Total plots generated: **{len(plots)}**")
        else:
            st.info("No suitable columns found for visualization.")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("⬅️ Upload a CSV file from the sidebar to begin.")
