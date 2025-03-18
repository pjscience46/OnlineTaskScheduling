import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap, Normalize

# Load data from CSV file
csv_file = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtpa\Heat_Maps\General\Generate_Avg_Max.csv'
data = pd.read_csv(csv_file)

# Define save directory
save_directory = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtpa\Contour_Plots\General'
os.makedirs(save_directory, exist_ok=True)  # Ensure the directory exists

# Create grid for contour plot
mu_vals = np.linspace(data['mu'].min(), data['mu'].max(), 100)
gamma_vals = np.linspace(data['gamma'].min(), data['gamma'].max(), 100)
mu_grid, gamma_grid = np.meshgrid(mu_vals, gamma_vals)

# Function to interpolate data
def interpolate_column(column_name):
    return griddata(
        (data['gamma'], data['mu']),  # (x, y) order
        data[column_name],
        (gamma_grid, mu_grid),  # Interpolated to match the grid
        method='linear'  # Change to 'linear' or 'nearest' if needed
    )

# Generate grids for 'average' and 'max' values
average_grid = interpolate_column('average')
max_grid = interpolate_column('max')

# Define custom colormap (Adjusted for Yellow → Red → Darker Blue)
custom_colors = [
    (1.0, 0.9, 0.4),  # Light Yellow (Max)
    (0.95, 0.4, 0.3), # Soft Red (Middle)
    (0.2, 0.4, 0.7)   # Darker Blue (Min)
]

# Create the colormap and its reversed version
custom_cmap = LinearSegmentedColormap.from_list("YlRdBu_custom", custom_colors, N=256)
custom_cmap_reversed = custom_cmap.reversed()

# Function to plot contour with minimum value marked
def plot_contour_with_min(grid, title, cmap=custom_cmap_reversed):
    plt.figure(figsize=(8, 6))
    
    # Plot the contour
    contour = plt.contourf(gamma_grid, mu_grid, grid, levels=20, cmap=cmap)
    plt.colorbar(contour)
    plt.xlabel(r'$\gamma$',  fontweight='bold')  # Bigger and bold gamma (α)
    plt.ylabel(r'$\mu$',  fontweight='bold')      # Bigger and bold Mu (μ)

    plt.title(title)
    
    # Invert y-axis so mu increases from top to bottom
    plt.gca().invert_yaxis()

    # Find the minimum value and its index
    min_value = np.nanmin(grid)  # Use nanmin to avoid issues with NaNs
    min_index = np.unravel_index(np.nanargmin(grid), grid.shape)  # Get index of min value
    
    # Get the corresponding gamma and mu values
    min_gamma = gamma_grid[min_index]
    min_mu = mu_grid[min_index]

    # Mark the minimum value on the plot with a red circle
    plt.scatter(min_gamma, min_mu, color='red', s=150, marker='X', edgecolors='white', linewidth=2, label=f"Min: {min_value:.2f}")
    
    # Add annotation next to the minimum marker
    plt.annotate(f"Optimal value: {min_value:.2f}", (min_gamma, min_mu), textcoords="offset points", xytext=(-15,10), ha='center', fontsize=10, color='black', bbox=dict(facecolor='white', alpha=0.6))

    # Save the plot before showing
    plot_path = os.path.join(save_directory, 'Contour_max.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')  # Save the figure
    plt.show()  # Display the plot

# Generate and save the contour plot for 'max' with the minimum value marked
plot_contour_with_min(max_grid, "")
