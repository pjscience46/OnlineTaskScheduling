import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap, Normalize

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
        (data['alpha'], data['mu']),  # (x, y) order
        data[column_name],
        (alpha_grid, mu_grid),  # Interpolated to match the grid
        method='cubic'  # Change to 'linear' or 'nearest' if needed
    )

# Generate grids for 'average' and 'max' values
average_grid = interpolate_column('average')
max_grid = interpolate_column('max')



# Function to plot contour with minimum value marked
def plot_contour_with_min(grid, title, cmap='RdYlBu_r'):
    plt.figure(figsize=(8, 6))
    
    # Plot the contour
    contour = plt.contourf(alpha_grid, mu_grid, grid, levels=20, cmap=cmap)
    plt.colorbar(contour)
    plt.xlabel(r'$\alpha$',  fontweight='bold')  # Bigger and bold alpha (α)
    plt.ylabel(r'$\mu$',  fontweight='bold')      # Bigger and bold Mu (μ)

    plt.title(title)
    
    # Invert y-axis so mu increases from top to bottom
    plt.gca().invert_yaxis()

    # Find the minimum value and its index
    min_value = np.nanmin(grid)  # Use nanmin to avoid issues with NaNs
    min_index = np.unravel_index(np.nanargmin(grid), grid.shape)  # Get index of min value
    
    # Get the corresponding alpha and mu values
    min_alpha = alpha_grid[min_index]
    min_mu = mu_grid[min_index]

    # Mark the minimum value on the plot with a red circle
    # plt.scatter(min_alpha, min_mu, color='red', s=150, marker='X',
    #         edgecolors='white', linewidth=2, clip_on=False,
    #         zorder=3, label=f"Min: {min_value:.2f}")

    
    plot_path = os.path.join(save_directory, 'Contour_max.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')  # Save the figure
    plt.show()  # Display the plot

# Generate and save the contour plot for 'max' with the minimum value marked
plot_contour_with_min(max_grid, "")