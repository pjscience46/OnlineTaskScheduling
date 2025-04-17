import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

csv_file = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtpa\Heat_Maps\General\Generate_Avg_Max.csv'
data = pd.read_csv(csv_file)
save_directory = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mtpa\Contour_Plots\General'
os.makedirs(save_directory, exist_ok=True)
x = data['gamma']
y = data['mu']
z = data['max']

min_val = np.nanmin(z)
max_val = np.nanmax(z)
levels = np.linspace(min_val, max_val, 100)  #fine-grained levels to enhance color variation
plt.figure(figsize=(8, 6))
contour = plt.tricontourf(x, y, z, levels=levels, cmap='RdYlBu_r') #tricontourf is for scattered data ,contourf is for regular data
plt.colorbar(contour)
plt.xlabel(r'$\gamma$', fontweight='bold',fontsize=20)
plt.ylabel(r'$\mu$', fontweight='bold',fontsize=20)
plt.gca().invert_yaxis()

# === Code to mark optimal point ===
min_index = np.nanargmin(z)
min_gamma = x.iloc[min_index]
min_mu = y.iloc[min_index]
min_value = z.iloc[min_index]

# Plot the red X marker
plt.scatter(min_gamma, min_mu, color='red', s=150, marker='X',
            edgecolors='white', linewidth=2, clip_on=False,
            zorder=3, label=f"Min: {min_value:.2f}")

# Get current plot limits
x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()

# Compute margins (10% of axis range)
x_margin = 0.1 * (x_max - x_min)
y_margin = 0.1 * (y_max - y_min)

# Default offset
x_offset = 20
y_offset = -20

# Adjust offsets based on proximity to edges to avoid overlap and stay inside
if (min_gamma - x_min) < x_margin:
    x_offset = 20  # move right
elif (x_max - min_gamma) < x_margin:
    x_offset = -20  # move left

if (y_max - min_mu) < y_margin:
    y_offset = 20  # move down (remember y-axis is inverted)
elif (min_mu - y_min) < y_margin:
    y_offset = -20  # move up

# Annotate the value with adjusted offsets
plt.annotate(f"{min_value:.2f}", (min_gamma, min_mu),
             textcoords="offset points", xytext=(x_offset, y_offset), ha='center',
             fontsize=10, color='black',
             bbox=dict(facecolor='white', alpha=0.6))
# === End optimal point annotation ===



plot_path = os.path.join(save_directory, 'Contour_max_levels.png')
plt.savefig(plot_path, dpi=300, bbox_inches='tight')
plt.show()
