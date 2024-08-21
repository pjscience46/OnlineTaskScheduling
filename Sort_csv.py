import pandas as pd

# Path to your CSV file
file_path = r'C:\Users\pjsci\schedule\OnlineTaskScheduling\Results_mast\Heat_Maps\Amdahl\Generate_Avg_Max.csv'

# Read the CSV file
df = pd.read_csv(file_path)

# Ensure there are at least 3 columns
if df.shape[1] < 3:
    raise ValueError("The CSV file must have at least three columns.")

# Sort by the third column (index 2) in ascending order
sorted_df = df.sort_values(by=df.columns[2], ascending=True)

# Get the top 10 values from the third column
top_10 = sorted_df.head(100)

# Print the results
print(top_10)
