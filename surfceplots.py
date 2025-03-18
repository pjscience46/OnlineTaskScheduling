import numpy as np
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load data
data = pd.read_csv(r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtpa\Heat_Maps\Roofline\Generate_Avg_Max.csv')

# Sort and pivot data to create a structured grid
data = data.sort_values(by=['gamma', 'mu'])
pivot_table = data.pivot(index='mu', columns='gamma', values='max')[::-1]  # Reverse Mu for top-down order

# Extract values for plotting
mu_vals = pivot_table.index.values  # Exact mu values from data
gamma_vals = np.sort(pivot_table.columns.values)  # Sorted gamma values
max_vals = pivot_table.values  # Values for max

# Create meshgrid
gamma_grid, mu_grid = np.meshgrid(gamma_vals, mu_vals)

# Create the surface plot
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot surface with no normalization (cmap 'inferno' has yellow in the higher range)
surf = ax.plot_surface(gamma_grid, mu_grid, max_vals, cmap='inferno', edgecolor='k')

# Plot peak point (highest value)
max_index = np.unravel_index(np.argmax(max_vals, axis=None), max_vals.shape)
max_gamma, max_mu, max_z = gamma_grid[max_index], mu_grid[max_index], max_vals[max_index]
ax.scatter(max_gamma, max_mu, max_z, color='red', s=100, label=f'Max: {max_z}')

# Set exact axis labels and limits
ax.set_xlabel(r'$\gamma$', fontsize=14)
ax.set_ylabel(r'$\mu$', fontsize=14)
ax.set_zlabel('Max')


# Use exact mu values without approximation
ax.set_xlim(gamma_vals[0], gamma_vals[-1])  # Set limits based on data
ax.set_ylim(mu_vals[0], mu_vals[-1])  # Use exact mu values

# Manually set the ticks for the mu axis to be exactly the mu values
ax.set_yticks(mu_vals)

# Adjust view angle
ax.view_init(elev=35, azim=140)

# Add color bar without normalization
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
cbar.set_label('Max')

# Add legend
ax.legend()

plt.show()
