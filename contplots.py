import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

csv_file = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mast\Heat_Maps\General\Generate_Avg_Max.csv'
data = pd.read_csv(csv_file)
save_directory = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mast\Contour_Plots\General'
os.makedirs(save_directory, exist_ok=True)
x = data['beta']
y = data['mu']
z = data['max']

min_val = np.nanmin(z)
max_val = np.nanmax(z)
levels = np.linspace(min_val, max_val, 100)  #fine-grained levels to enhance color variation
plt.figure(figsize=(8, 6))
contour = plt.tricontourf(x, y, z, levels=levels, cmap='RdYlBu_r') #tricontourf is for scattered data ,contourf is for regular data
plt.colorbar(contour)
plt.xlabel(r'$\beta$', fontweight='bold')
plt.ylabel(r'$\mu$', fontweight='bold')
plt.gca().invert_yaxis()
plot_path = os.path.join(save_directory, 'Contour_max_levels.png')
plt.savefig(plot_path, dpi=300, bbox_inches='tight')
plt.show()
