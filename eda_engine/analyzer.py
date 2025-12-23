import pandas as pd
from pandas.api.types import (
    is_numeric_dtype,
    is_datetime64_any_dtype,
    is_string_dtype
)


def analyze_dataset(df: pd.DataFrame) -> dict:
    """
    Analyzes a dataset and returns key metadata and statistics.
    """

    analysis = {}

    # Basic info
    analysis["num_rows"] = df.shape[0]
    analysis["num_columns"] = df.shape[1]
    analysis["column_names"] = list(df.columns)

    # Column type detection
    column_types = {}
    numeric_columns = []
    categorical_columns = []
    datetime_columns = []

    for col in df.columns:
        if is_numeric_dtype(df[col]):
            column_types[col] = "Numeric"
            numeric_columns.append(col)

        elif is_datetime64_any_dtype(df[col]):
            column_types[col] = "Datetime"
            datetime_columns.append(col)

        elif is_string_dtype(df[col]):
            column_types[col] = "Categorical"
            categorical_columns.append(col)

        else:
            column_types[col] = "Other"

    analysis["column_types"] = column_types
    analysis["numeric_columns"] = numeric_columns
    analysis["categorical_columns"] = categorical_columns
    analysis["datetime_columns"] = datetime_columns

    # Missing values
    analysis["missing_values"] = df.isnull().sum().to_dict()

    # Duplicate rows
    analysis["duplicate_rows"] = int(df.duplicated().sum())

    # Summary statistics for numeric columns
    if numeric_columns:
        analysis["numeric_summary"] = df[numeric_columns].describe().to_dict()
    else:
        analysis["numeric_summary"] = {}

    return analysis
