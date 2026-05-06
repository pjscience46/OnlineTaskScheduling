import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel as C, WhiteKernel

#Note : this file should be used to generate Bayesina maps. Find for chnag eword to change the code as needed for different algos.
def plot_bo_search_pattern_black_points_red_best(
    csv_path: str,
    p1_col: str = "P1",
    p2_col: str = "P2",
    y_col: str = "value",
    best_p1_col: str = "global_best_P1",
    best_p2_col: str = "global_best_P2",
    best_y_col: str = "global_best_value",
    grid_n: int = 240,
    padding_frac: float = 0.05,
    show_background_surrogate: bool = True,
    contour_alpha: float = 0.50,
    contour_lw: float = 1.4,
    low_q_start: float = 0.01,
    low_q_end: float = 0.20,
    n_low_levels: int = 22,
    n_mid_levels: int = 6,
    save_path: str | None = None,
):
    df = pd.read_csv(csv_path)

    X = df[[p1_col, p2_col]].to_numpy(float)
    y = df[y_col].to_numpy(float)

    # -------------------------
    # Build output path automatically from input CSV path
    # Example:
    # combo_results_General.csv -> General.png
    # -------------------------
    if save_path is None:
        csv_file = Path(csv_path)
        output_dir = csv_file.parent

        stem = csv_file.stem  # combo_results_General
        if stem.startswith("combo_results_"):
            output_name = stem.replace("combo_results_", "", 1) + ".png"
        else:
            output_name = stem + ".png"

        save_path = str(output_dir / output_name)

    # Best point
    if {best_p1_col, best_p2_col, best_y_col}.issubset(df.columns):
        best_p1 = float(df[best_p1_col].iloc[-1])
        best_p2 = float(df[best_p2_col].iloc[-1])
        best_y = float(df[best_y_col].iloc[-1])
        best_source = "global_best_* (last row)"
    else:
        i = int(np.argmin(y))
        best_p1, best_p2, best_y = float(X[i, 0]), float(X[i, 1]), float(y[i])
        best_source = "min(value)"

    # Bounds with padding
    def pad(vmin, vmax, frac):
        if np.isclose(vmin, vmax):
            d = 1.0 if np.isclose(vmin, 0.0) else abs(vmin) * 0.1
            return vmin - d, vmax + d
        span = vmax - vmin
        return vmin - frac * span, vmax + frac * span

    p1_lo, p1_hi = pad(X[:, 0].min(), X[:, 0].max(), padding_frac)
    p2_lo, p2_hi = pad(X[:, 1].min(), X[:, 1].max(), padding_frac)

    # Optional surrogate background
    MU = None
    P1g = P2g = None
    levels = None

    if show_background_surrogate:
        kernel = (
            C(1.0, (1e-2, 1e2))
            * Matern(length_scale=[0.5, 0.5], length_scale_bounds=(1e-2, 1e2), nu=2.5)
            + WhiteKernel(noise_level=1e-6)
        )
        gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, random_state=0)
        gp.fit(X, y)

        p1_grid = np.linspace(p1_lo, p1_hi, grid_n)
        p2_grid = np.linspace(p2_lo, p2_hi, grid_n)
        P1g, P2g = np.meshgrid(p1_grid, p2_grid)

        Xg = np.column_stack([P1g.ravel(), P2g.ravel()])
        MU = gp.predict(Xg).reshape(grid_n, grid_n)

        mu_flat = MU.ravel()
        lo = np.quantile(mu_flat, low_q_start)
        hi = np.quantile(mu_flat, low_q_end)

        low_levels = np.linspace(lo, hi, n_low_levels)

        if n_mid_levels > 0:
            hi2 = np.quantile(mu_flat, 0.95)
            mid_levels = np.linspace(hi, hi2, n_mid_levels + 1)[1:]
            levels = np.unique(np.concatenate([low_levels, mid_levels]))
        else:
            levels = low_levels

    # -------------------------
    # Plot
    # -------------------------
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_axes([0.15, 0.15, 0.75, 0.75])  # fixed position: left, bottom, width, height
    ax.set_facecolor("#f2f2f2")

    if show_background_surrogate and MU is not None and levels is not None:
        #wihout sidebar code
    #     ax.contour(
    # P2g, P1g, MU,
    # levels=levels,
    # cmap="RdBu_r",
    # linewidths=contour_lw,
    # alpha=contour_alpha,
    # zorder=1
# )
        
     ##########################################################################   with sidebar code
        contour = ax.contour(
        P2g, P1g, MU,
        levels=levels,
        cmap="RdBu_r",   # SAME palette (unchanged)
        linewidths=contour_lw,
        alpha=contour_alpha,
        zorder=1
        )

        # ---- ADD COLORBAR (SIDEBAR) ----
                # ---- CLEAN COLORBAR ONLY ----
        positive_levels = levels[levels > 0]

        if len(positive_levels) > 0:
            vmin = positive_levels.min()
            vmax = positive_levels.max()

            norm = Normalize(vmin=vmin, vmax=vmax)
            sm = ScalarMappable(norm=norm, cmap="RdBu_r")
            sm.set_array([])

            cbar = fig.colorbar(sm, ax=ax)

            tick_values = np.linspace(vmin, vmax, 10)
            cbar.set_ticks(tick_values)
            cbar.set_ticklabels([f"{v:.3f}" for v in tick_values])

          
                

     ##############################################################################

    # All evaluations: black X
    ax.scatter(
        X[:, 1], X[:, 0],
        marker="x",
        c="black",
        s=90,
        linewidths=2.0,
        alpha=0.95,
        zorder=3
    )

    # Keep best point inside plot borders
    eps_x = 0.01 * (p2_hi - p2_lo)
    eps_y = 0.01 * (p1_hi - p1_lo)

    best_p2_plot = np.clip(best_p2, p2_lo + eps_x, p2_hi - eps_x)
    best_p1_plot = np.clip(best_p1, p1_lo + eps_y, p1_hi - eps_y)

    # Best: red X
    # ax.scatter(
    #     [best_p2], [best_p1],
    #     marker="x",
    #     c="red",
    #     s=220,
    #     linewidths=3.0,
    # )
    ax.scatter(
    [best_p2_plot], [best_p1_plot],
        marker="x",
        c="red",
        s=220,
        linewidths=3.0,
        zorder=4
    )

    # Label best value
    # ax.text(
    #     best_p2 + 0.01 * (p2_hi - p2_lo),
    #     best_p1 + 0.01 * (p1_hi - p1_lo),
    #     f"{best_y:.4f}",
    #     color="red" 
    # )
    
    # Smart text placement (keeps label inside borders)
    # Smart text placement with SAFE MARGIN from borders
    dx = 0.02 * (p2_hi - p2_lo)
    dy = 0.02 * (p1_hi - p1_lo)

    margin_x = 0.07 * (p2_hi - p2_lo)   # extra safety margin
    margin_y = 0.07 * (p1_hi - p1_lo)

    # Default position
    text_x = best_p2_plot + dx
    text_y = best_p1_plot + dy

    # Flip direction if near edges
    if best_p2_plot > p2_hi - 2 * dx:
        text_x = best_p2_plot - dx
    if best_p2_plot < p2_lo + 2 * dx:
        text_x = best_p2_plot + dx

    # Inverted Y-axis handling
    if best_p1_plot < p1_lo + 2 * dy:
        text_y = best_p1_plot + dy
    if best_p1_plot > p1_hi - 2 * dy:
        text_y = best_p1_plot - dy

    # Enforce minimum distance from borders
    text_x = np.clip(text_x, p2_lo + margin_x, p2_hi - margin_x)
    text_y = np.clip(text_y, p1_lo + margin_y, p1_hi - margin_y)

    # ax.text(
    #     text_x,
    #     text_y,
    #     f"{best_y:.4f}",
    #     color="red"
    # )

    # simple label placement near best point
    if best_p2_plot > p2_hi - 0.10 * (p2_hi - p2_lo):
        offset = (-8, -10)   # move left and slightly down
        ha = "right"
    else:
        offset = (8, -10)    # move right and slightly down
        ha = "left"

    ax.annotate(
        f"{best_y:.4f}",
        xy=(best_p2_plot, best_p1_plot),
        xytext=offset,
        textcoords="offset points",
        color="red",
        fontweight="bold",
        ha=ha,
        va="top",
        zorder=5,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.9, pad=1.2)
    )

#change labels as needed 
    ax.set_xlabel(r'$\beta$', fontsize=16)
    #ax.set_xlabel(r'$\alpha$', fontsize=16)
    # ax.set_xlabel(r'$\gamma$', fontsize=16)
    ax.set_ylabel(r'$\mu$', fontsize=16)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
   
   # plt.title("Bayesian Optimization Search Pattern")
    #ax.set_xlim(p2_lo, p2_hi)
    # ax.set_ylim(p1_lo, p1_hi)
    # ax.set_xlim(0, 1.0)
    # ax.set_xticks(np.arange(0, 1.01, 0.2)) 

 #change
 #for alpha and beta
    ax.set_xlim(1.0, 5.0)
    ax.set_xticks(np.arange(1.0, 5.01, 0.5))
#for gamma
    # ax.set_xlim(0.0, 1.0)
    # ax.set_xticks(np.arange(0.0, 1.01, 0.2))
    
#for mu- same for all
    ax.set_ylim(0.1, 0.9) 
    ax.set_yticks(np.arange(0.1, 0.91, 0.1))
    
    
     


    # Invert Y axis: top to bottom
    ax.invert_yaxis()

   
    plt.savefig(save_path, dpi=300)
    print(f"Plot saved to: {save_path}")

    plt.show()


if __name__ == "__main__":
    # CSV_PATH = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_Roofline.csv"

    # plot_bo_search_pattern_black_points_red_best(
    #     csv_path=CSV_PATH,
    #     show_background_surrogate=True,
    #     contour_alpha=0.55,
    #     contour_lw=1.4,
    #     low_q_start=0.01,
    #     low_q_end=0.2,
    #     n_low_levels=25,
    #     n_mid_levels=4,
    # ) 
#change as needed 
    csv_files = [
    # #     #FCFS
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_comm.csv",
        #Length
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MAST\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MAST\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MAST\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MAST\combo_results_comm.csv",
    #  #Area
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MAST\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MAST\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MAST\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MAST\combo_results_comm.csv",
    # #Allocation
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MAST\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MAST\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MAST\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MAST\combo_results_comm.csv"
    
    # ,


    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTSA\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTSA\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTSA\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTSA\combo_results_comm.csv",
    #     #Length
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTSA\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTSA\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTSA\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTSA\combo_results_comm.csv",
    #  #Area
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTSA\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTSA\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTSA\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTSA\combo_results_comm.csv",
    # #Allocation
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTSA\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTSA\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTSA\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTSA\combo_results_comm.csv"
    
    # ,


    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTPA\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTPA\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTPA\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTPA\combo_results_comm.csv",
    #    # Length
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTPA\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTPA\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTPA\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTPA\combo_results_comm.csv",
    #   #Area
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTPA\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTPA\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTPA\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTPA\combo_results_comm.csv",
    #  #Allocation
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTPA\combo_results_Roofline.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTPA\combo_results_General.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTPA\combo_results_Amdahl.csv",
    # r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTPA\combo_results_comm.csv"


]

for csv_path in csv_files:
    plot_bo_search_pattern_black_points_red_best(
        csv_path=csv_path,
        show_background_surrogate=True,
        contour_alpha=0.55,
        contour_lw=1.4,
        low_q_start=0.01,
        low_q_end=0.2,
        n_low_levels=25,
        n_mid_levels=4,
    )