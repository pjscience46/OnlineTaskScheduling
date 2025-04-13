import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import griddata

# Load data from CSV file
csv_file = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtsa\Heat_Maps\Communication\Generate_Avg_Max.csv'
data = pd.read_csv(csv_file)

# Define save directory
save_directory = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtsa\Contour_Plots\Communication'
os.makedirs(save_directory, exist_ok=True)  # Ensure the directory exists


# Create grid for contour plot
mu_vals = np.linspace(data['mu'].min(), data['mu'].max(), 100)
alpha_vals = np.linspace(data['alpha'].min(), data['alpha'].max(), 100)
mu_grid, alpha_grid = np.meshgrid(mu_vals, alpha_vals)

# Function to interpolate data
def interpolate_column(column_name):
    return griddata(
        (data['alpha'], data['mu']),
        data[column_name],
        (alpha_grid, mu_grid),
        method='cubic'
    )

# Interpolate the 'max' column
max_grid = interpolate_column('max')

# Define discrete contour levels
min_val = np.nanmin(max_grid)
max_val = np.nanmax(max_grid)
levels = np.arange(np.floor(min_val), np.ceil(max_val) + 1, 1)

# Final plot: No labels, no markers, no contour borders
def plot_smooth_contour(grid, title, filename, cmap='RdYlBu_r'):
    plt.figure(figsize=(8, 6))

    # Only filled contour (no black lines)
    contourf = plt.contourf(alpha_grid, mu_grid, grid, levels=levels, cmap=cmap)
    plt.colorbar(contourf)

    # Axis labels and title
    plt.xlabel(r'$\alpha$', fontweight='bold')
    plt.ylabel(r'$\mu$', fontweight='bold')
    plt.title(title)

    # Invert y-axis if needed
    plt.gca().invert_yaxis()

    # Save and show
    plot_path = os.path.join(save_directory, filename)
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.show()

# Call the plotting function
plot_smooth_contour(max_grid, '', 'Contour_max1.png')