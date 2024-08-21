import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Define the path to the summary CSV file
summary_file_path = r'C:\Users\pjsci\schedule\Algorithm2\OnlineTaskScheduling\Results_mtsa\n\Heat_Maps\Amdahl\Generate_Avg_Max.csv'

# Load the summary data into a DataFrame
df = pd.read_csv(summary_file_path)

# Check if the required columns are present
if not all(col in df.columns for col in ['mu', 'beta', 'average', 'max']):
    raise ValueError("The summary file is missing required columns.")

# Pivot the data for average values
pivot_avg = df.pivot(index='mu', columns='beta', values='average')

# Plot the heat map for average values with improved annotation readability
plt.figure(figsize=(20, 8))
sns.heatmap(pivot_avg, annot=True, fmt='.2f', cmap='viridis', cbar=True, annot_kws={"size": 8})
plt.title('Heat Map of Average Values')
plt.xlabel('Beta')
plt.ylabel('Mu')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('heatmap_average.png')
plt.show()

# Pivot the data for max values
pivot_max = df.pivot(index='mu', columns='beta', values='max')

# Plot the heat map for max values with improved annotation readability
plt.figure(figsize=(12, 12))
sns.heatmap(pivot_max, annot=True, fmt='.2f', cmap='viridis', cbar=True, annot_kws={"size": 8})
plt.title('Heat Map of Max Values')
plt.xlabel('Beta')
plt.ylabel('Mu')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('heatmap_max.png')
plt.show()

# Set x-axis ticks to have a difference of 0.05
beta_ticks = np.arange(1, 5.05, 0.05)
plt.figure(figsize=(20, 8))
sns.heatmap(pivot_avg, annot=True, fmt='.2f', cmap='viridis', cbar=True, annot_kws={"size": 8})
plt.title('Heat Map of Average Values')
plt.xlabel('Beta')
plt.ylabel('Mu')
plt.xticks(ticks=np.arange(len(pivot_avg.columns)), labels=np.round(pivot_avg.columns, 2), rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('heatmap_average_custom_ticks.png')
plt.show()
