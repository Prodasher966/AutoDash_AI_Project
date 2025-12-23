from eda_engine.loader import load_csv
from eda_engine.analyzer import analyze_dataset
from eda_engine.visualizer import generate_visualizations

if __name__ == "__main__":
    file_path = input("Enter CSV file path: ")

    try:
        df = load_csv(file_path)
        print("\n✅ CSV Loaded Successfully!\n")
        print(df.head())
        
        analysis = analyze_dataset(df)

        print("📊 Dataset Overview")
        print(f"Rows: {analysis['num_rows']}")
        print(f"Columns: {analysis['num_columns']}")
        print(f"Duplicate Rows: {analysis['duplicate_rows']}\n")

        print("🧠 Column Types")
        for col, col_type in analysis["column_types"].items():
            print(f"{col}: {col_type}")

        print("\n❗ Missing Values")
        for col, missing in analysis["missing_values"].items():
            print(f"{col}: {missing}")

        plots = generate_visualizations(
            df,
            analysis["numeric_columns"],
            analysis["categorical_columns"]
        )

        print("\n📊 Analysis Complete")
        print(f"Generated {len(plots)} plots")
        print("Saved plots:")
        for p in plots:
            print(f"- {p}")
        
    except ValueError as error:
        print(f"\n❌ Error: {error}")

