import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel as C, WhiteKernel


# =========================================================
# 1. BASE DIRECTORY
# =========================================================
base_dir = r"C:\Thesis\Paper1\Extension_Fair_algo\EXT_Fair_algo\OnlineTaskScheduling"


# =========================================================
# 2. PRIORITY FOLDER -> FILE SUFFIX
# Allocation folder has combo_results_Alloc.csv
# =========================================================
priority_file_map = {
    "FCFS": "FCFS",
    "Length": "Length",
    "Allocation": "Alloc",
    "Area": "Area"
}


# =========================================================
# 3. ALGORITHMS
# =========================================================
algo_folders = [
    "BO_Fair",
    "BO_MAST",
    "BO_MTSA",
    "BO_MTPA"
]


# =========================================================
# 4. AUTO-GENERATE ALL CSV PATHS
#
# Example:
# FCFS\BO_Fair\combo_results_FCFS.csv
# FCFS\BO_MAST\combo_results_FCFS.csv
# Allocation\BO_MTPA\combo_results_Alloc.csv
# =========================================================
csv_files = []

for priority_folder, file_suffix in priority_file_map.items():
    for algo_folder in algo_folders:
        csv_path = rf"{base_dir}\{priority_folder}\{algo_folder}\combo_results_{file_suffix}.csv"
        csv_files.append(csv_path)


# =========================================================
# 5. GET INFO FROM PATH
# =========================================================
def get_path_info(csv_path):
    p = Path(csv_path)

    priority_folder = p.parts[-3]
    algo_folder = p.parts[-2]

    return priority_folder, algo_folder


# =========================================================
# 6. BUILD SAVE PATH
# Save graph inside the same algorithm folder
#
# Example:
# FCFS\BO_Fair\Bayesian_Search_FCFS_BO_Fair.png
# Allocation\BO_MAST\Bayesian_Search_Allocation_BO_MAST.png
# =========================================================
def build_save_path(csv_path):
    p = Path(csv_path)

    output_dir = p.parent

    output_name = "Bayesian_Graph.png"

    return str(output_dir / output_name)


# =========================================================
# 7. GET PARAMETER SETTINGS BASED ON ALGORITHM
# =========================================================
def get_algo_axis_settings(algo_folder):
    if algo_folder == "BO_MAST":
        p2_label = r"$\beta$"
        p2_xlim = (1.0, 5.0)
        p2_xticks = np.arange(1.0, 5.01, 0.5)

    elif algo_folder == "BO_MTSA":
        p2_label = r"$\alpha$"
        p2_xlim = (1.0, 5.0)
        p2_xticks = np.arange(1.0, 5.01, 0.5)

    elif algo_folder == "BO_MTPA":
        p2_label = r"$\gamma$"
        p2_xlim = (0.0, 1.0)
        p2_xticks = np.arange(0.0, 1.01, 0.2)

    else:
        p2_label = r"$P2$"
        p2_xlim = None
        p2_xticks = None

    return p2_label, p2_xlim, p2_xticks


# =========================================================
# 8. FIT GP SURROGATE
# =========================================================
def fit_gp(X, y):
    n_features = X.shape[1]

    kernel = (
        C(1.0, (1e-3, 1e3))
        * Matern(
            length_scale=[0.1] * n_features,
            length_scale_bounds=(1e-2, 1e2),
            nu=2.5
        )
        + WhiteKernel(noise_level=1e-6)
    )

    gp = GaussianProcessRegressor(
        kernel=kernel,
        normalize_y=True,
        n_restarts_optimizer=2,
        random_state=0
    )

    gp.fit(X, y)

    return gp


# =========================================================
# 9. 2D BAYESIAN CONTOUR PLOT
# For BO_MAST, BO_MTSA, BO_MTPA
# =========================================================
def plot_2d_bayesian_map(
    csv_path,
    p1_col="P1",
    p2_col="P2",
    y_col="value",
    best_p1_col="global_best_P1",
    best_p2_col="global_best_P2",
    best_y_col="global_best_value",
    grid_n=240,
    padding_frac=0.05,
    contour_alpha=0.55,
    contour_lw=1.4,
    low_q_start=0.01,
    low_q_end=0.20,
    n_low_levels=25,
    n_mid_levels=4
):
    df = pd.read_csv(csv_path)

    if df.empty:
        print(f"Skipped empty file: {csv_path}")
        return

    required_cols = [p1_col, p2_col, y_col]

    for col in required_cols:
        if col not in df.columns:
            print(f"Skipped because '{col}' is missing: {csv_path}")
            return

    priority_folder, algo_folder = get_path_info(csv_path)
    p2_label, p2_xlim, p2_xticks = get_algo_axis_settings(algo_folder)

    save_path = build_save_path(csv_path)

    X = df[[p1_col, p2_col]].to_numpy(float)
    y = df[y_col].to_numpy(float)

    # =====================================================
    # Best point
    # =====================================================
    if {best_p1_col, best_p2_col, best_y_col}.issubset(df.columns):
        best_p1 = float(df[best_p1_col].dropna().iloc[-1])
        best_p2 = float(df[best_p2_col].dropna().iloc[-1])
        best_y = float(df[best_y_col].dropna().iloc[-1])
    else:
        best_idx = int(np.argmin(y))
        best_p1 = float(X[best_idx, 0])
        best_p2 = float(X[best_idx, 1])
        best_y = float(y[best_idx])

    # =====================================================
    # Bounds with padding
    # =====================================================
    def pad(vmin, vmax, frac):
        if np.isclose(vmin, vmax):
            d = 1.0 if np.isclose(vmin, 0.0) else abs(vmin) * 0.1
            return vmin - d, vmax + d

        span = vmax - vmin
        return vmin - frac * span, vmax + frac * span

    p1_lo, p1_hi = pad(X[:, 0].min(), X[:, 0].max(), padding_frac)
    p2_lo, p2_hi = pad(X[:, 1].min(), X[:, 1].max(), padding_frac)

    # =====================================================
    # GP surrogate
    # =====================================================
    gp = fit_gp(X, y)

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

    # =====================================================
    # Plot
    # =====================================================
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_axes([0.15, 0.15, 0.75, 0.75])
    ax.set_facecolor("#f2f2f2")

    contour = ax.contour(
        P2g,
        P1g,
        MU,
        levels=levels,
        cmap="RdBu_r",
        linewidths=contour_lw,
        alpha=contour_alpha,
        zorder=1
    )

    # =====================================================
    # Sidebar / colorbar
    # =====================================================
    positive_levels = levels[levels > 0]

    if len(positive_levels) > 0:
        vmin = positive_levels.min()
        vmax = positive_levels.max()
    else:
        vmin = levels.min()
        vmax = levels.max()

    norm = Normalize(vmin=vmin, vmax=vmax)
    sm = ScalarMappable(norm=norm, cmap="RdBu_r")
    sm.set_array([])

    cbar = fig.colorbar(sm, ax=ax)

    tick_values = np.linspace(vmin, vmax, 10)
    cbar.set_ticks(tick_values)
    cbar.set_ticklabels([f"{v:.3f}" for v in tick_values])
    cbar.ax.tick_params(labelsize=10)

    # =====================================================
    # All evaluations: black X
    # =====================================================
    ax.scatter(
        X[:, 1],
        X[:, 0],
        marker="x",
        c="black",
        s=90,
        linewidths=2.0,
        alpha=0.95,
        zorder=3
    )

    # =====================================================
    # Keep best point inside plot border
    # =====================================================
    eps_x = 0.01 * (p2_hi - p2_lo)
    eps_y = 0.01 * (p1_hi - p1_lo)

    best_p2_plot = np.clip(best_p2, p2_lo + eps_x, p2_hi - eps_x)
    best_p1_plot = np.clip(best_p1, p1_lo + eps_y, p1_hi - eps_y)

    ax.scatter(
        [best_p2_plot],
        [best_p1_plot],
        marker="x",
        c="red",
        s=220,
        linewidths=3.0,
        zorder=4
    )

    # =====================================================
    # Best value label
    # =====================================================
    if best_p2_plot > p2_hi - 0.10 * (p2_hi - p2_lo):
        offset = (-8, -10)
        ha = "right"
    else:
        offset = (8, -10)
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
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.9,
            pad=1.2
        )
    )

    # =====================================================
    # Axis labels
    # x-axis = P2 parameter
    # y-axis = mu
    # =====================================================
    ax.set_xlabel(p2_label, fontsize=16)
    ax.set_ylabel(r"$\mu$", fontsize=16)

    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=12)

    if p2_xlim is not None:
        ax.set_xlim(p2_xlim[0], p2_xlim[1])

    if p2_xticks is not None:
        ax.set_xticks(p2_xticks)

    ax.set_ylim(0.1, 0.9)
    ax.set_yticks(np.arange(0.1, 0.91, 0.1))

    ax.invert_yaxis()

    # No title
    # No legend

    for side in ["bottom", "left", "top", "right"]:
        ax.spines[side].set_visible(True)
        ax.spines[side].set_color("black")
        ax.spines[side].set_linewidth(1.1)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Saved 2D Bayesian map: {save_path}")

    plt.show()


# =========================================================
# 10. 1D BAYESIAN PLOT
# For BO_Fair only
# P1 = mu
# =========================================================
def plot_1d_fair_bayesian_map(
    csv_path,
    p1_col="P1",
    y_col="value",
    best_p1_col="global_best_P1",
    best_y_col="global_best_value",
    grid_n=300
):
    df = pd.read_csv(csv_path)

    if df.empty:
        print(f"Skipped empty file: {csv_path}")
        return

    required_cols = [p1_col, y_col]

    for col in required_cols:
        if col not in df.columns:
            print(f"Skipped because '{col}' is missing: {csv_path}")
            return

    priority_folder, algo_folder = get_path_info(csv_path)
    save_path = build_save_path(csv_path)

    x = df[p1_col].to_numpy(float)
    y = df[y_col].to_numpy(float)

    X = x.reshape(-1, 1)

    # =====================================================
    # Best point
    # =====================================================
    if {best_p1_col, best_y_col}.issubset(df.columns):
        best_p1 = float(df[best_p1_col].dropna().iloc[-1])
        best_y = float(df[best_y_col].dropna().iloc[-1])
    else:
        best_idx = int(np.argmin(y))
        best_p1 = float(x[best_idx])
        best_y = float(y[best_idx])

    # =====================================================
    # GP surrogate
    # =====================================================
    gp = fit_gp(X, y)

    x_grid = np.linspace(0.1, 0.9, grid_n)
    X_grid = x_grid.reshape(-1, 1)

    mu_pred, sigma_pred = gp.predict(X_grid, return_std=True)

    # =====================================================
    # Plot
    # =====================================================
    fig = plt.figure(figsize=(8, 5.5))
    ax = fig.add_axes([0.15, 0.15, 0.75, 0.75])
    ax.set_facecolor("#f2f2f2")

    # GP mean line
    ax.plot(
        x_grid,
        mu_pred,
        color="black",
        linewidth=1.8,
        alpha=0.9,
        zorder=2
    )

    # Uncertainty band
    ax.fill_between(
        x_grid,
        mu_pred - sigma_pred,
        mu_pred + sigma_pred,
        color="gray",
        alpha=0.25,
        zorder=1
    )

    # Evaluated points colored by value, so sidebar is meaningful
    scatter = ax.scatter(
        x,
        y,
        marker="x",
        c=y,
        cmap="RdBu_r",
        s=90,
        linewidths=2.0,
        alpha=0.95,
        zorder=3
    )

    # Sidebar / colorbar
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.ax.tick_params(labelsize=10)

    # Best point
    ax.scatter(
        [best_p1],
        [best_y],
        marker="x",
        c="red",
        s=220,
        linewidths=3.0,
        zorder=4
    )

    ax.annotate(
        f"{best_y:.4f}",
        xy=(best_p1, best_y),
        xytext=(8, -10),
        textcoords="offset points",
        color="red",
        fontweight="bold",
        ha="left",
        va="top",
        zorder=5,
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.9,
            pad=1.2
        )
    )

    ax.set_xlabel(r"$\mu$", fontsize=16)
    ax.set_ylabel("Makespan Ratio", fontsize=16)

    ax.set_xlim(0.1, 0.9)
    ax.set_xticks(np.arange(0.1, 0.91, 0.1))

    y_min = min(np.min(y), np.min(mu_pred - sigma_pred), best_y)
    y_max = max(np.max(y), np.max(mu_pred + sigma_pred), best_y)

    y_range = y_max - y_min

    if y_range <= 0:
        y_range = 1.0

    ax.set_ylim(
        max(0, y_min - 0.12 * y_range),
        y_max + 0.18 * y_range
    )

    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=12)

    ax.grid(True, linestyle="--", alpha=0.4)

    # No title
    # No legend

    for side in ["bottom", "left", "top", "right"]:
        ax.spines[side].set_visible(True)
        ax.spines[side].set_color("black")
        ax.spines[side].set_linewidth(1.1)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Saved 1D FAIR Bayesian map: {save_path}")

    plt.show()


# =========================================================
# 11. MAIN DRIVER
# =========================================================
if __name__ == "__main__":

    for csv_path in csv_files:
        if not os.path.exists(csv_path):
            print(f"File not found, skipped: {csv_path}")
            continue

        priority_folder, algo_folder = get_path_info(csv_path)

        print("\nProcessing:")
        print(f"Priority: {priority_folder}")
        print(f"Algorithm: {algo_folder}")
        print(f"CSV: {csv_path}")

        if algo_folder == "BO_Fair":
            plot_1d_fair_bayesian_map(csv_path)
        else:
            plot_2d_bayesian_map(
                csv_path=csv_path,
                contour_alpha=0.55,
                contour_lw=1.4,
                low_q_start=0.01,
                low_q_end=0.20,
                n_low_levels=25,
                n_mid_levels=4
            )