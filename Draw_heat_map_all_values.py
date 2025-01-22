import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Define the path to the summary CSV file
summary_file_path = r'C:\Thesis\Test_Prog\Algo3\OnlineTaskScheduling\Results_mast\Heat_Maps\Amdahl\Generate_Avg_Max.csv'

# Define the directory to save the heat maps
save_directory = r'C:\Thesis\Test_Prog\Algo3\OnlineTaskScheduling\Results_mast\Heat_Maps\Amdahl'

# Ensure the save directory exists
os.makedirs(save_directory, exist_ok=True)

# Load the summary data into a DataFrame

df = pd.read_csv(summary_file_path)

# Check if the required columns are present
if not all(col in df.columns for col in ['mu', 'beta', 'average', 'max']):
    raise ValueError("The summary file is missing required columns.")
df_filtered = df
# Pivot the data for average values
pivot_avg = df_filtered.pivot(index='mu', columns='beta', values='average')
min_value_avg = df_filtered['average'].min()
max_value_avg = df_filtered['average'].max()

min_value_max = df_filtered['max'].min()
max_value_max = df_filtered['max'].max()
# Plot the heat map for average values without annotations
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_avg, annot=True, fmt="g",cmap='viridis', cbar=True,vmin = min_value_avg )  # annot=False to hide numbers
plt.title('Heat Map of Average Values')
plt.xlabel('Beta')
plt.ylabel('Mu')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

# Save the average heatmap
average_heatmap_path = os.path.join(save_directory, 'heatmap_average.png')
plt.savefig(average_heatmap_path)
plt.show()

# Pivot the data for max values
pivot_max = df_filtered.pivot(index='mu', columns='beta', values='max')

# Plot the heat map for max values without annotations
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_max, annot=True, fmt="g" ,cmap='viridis', cbar=True,vmin = min_value_max)  # annot=False to hide numbers
plt.title('Heat Map of Max Values')
plt.xlabel('Beta')
plt.ylabel('Mu')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

# Save the max heatmap
max_heatmap_path = os.path.join(save_directory, 'heatmap_max.png')
plt.savefig(max_heatmap_path)
plt.show()
