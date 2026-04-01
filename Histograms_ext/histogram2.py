import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------- LOAD DATA --------------------
main_folder = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\TASKS"

# Read one file
all_files = glob.glob(os.path.join(main_folder, "n=1000", "1.csv"))
#all_files = glob.glob(os.path.join(main_folder, "n=*/", "*.csv"))

# If you want all CSVs from all n=* folders, use this instead:
# all_files = glob.glob(os.path.join(main_folder, "n=*","*.csv"))

df_list = [pd.read_csv(file) for file in all_files]
df = pd.concat(df_list, ignore_index=True)

# -------------------- SAVE FOLDER --------------------
save_folder = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Histograms"
os.makedirs(save_folder, exist_ok=True)

# -------------------- FUNCTION FOR w, d, c --------------------
def plot_power_histogram(data, column_name, power_edges, step=0.5, save_folder=None):
    x = data[column_name].dropna()
    x = x[x > 0]

    total = len(x)

    min_power, max_power = min(power_edges), max(power_edges)
    n_bins = 32

    bins = np.logspace(
        np.log10(x.min()),
        np.log10(x.max()),
        n_bins
    )

    plt.figure(figsize=(8, 6))

    # Relative frequency
    weights = np.ones_like(x) / total

    plt.hist(
        x,
        bins=bins,
        weights=weights,
        edgecolor="black",
        linewidth=1.2,
        rwidth=0.95
    )

    plt.xscale("log")

    ticks = np.arange(min_power, max_power + step, step)
    plt.xticks(10.0 ** ticks, [f"$10^{{{p}}}$" for p in ticks], fontsize=14)
    plt.yticks(fontsize=14)

    if column_name == "w":
        plt.xlabel(r"$w$ (total parallelizable work)", fontsize=14)
        file_name = "hist_w_freq.png"
    elif column_name == "d":
        plt.xlabel(r"$d^\prime$ (sequential fraction)", fontsize=14)
        file_name = "hist_d_freq.png"
    elif column_name == "c":
        plt.xlabel(r"$c^\prime$ (communication overhead)", fontsize=14)
        file_name = "hist_c_freq.png"
    else:
        plt.xlabel(column_name, fontsize=14)
        file_name = f"hist_{column_name}_freq.png"

    plt.ylabel("frequency", fontsize=14)
    plt.tight_layout()

    if save_folder is not None:
        save_path = os.path.join(save_folder, file_name)
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()
    plt.close()

# -------------------- PLOT w, d, c --------------------
plot_power_histogram(df, "w", [2, 5], step=0.5, save_folder=save_folder)
plot_power_histogram(df, "d", [-3, -0.5], step=0.5, save_folder=save_folder)
plot_power_histogram(df, "c", [-6, -2], step=1, save_folder=save_folder)

# -------------------- p HISTOGRAM --------------------
p = df["p"].dropna()
p = p[p > 0]

total = len(p)
bins = np.linspace(1, 1024, 33)   # 32 bins

plt.figure(figsize=(8, 6))

weights = np.ones_like(p) / total

plt.hist(
    p,
    bins=bins,
    weights=weights,
    edgecolor="black",
    linewidth=1.2,
    rwidth=0.95
)

plt.xlabel(r'$\bar{p}$ (maximum degree of parallelism)', fontsize=14)
plt.ylabel("frequency", fontsize=14)

plt.xticks([1, 256, 512, 768, 1024], fontsize=14)
plt.yticks(fontsize=14)
plt.margins(x=0.05)

plt.tight_layout()

save_path = os.path.join(save_folder, "hist_p_freq_.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")

plt.show()
plt.close()