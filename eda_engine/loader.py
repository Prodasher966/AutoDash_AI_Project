import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Loads a CSV file and returns a pandas DataFrame.

    Parameters:
        file_path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Loaded dataset

    Raises:
        ValueError: If file cannot be loaded
    """
    try:
        df = pd.read_csv(file_path)
        
        if df.empty:
            raise ValueError("The CSV file is empty.")
        
        return df

    except FileNotFoundError:
        raise ValueError("File not found. Please check the path.")

    except pd.errors.ParserError:
        raise ValueError("Error parsing the CSV file.")

    except Exception as e:
        raise ValueError(f"Unexpected error: {str(e)}")
