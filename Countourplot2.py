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
    # grid = interpolate_column('max')
    # grid[grid < 0] = np.nan  # Optionally mask negative artifacts
    # Find the actual minimum from the original data
    min_row = data.loc[data['max'].idxmin()]
    min_alpha = min_row['alpha']
    min_mu = min_row['mu']
    min_value = min_row['max']

    # Find the minimum value and its index
    # min_value = np.nanmin(grid)  # Use nanmin to avoid issues with NaNs
    

    # Mark the minimum value on the plot with a red circle
    plt.scatter(min_alpha, min_mu, color='red', s=150, marker='X',
            edgecolors='white', linewidth=2, clip_on=False,
            zorder=3, label=f"Min: {min_value:.2f}")
    #plt.scatter(min_alpha, min_mu, color='red', s=150, marker='X', edgecolors='white', linewidth=2, label=f"Min: {min_value:.2f}")
    
    # Add annotation next to the minimum marker
    plt.annotate(f"{min_value:.2f}", (min_alpha, min_mu),
             textcoords="offset points", xytext=(-15,10), ha='center',
             fontsize=10, color='black',
             bbox=dict(facecolor='white', alpha=0.6))
    
    plot_path = os.path.join(save_directory, 'Contour_max.png')
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')  # Save the figure
    plt.show()  # Display the plot

# Generate and save the contour plot for 'max' with the minimum value marked
plot_contour_with_min(max_grid, "")
