import pandas as pd
import re
import os

# Define the folder containing CSV files
folder_path = r'C:\Users\pjsci\schedule\OnlineTaskScheduling\Results_mast\n\General'

# Initialize an empty DataFrame to collect results
results_df = pd.DataFrame(columns=['mu', 'beta', 'average', 'max'])

# Function to process a single file
def process_file(file_path):
    global results_df  # Ensure the function uses the global results_df

    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip')
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as e:
        print(f"Warning: Skipping file {file_path} due to error: {e}")
        return

    # Check if the DataFrame is not empty and has at least one row
    if df.empty:
        print(f"Warning: The file {file_path} is empty. Skipping file.")
        return

    # Get the last column name
    last_column_name = df.columns[-1]

    # Check if any value in the last column is less than one
    if (df[last_column_name] < 1).any():
        print(f"Skipping file {file_path} because it contains values less than zero.")
        return

    # Initialize a list to collect valid values from the last column
    valid_values = []

    # Iterate over each row and collect valid values
    for index, row in df.iterrows():
        try:
            # Convert the value from the last column to numeric
            value = pd.to_numeric(row[last_column_name], errors='coerce')
            if pd.notna(value):
                valid_values.append(value)
        except Exception as e:
            print(f"Warning: Skipping row {index} in file {file_path} due to error: {e}")

    # Proceed only if there are valid values
    if valid_values:
        # Calculate the average and maximum of the valid values
        average_value = pd.Series(valid_values).mean()
        max_value = pd.Series(valid_values).max()

        # Extract the filename from the file path
        filename = os.path.basename(file_path)

        # Extract mu and beta values from the filename
        match = re.match(r'mu_([\d.]+)_beta_([\d.]+)\.csv', filename)
        if not match:
            print(f"Error: Filename {filename} does not match the expected format.")
            return

        mu_value, beta_value = match.groups()

        try:
            mu_value = float(mu_value)
            beta_value = float(beta_value)
        except ValueError as e:
            print(f"Error: Could not convert mu or beta value to float. {e}")
            return

        # Append the result to the global results DataFrame
        results_df.loc[len(results_df)] = [mu_value, beta_value, average_value, max_value]

        print(f"Processed {file_path}")
    else:
        print(f"Warning: No valid data found in file {file_path}. Skipping file.")

# Loop through all CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        process_file(file_path)

# Define the output file path
output_file_path = r'C:\Users\pjsci\schedule\OnlineTaskScheduling\Eliminate_Zeros\General\Eliminate_zeros_output.csv'

# Write the DataFrame to a new CSV file
results_df.to_csv(output_file_path, index=False)

print(f"All data has been collected and saved to {output_file_path}")
