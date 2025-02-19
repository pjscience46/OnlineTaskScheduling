import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_surface_from_csv(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Ensure the data is sorted for proper reshaping
    df = df.sort_values(by=["mu", "beta"])
    
    # Creating meshgrid for plotting
    X_unique = np.unique(df["beta"].values)
    Y_unique = np.unique(df["mu"].values)
    X_mesh, Y_mesh = np.meshgrid(X_unique, Y_unique)
    
    # Pivot the DataFrame to match the meshgrid structure
    Z_mesh = df.pivot(index="mu", columns="beta", values="max").values
    
    # Creating the figure
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # Ensure Z_mesh is properly shaped
    if Z_mesh.shape != X_mesh.shape:
        print("Error: Z_mesh shape does not match X_mesh and Y_mesh shapes.")
        return
    
    # Surface plot
    surf = ax.plot_surface(X_mesh, Y_mesh, Z_mesh, cmap="viridis", edgecolor='k', alpha=0.8)
    
    # Finding max value and its location
    max_index = np.unravel_index(np.argmax(Z_mesh, axis=None), Z_mesh.shape)
    max_beta = X_unique[max_index[1]]
    max_mu = Y_unique[max_index[0]]
    max_value = Z_mesh[max_index]
    
    # Annotating max value
    ax.scatter(max_beta, max_mu, max_value, color='r', s=100, label=f'Max: {max_value:.2f}')
    ax.text(max_beta, max_mu, max_value, f'Max: {max_value:.2f}', color='red', fontsize=12)
    
    # Labels and title
    ax.set_xlabel("Beta")
    ax.set_ylabel("Mu")
    ax.set_zlabel("Max Value")
    ax.set_title("Surface Plot of Max Value")
    
    # Show color bar with correct limits
    cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label("Max Value")
    cbar.mappable.set_clim(df["max"].min(), df["max"].max())
    
    # Show legend
    ax.legend()
    
    # Show plot
    plt.show()

# Example usage:
plot_surface_from_csv("C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mast\Heat_Maps\Amdahl\Generate_Avg_Max.csv")








# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import pandas as pd
# import os
# # Load data from CSV file
# data = pd.read_csv('C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mast\Heat_Maps\Amdahl\Generate_Avg_Max')
# save_directory = r'C:\Thesis\Fresh pull\Onlineschedulingalgo_assorted_1\Results_mast\Surface_Plots\Amdahl'

# # Ensure the save directory exists
# os.makedirs(save_directory, exist_ok=True)

# # Extract columns
# mu = data['mu'].values
# beta = data['beta'].values
# average = data['average'].values
# max_val = data['max'].values

# # Create a grid for plotting
# mu_unique = np.unique(mu)
# beta_unique = np.unique(beta)
# mu_grid, beta_grid = np.meshgrid(mu_unique, beta_unique)

# # Reshape data to fit the grid
# average_grid = average.reshape(len(beta_unique), len(mu_unique))
# max_grid = max_val.reshape(len(beta_unique), len(mu_unique))

# # # Plotting for Average
# # fig1 = plt.figure(figsize=(7, 6))
# # ax1 = fig1.add_subplot(111, projection='3d')
# # surf1 = ax1.plot_surface(mu_grid, beta_grid, average_grid, cmap='viridis', edgecolor='k',vmin=average.min(), vmax=average.max())
# # ax1.set_title('Surface Plot for Average')
# # ax1.set_xlabel('Mu')
# # ax1.set_ylabel('beta')
# # ax1.set_zlabel('Average')
# # fig1.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10)
# # average_surfaceplot_path = os.path.join(save_directory, 'Surface_Plot_average.png')
# # plt.savefig(average_surfaceplot_path)
# # plt.tight_layout()
# # plt.show()

# # Plotting for Max
# fig2 = plt.figure(figsize=(7, 6))
# ax2 = fig2.add_subplot(111, projection='3d')
# surf2 = ax2.plot_surface(mu_grid, beta_grid, max_grid, cmap='plasma', edgecolor='k',vmin=max_val.min(), vmax=max_val.max())
# ax2.set_title('Surface Plot for Max')
# ax2.set_xlabel('Mu')
# ax2.set_ylabel('beta')
# ax2.set_zlabel('Max')
# fig2.colorbar(surf2, ax=ax2, shrink=0.5, aspect=10)
# max_surfaceplot_path = os.path.join(save_directory, 'Surface_Plot_max.png')
# plt.savefig(max_surfaceplot_path)
# plt.tight_layout()
# plt.show()
