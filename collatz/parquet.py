import pandas as pd

# Replace this with your correct path to the Parquet file
file_path = "data/collatz_metrics_part_000001.parquet"

# Load the Parquet file into a pandas DataFrame
df = pd.read_parquet(file_path)

# Display basic info and the first few rows
print(df.info())
print(df.head())
