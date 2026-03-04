import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel as C, WhiteKernel
#=== good so far than bayesian3 and 4==========

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
    # ---- contour styling ----
    contour_alpha: float = 0.50,
    contour_lw: float = 1.4,
    # ---- NEW: focus contour density near best (low) region ----
    low_q_start: float = 0.01,      # start quantile (very low values)
    low_q_end: float = 0.35,        # end quantile (still low-ish)
    n_low_levels: int = 22,         # number of levels in low region (more = more rings)
    n_mid_levels: int = 6,          # a few extra levels outside low region (optional)
    save_path: str = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Bayesian_Maps\Graphs\Priority_Length\MAST"
):
    df = pd.read_csv(csv_path)

    X = df[[p1_col, p2_col]].to_numpy(float)
    y = df[y_col].to_numpy(float)

    # Best point (prefer global_best_* if present)
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

    # Optional surrogate background (context only)
    MU = None
    P1g = P2g = None
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

        # ---- NEW: concentrate contour levels in the low (blue) region ----
        mu_flat = MU.ravel()
        lo = np.quantile(mu_flat, low_q_start)
        hi = np.quantile(mu_flat, low_q_end)

        low_levels = np.linspace(lo, hi, n_low_levels)

        # Optional: add a few mid/high levels so the rest of the map still has shape
        if n_mid_levels > 0:
            hi2 = np.quantile(mu_flat, 0.95)
            mid_levels = np.linspace(hi, hi2, n_mid_levels + 1)[1:]  # avoid repeating 'hi'
            levels = np.unique(np.concatenate([low_levels, mid_levels]))
        else:
            levels = low_levels

    # -------------------------
    # Plot
    # -------------------------
    plt.figure(figsize=(11, 7))
    ax = plt.gca()
    ax.set_facecolor("#f2f2f2")

    # Darker + denser contours around best region (no colorbar)
    if show_background_surrogate and MU is not None:
        plt.contour(
            P2g, P1g, MU,
            levels=levels,
            cmap="RdBu_r",
            linewidths=contour_lw,
            alpha=contour_alpha
        )

    # All evaluations: BLACK X marks
    plt.scatter(
        X[:, 1], X[:, 0],
        marker="x",
        c="black",
        s=90,
        linewidths=2.0,
        alpha=0.95,
       # label="Evaluations"
    )

    # Best: RED X mark (no circle)
    plt.scatter(
        [best_p2], [best_p1],
        marker="x",
        c="red",
        s=220,
        linewidths=3.0,
        label=f"Best ({best_source})"
    )

    # Label best value
    plt.text(
        best_p2 + 0.01 * (p2_hi - p2_lo),
        best_p1 + 0.01 * (p1_hi - p1_lo),
        f"{best_y:.4f}",
        color="red"
    )

    plt.xlabel("P2")
    plt.ylabel("P1")
    plt.title("Bayesian Optimization search pattern")
    plt.xlim(p2_lo, p2_hi)
    plt.ylim(p1_lo, p1_hi)

   # plt.legend(loc="best")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Plot saved to: {save_path}")
    plt.show()
    plt.show()


if __name__ == "__main__":
    CSV_PATH = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Priority_Length\BO_MAST\combo_results_Amdahl.csv"

    plot_bo_search_pattern_black_points_red_best(
        csv_path=CSV_PATH,
        show_background_surrogate=True,
        contour_alpha=0.55,
        contour_lw=1.4,
        low_q_start=0.01,
        low_q_end=0.35,
        n_low_levels=20,
        n_mid_levels=6,
    )