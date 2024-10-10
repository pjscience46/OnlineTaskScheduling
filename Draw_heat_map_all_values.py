import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Define the path to the summary CSV file
summary_file_path = r'C:\Thesis\Test_Prog\Algo2\OnlineTaskScheduling\Results_mtsa1\n\Communication\Generate_Avg_Max.csv'

# Define the directory to save the heat maps
save_directory = r'C:\Thesis\Test_Prog\Algo2\OnlineTaskScheduling\Results_mtsa1\n\Heat_Maps\Communication'

# Ensure the save directory exists
os.makedirs(save_directory, exist_ok=True)

# Load the summary data into a DataFrame

df = pd.read_csv(summary_file_path)

# Check if the required columns are present
if not all(col in df.columns for col in ['mu', 'beta', 'average', 'max']):
    raise ValueError("The summary file is missing required columns.")

# Pivot the data for average values
pivot_avg = df.pivot(index='mu', columns='beta', values='average')

# Plot the heat map for average values without annotations
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_avg, annot=True, cmap='viridis', cbar=True)  # annot=False to hide numbers
plt.title('Heat Map of Average Values')
plt.xlabel('Alpha')
plt.ylabel('Mu')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

# Save the average heatmap
average_heatmap_path = os.path.join(save_directory, 'heatmap_average.png')
plt.savefig(average_heatmap_path)
plt.show()

# Pivot the data for max values
pivot_max = df.pivot(index='mu', columns='beta', values='max')

# Plot the heat map for max values without annotations
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_max, annot=True, cmap='viridis', cbar=True)  # annot=False to hide numbers
plt.title('Heat Map of Max Values')
plt.xlabel('Alpha')
plt.ylabel('Mu')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

# Save the max heatmap
max_heatmap_path = os.path.join(save_directory, 'heatmap_max.png')
plt.savefig(max_heatmap_path)
plt.show()
