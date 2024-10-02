
import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt




# Define the path to the summary CSV file

#summary_file_path = r'C:\Users\pjsci\schedule\Algorithm2\OnlineTaskScheduling\Results_mtsa1\n\Heat_Maps\Amdahl\Generate_Avg_Max.csv'

summary_file_path = r'C:\Thesis\updated_algo\Algo2\OnlineTaskScheduling\Results_mtsa1\n\Amdahl\Generate_Avg_Max.csv'


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

plt.savefig('heatmap_average.png')

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

plt.savefig('heatmap_max.png')

plt.show()




