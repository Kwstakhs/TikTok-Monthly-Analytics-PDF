import pandas as pd


# Function to load and preprocess CSV files
def load_and_preprocess_csv(file_path):
    df = pd.read_csv(file_path)
    return df


# Ensure all necessary columns are numeric
def ensure_numeric(data, columns):
    for column in columns:
        data[column] = pd.to_numeric(data[column], errors='coerce')
    return data


# Generate summary reports
def generate_summary_report(data, sum_metrics, avg_metrics):
    try:
        summary_sum = data.groupby('Month', observed=True)[sum_metrics].sum()
        return summary_sum, None
    except Exception as e:
        print(f"Error generating summary report: {e}")
        return None, None
