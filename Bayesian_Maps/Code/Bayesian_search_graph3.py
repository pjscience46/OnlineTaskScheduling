import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel as C, WhiteKernel


def plot_bo_surface_from_csv(
    csv_path: str,
    p1_col: str = "P1",
    p2_col: str = "P2",
    y_col: str = "value",
    best_p1_col: str = "global_best_P1",
    best_p2_col: str = "global_best_P2",
    best_y_col: str = "global_best_value",
    grid_n: int = 250,
    padding_frac: float = 0.05,
    show_uncertainty: bool = True,
    save_path: str = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Bayesian_Maps\Graphs"
):
    # -------------------------
    # Load and validate data
    # -------------------------
    df = pd.read_csv(csv_path)

    required = {p1_col, p2_col, y_col}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    X = df[[p1_col, p2_col]].to_numpy(dtype=float)
    y = df[y_col].to_numpy(dtype=float)

    # Best point (prefer global_best_* columns if present; else compute from y)
    if {best_p1_col, best_p2_col, best_y_col}.issubset(df.columns):
        best_p1 = float(df[best_p1_col].iloc[-1])
        best_p2 = float(df[best_p2_col].iloc[-1])
        best_y = float(df[best_y_col].iloc[-1])
        best_source = ""
    else:
        best_idx = int(np.argmin(y))
        best_p1, best_p2, best_y = float(X[best_idx, 0]), float(X[best_idx, 1]), float(y[best_idx])
        best_source = "min(value) in data"

    # -------------------------
    # Define plotting bounds
    # Use observed min/max + padding
    # -------------------------
    p1_min, p1_max = np.min(X[:, 0]), np.max(X[:, 0])
    p2_min, p2_max = np.min(X[:, 1]), np.max(X[:, 1])

    # Handle case where all P1 or P2 equal (avoid zero width bounds)
    def pad_bounds(vmin, vmax, frac):
        if np.isclose(vmin, vmax):
            # arbitrary small pad if constant
            delta = 1.0 if np.isclose(vmin, 0.0) else abs(vmin) * 0.1
            return vmin - delta, vmax + delta
        span = vmax - vmin
        return vmin - frac * span, vmax + frac * span

    p1_lo, p1_hi = pad_bounds(p1_min, p1_max, padding_frac)
    p2_lo, p2_hi = pad_bounds(p2_min, p2_max, padding_frac)

    # -------------------------
    # Fit Gaussian Process surrogate
    # -------------------------
    # Kernel choice: Constant * Matern + WhiteKernel for noise
    # (reasonable default for BO-like surfaces)
    kernel = C(1.0, (1e-2, 1e2)) * Matern(length_scale=[0.5, 0.5], length_scale_bounds=(1e-2, 1e2), nu=2.5) \
             + WhiteKernel(noise_level=1e-6, noise_level_bounds=(1e-10, 1e-2))
    

    gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, random_state=0)
    gp.fit(X, y)

    # -------------------------
    # Create grid & predict
    # -------------------------
    p1_grid = np.linspace(p1_lo, p1_hi, grid_n)
    p2_grid = np.linspace(p2_lo, p2_hi, grid_n)
    P1g, P2g = np.meshgrid(p1_grid, p2_grid)

    X_grid = np.column_stack([P1g.ravel(), P2g.ravel()])
    mu, std = gp.predict(X_grid, return_std=True)
    MU = mu.reshape(grid_n, grid_n)
    STD = std.reshape(grid_n, grid_n)

    # -------------------------
    # Plot surrogate mean (objective colors)
    # -------------------------
    plt.figure(figsize=(8, 6))

    # RdBu_r means: low values -> blue, high values -> red
    # SWITCH AXES IN PLOTTING ONLY: x-axis = P2, y-axis = P1
    cf = plt.contourf(P2g, P1g, MU, levels=35, cmap="RdBu_r")
    plt.colorbar(cf, label= None)

    # Light contour lines (structure)
    plt.contour(P2g, P1g, MU, levels=12, colors="k", alpha=0.25, linewidths=0.8)

    # Observed points (x=P2, y=P1)
    plt.scatter(X[:, 1], X[:, 0], marker="x", c="black", s=45, linewidths=1.2)

    # Best marker (x=best_p2, y=best_p1)
    # plt.scatter([best_p2], [best_p1], s=160, facecolors="none", edgecolors="red", linewidths=2.2,
    #             label=f"Best ({best_source})")
    
    plt.scatter([best_p2], [best_p1],
            marker="x",
            c="red",
            s=120,
            linewidths=3,
            label=f"Best ({best_source})")
    plt.text(best_p2 + 0.01*(p2_hi-p2_lo), best_p1 + 0.01*(p1_hi-p1_lo), f"{best_y:.4f}", color="red")

    plt.xlabel("P2")
    plt.ylabel("P1")
    plt.title("Bayesian surrogate objective map")
    plt.xlim(p2_lo, p2_hi)
    plt.ylim(p1_lo, p1_hi)
    #plt.legend(loc="best")
    plt.tight_layout()
    # Save figure if path is provided
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Plot saved to: {save_path}")
    plt.show()

    # Print kernel after fitting (useful diagnostic)
    print("Fitted GP kernel:", gp.kernel_)
    


if __name__ == "__main__":
    # Change this to your CSV filename/path
    CSV_PATH = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_Roofline.csv"

    plot_bo_surface_from_csv(
        csv_path=CSV_PATH,
        grid_n=250,
        padding_frac=0.05,
        show_uncertainty=True
    )