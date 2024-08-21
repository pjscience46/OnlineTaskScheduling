
import pandas as pd

import re

import os




# Define the folder containing CSV files

folder_path = r'C:\Users\m779p635\Desktop\Online_schedule\OnlineTaskScheduling\Results_mtsa\n\Amdahl'




# Initialize an empty DataFrame to collect results

results_df = pd.DataFrame(columns=['mu', 'beta', 'average', 'max'])




# Function to process a single file

def process_file(file_path):

    global results_df  # Ensure the function uses the global results_df

    

    try:

        # Load the CSV file into a DataFrame with a specified encoding

        df = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip')

    except pd.errors.EmptyDataError:

        print(f"Warning: The file {file_path} is empty or could not be read.")

        return

    except pd.errors.ParserError as e:

        print(f"Error: Could not parse the file {file_path}. {e}")

        return

    except UnicodeDecodeError as e:

        print(f"Error: Unicode decode error in file {file_path}. {e}")

        return

    

    

    

    # Filter rows to keep only those with exactly 6 columns

    if df.shape[1] != 6:

        print(f"Warning: The file {file_path} does not have exactly 6 columns. Skipping file.")

        return

    

    # Get the last column name

    last_column_name = df.columns[-1]

    

    # Extract values from the last column and store them in a list

    last_column_values = df[last_column_name].tolist()

    

    # Convert the list of values to numeric, forcing errors to NaN (to handle non-numeric values)

    numeric_values = pd.to_numeric(last_column_values, errors='coerce')

    

    # Calculate the average of the numeric values, ignoring NaN values

    average_value = numeric_values.mean()

    

    # Find the maximum value in the list, excluding the average value itself

    filtered_values = numeric_values[numeric_values != average_value]

    

    # Handle the case where filtered_values might be empty

    if filtered_values.size == 0:

        max_value = pd.NA  # or np.nan, depending on your preference

    else:

        max_value = filtered_values.max()

    

    # Extract the filename from the file path

    filename = os.path.basename(file_path)

    

    # Extract mu and beta values from the filename

    # Assuming the filename is 'mu_0.1_beta_1.csv'

    match = re.match(r'mu_([\d.]+)_beta_([\d.]+)', filename)

    if not match:

        print(f"Error: Filename {filename} does not match the expected format.")

        return

    

    mu_value, beta_value = match.groups()

    

    # Clean the extracted values to ensure proper float conversion

    mu_value = mu_value.rstrip('.')  # Remove any trailing periods

    beta_value = beta_value.rstrip('.')  # Remove any trailing periods

    

    try:

        mu_value = float(mu_value)

        beta_value = float(beta_value)

    except ValueError as e:

        print(f"Error: Could not convert mu or beta value to float. {e}")

        return

    

    # Append the result to the global results DataFrame

    results_df.loc[len(results_df)] = [mu_value, beta_value, average_value, max_value]




    print(f"Processed {file_path}")




# Loop through all CSV files in the folder

for file_name in os.listdir(folder_path):

    if file_name.endswith('.csv'):

        file_path = os.path.join(folder_path, file_name)

        process_file(file_path)




# Define the output file path
file_path = r'C:\Users\m779p635\Desktop\Online_schedule\OnlineTaskScheduling'
output_file_path = os.path.join(file_path, 'Generate_Avg_Max.csv')
# Write the DataFrame to a new CSV file

results_df.to_csv(output_file_path, index=False)




print(f"All data has been collected and saved to {output_file_path}")
