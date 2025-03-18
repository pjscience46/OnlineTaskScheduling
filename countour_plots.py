import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm

# Load data from Excel file
data = pd.read_csv(r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtsa\Heat_Maps\Amdahl\Generate_Avg_Max.csv')  # Replace 'data.xlsx' with your actual file name

save_directory = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtsa\Contour_Plots\Amdahl'

# Ensure the save directory exists
os.makedirs(save_directory, exist_ok=True)

# Create grid for contour plot
mu_vals = np.linspace(data['mu'].min(), data['mu'].max(), 100)
alpha_vals = np.linspace(data['alpha'].min(), data['alpha'].max(), 100)
mu_grid, alpha_grid = np.meshgrid(mu_vals, alpha_vals)

# Interpolate the data
def interpolate_column(column_name):
    return griddata(
        (data['alpha'], data['mu']),  # (x, y) order
        data[column_name],
        (alpha_grid, mu_grid),  # Interpolated to match the grid
        method='cubic'  # Change to 'linear' or 'nearest' if needed
    )

average_grid = interpolate_column('average')
max_grid = interpolate_column('max')
# colors = [(1, 1, 0), (1, 0, 0), (0, 0, 0.5)]  # Yellow → Red → Green
# custom_cmap = LinearSegmentedColormap.from_list("YellowRedNavy", colors, N=256)

custom_colors = [
    (1.0, 0.9, 0.4),  # Light Yellow (Max, from extracted image)
    (0.95, 0.4, 0.3),  # Soft Red (Middle, from extracted image)
    (0.2, 0.4, 0.7)

]
# Reverse the custom colormap


# Create a smooth custom colormap
custom_cmap = LinearSegmentedColormap.from_list("YlRdBu_custom", custom_colors, N=256)
custom_cmap_reversed = custom_cmap.reversed()


# Function to plot contour
# Function to plot contour with inverted y-axis
def plot_contour(grid, title, cmap=custom_cmap_reversed):
    plt.figure(figsize=(8, 6))
    contour = plt.contourf(alpha_grid, mu_grid, grid, levels=20, cmap=cmap)
    plt.colorbar(contour)
    # plt.xlabel('alpha')
    # plt.ylabel('mu')
    plt.xlabel(r'$\alpha$')  # Alpha (α)
    plt.ylabel(r'$\mu$')      # Mu (μ)

    plt.title(title)
    
    # Invert y-axis so mu increases from top to bottom
    plt.gca().invert_yaxis()
    

plot_contour(max_grid, '')

max_plot = os.path.join(save_directory, 'Contour_max.png')
fig = plt.gcf()
# Save BEFORE showing the plot
fig.savefig(max_plot, dpi=300, bbox_inches='tight')  # Optional: Increase DPI for quality
plt.show()  # Now display the plot

