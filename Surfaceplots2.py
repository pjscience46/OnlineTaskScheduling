import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Load data
data = pd.read_csv(r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtsa\Heat_Maps\Communication\Generate_Avg_Max.csv')

save_directory = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtsa\Surface_Plots\Communication'
os.makedirs(save_directory, exist_ok=True)  # Ensure the directory exists

# Sort and pivot data to create a structured grid
data = data.sort_values(by=['alpha', 'mu'])
pivot_table = data.pivot(index='mu', columns='alpha', values='max')[::-1]  # Reverse Mu for top-down order

# Extract values for plotting
mu_vals = pivot_table.index.values  # Exact mu values from data
alpha_vals = np.sort(pivot_table.columns.values)  # Sorted alpha values
max_vals = pivot_table.values  # Values for max

# Create meshgrid
alpha_grid, mu_grid = np.meshgrid(alpha_vals, mu_vals)

# Create the surface plot with a **smaller figure size**
fig = plt.figure(figsize=(6, 5), dpi=150)  # Decrease image size
ax = fig.add_subplot(111, projection='3d')

# Plot surface with no normalization (cmap 'inferno' has yellow in the higher range)
surf = ax.plot_surface(alpha_grid, mu_grid, max_vals, cmap='inferno', edgecolor='k')

# Find minimum value (optimal value)
min_index = np.unravel_index(np.argmin(max_vals, axis=None), max_vals.shape)
min_alpha, min_mu, min_z = alpha_grid[min_index], mu_grid[min_index], max_vals[min_index]

# # **Check if the minimum value is within plot bounds before marking**
# if (alpha_vals[0] <= min_alpha <= alpha_vals[-1]) and (mu_vals[0] <= min_mu <= mu_vals[-1]):
#     ax.scatter(min_alpha, min_mu, min_z, color='red', s=80, marker='X', edgecolors='white', linewidth=1.5, label="Optimal value")
#     ax.text(min_alpha, min_mu, min_z, f"Optimal: {min_z:.2f}", color='black', fontsize=8, ha='left', bbox=dict(facecolor='white', alpha=0.6))

# Set axis labels and limits
ax.set_xlabel(r'$\alpha$', fontsize=8, labelpad=8)
ax.set_ylabel(r'$\mu$', fontsize=8, labelpad=8)

ax.zaxis.set_rotate_label(False)  # Prevent automatic rotation


ax.view_init(elev=30, azim=45)  # Adjust azimuth angle to bring Z-axis to the left

ax.zaxis.set_label_coords(-0.1, 0.5)

# Use exact mu values without approximation
ax.set_xlim(alpha_vals[0], alpha_vals[-1])  # Set limits based on data
ax.set_ylim(mu_vals[0], mu_vals[-1])  # Use exact mu values

# Manually set the ticks for the mu axis to be exactly the mu values
ax.set_yticks(mu_vals)

# Adjust view angle
ax.view_init(elev=30, azim=135)
ax.tick_params(axis='x', labelsize=5,pad=0.05)  # X-axis numbers smaller
ax.tick_params(axis='y', labelsize=5,pad=0.05)  # Y-axis numbers smaller

# Add **smaller color bar** to save space
ccbar = fig.colorbar(surf, ax=ax, shrink=0.6, aspect=20, pad=0.15)
 # Smaller color bar
# cbar.set_label('Max', fontsize=10)

# Add legend only if the optimal value was marked
# if (alpha_vals[0] <= min_alpha <= alpha_vals[-1]) and (mu_vals[0] <= min_mu <= mu_vals[-1]):
#     ax.legend(fontsize=9)

# **Make the layout tighter manually**
fig.tight_layout()  # Auto-adjust elements for tight layout
fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Manually trim excess space
plot_path = os.path.join(save_directory, 'Surfaceplot_max.png')
plt.savefig(plot_path, dpi=300, bbox_inches='tight') 

# Show the plot
plt.show()