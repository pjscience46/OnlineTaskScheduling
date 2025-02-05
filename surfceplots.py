import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import os
# Load data from CSV file
data = pd.read_csv('C:\Thesis\Fresh pull\OnlineTaskScheduling\Results_mtpa\Heat_Maps\Roofline\Generate_Avg_Max.csv')
save_directory = r'C:\Thesis\Fresh pull\OnlineTaskScheduling\Results_mtpa\Surface_Plots\Roofline'

# Ensure the save directory exists
os.makedirs(save_directory, exist_ok=True)

# Extract columns
mu = data['mu'].values
gamma = data['gamma'].values
average = data['average'].values
max_val = data['max'].values

# Create a grid for plotting
mu_unique = np.unique(mu)
gamma_unique = np.unique(gamma)
mu_grid, gamma_grid = np.meshgrid(mu_unique, gamma_unique)

# Reshape data to fit the grid
average_grid = average.reshape(len(gamma_unique), len(mu_unique))
max_grid = max_val.reshape(len(gamma_unique), len(mu_unique))

# Plotting for Average
fig1 = plt.figure(figsize=(7, 6))
ax1 = fig1.add_subplot(111, projection='3d')
surf1 = ax1.plot_surface(mu_grid, gamma_grid, average_grid, cmap='viridis', edgecolor='k',vmin=average.min(), vmax=average.max())
ax1.set_title('Surface Plot for Average')
ax1.set_xlabel('Mu')
ax1.set_ylabel('gamma')
ax1.set_zlabel('Average')
fig1.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10)
average_surfaceplot_path = os.path.join(save_directory, 'Surface_Plot_average.png')
plt.savefig(average_surfaceplot_path)
plt.tight_layout()
plt.show()

# Plotting for Max
fig2 = plt.figure(figsize=(7, 6))
ax2 = fig2.add_subplot(111, projection='3d')
surf2 = ax2.plot_surface(mu_grid, gamma_grid, max_grid, cmap='plasma', edgecolor='k',vmin=max_val.min(), vmax=max_val.max())
ax2.set_title('Surface Plot for Max')
ax2.set_xlabel('Mu')
ax2.set_ylabel('gamma')
ax2.set_zlabel('Max')
fig2.colorbar(surf2, ax=ax2, shrink=0.5, aspect=10)
max_surfaceplot_path = os.path.join(save_directory, 'Surface_Plot_max.png')
plt.savefig(max_surfaceplot_path)
plt.tight_layout()
plt.show()
