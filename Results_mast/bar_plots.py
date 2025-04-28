import pandas as pd
import matplotlib.pyplot as plt

# File paths for each algorithm's results
file_paths = {
    'MAST': r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mast\Heat_Maps\Amdahl\Generate_Avg_Max.csv',
    'MTSA': r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtsa\Heat_Maps\Amdahl\Generate_Avg_Max.csv',
    'MTPA': r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtpa\Heat_Maps\Amdahl\Generate_Avg_Max.csv'
}

# Mapping: algorithm name --> parameter symbol and CSV column name
param_info = {
    'MAST': {'symbol': r'\beta', 'column': 'beta'},
    'MTSA': {'symbol': r'\alpha', 'column': 'alpha'},
    'MTPA': {'symbol': r'\gamma', 'column': 'gamma'}
}

# Storage for plotting
algorithms = []
average_values = []
max_values = []
mu_values = []
param_values = []
param_symbols = []

# Process each file
for algo_name, file_path in file_paths.items():
    df = pd.read_csv(file_path)
    min_row = df.loc[df['max'].idxmin()]  # <<<<===== CHANGE HERE: minimum value of max!

    # Which column to pick for the parameter?
    param_column = param_info[algo_name]['column']
    param_symbol = param_info[algo_name]['symbol']

    algorithms.append(algo_name)
    average_values.append(min_row['average'])
    max_values.append(min_row['max'])
    mu_values.append(min_row['mu'])
    param_values.append(min_row[param_column])  # Read correct parameter
    param_symbols.append(param_symbol)

# Create plot
fig, ax = plt.subplots(figsize=(10, 7))

x = range(len(algorithms))
bar_width = 0.35

# Plot bars
bars1 = ax.bar([i - bar_width/2 for i in x], average_values, width=bar_width, label='Average Makespan', color="#4C72B0")
bars2 = ax.bar([i + bar_width/2 for i in x], max_values, width=bar_width, label='Max Makespan', color="#55A868")

# Annotate values
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

# Correct x-tick labels: show μ and correct parameter symbol (α/β/γ)
xtick_labels = [
    f'{algo}\nμ={mu_values[i]}, {param_symbols[i]}={param_values[i]}' for i, algo in enumerate(algorithms)
]

ax.set_xticks(x)
ax.set_xticklabels(xtick_labels)

ax.set_ylabel('Makespan')
ax.set_title('Comparison of Average and Max Makespan at Optimal Settings (for Amdahl Model)')
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
