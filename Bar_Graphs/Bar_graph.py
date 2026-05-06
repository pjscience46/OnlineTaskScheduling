import pandas as pd
import matplotlib.pyplot as plt
from pathlib import PureWindowsPath
#note : use this one

# =========================================================
# 1. GIVE ALL CSV PATHS HERE
# =========================================================
csv_paths = [
    # ========================= MAST =========================
    # FCFS
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MAST\combo_results_comm.csv",

    # Length
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MAST\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MAST\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MAST\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MAST\combo_results_comm.csv",

    # Area
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MAST\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MAST\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MAST\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MAST\combo_results_comm.csv",

    # Allocation
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MAST\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MAST\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MAST\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MAST\combo_results_comm.csv",

    # ========================= MTSA =========================
    # FCFS
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTSA\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTSA\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTSA\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTSA\combo_results_comm.csv",

    # Length
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTSA\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTSA\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTSA\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTSA\combo_results_comm.csv",

    # Area
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTSA\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTSA\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTSA\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTSA\combo_results_comm.csv",

    # Allocation
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTSA\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTSA\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTSA\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTSA\combo_results_comm.csv",

    # ========================= MTPA =========================
    # FCFS
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTPA\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTPA\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTPA\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\FCFS\BO_MTPA\combo_results_comm.csv",

    # Length
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTPA\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTPA\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTPA\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Length\BO_MTPA\combo_results_comm.csv",

    # Area
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTPA\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTPA\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTPA\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Area\BO_MTPA\combo_results_comm.csv",

    # Allocation
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTPA\combo_results_Roofline.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTPA\combo_results_General.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTPA\combo_results_Amdahl.csv",
    r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Allocation\BO_MTPA\combo_results_comm.csv",
]

# =========================================================
# 2. ORDER OF DISPLAY
# =========================================================
model_order = ["Roofline", "Communication", "Amdahl", "General"]
algo_order = ["MAST", "MTSA", "MTPA"]
priority_order = ["FCFS", "Allocation", "Length", "Area"]

# =========================================================
# 3. NORMALIZATION MAPS
# =========================================================
algo_map = {
    "BO_MAST": "MAST",
    "BO_MTSA": "MTSA",
    "BO_MTPA": "MTPA"
}

model_map = {
    "Roofline": "Roofline",
    "comm": "Communication",
    "Communication": "Communication",
    "Amdahl": "Amdahl",
    "General": "General"
}

# =========================================================
# 4. EXTRACT MODEL, ALGO, PRIORITY FROM FILE PATH
# =========================================================
def extract_info_from_path(file_path):
    p = PureWindowsPath(file_path)

    # ...\Priority\BO_ALGO\combo_results_Model.csv
    priority = p.parts[-3]
    algo_folder = p.parts[-2]
    filename = p.name

    model_raw = filename.replace("combo_results_", "").replace(".csv", "")

    algo = algo_map.get(algo_folder, algo_folder)
    model = model_map.get(model_raw, model_raw)

    return model, algo, priority

# =========================================================
# 5. GET LAST global_best_value
# =========================================================
def get_last_global_best_value(file_path):
    df = pd.read_csv(file_path)

    if df.empty:
        return None

    if "global_best_value" not in df.columns:
        raise ValueError(f"'global_best_value' column not found in file:\n{file_path}")

    return float(df["global_best_value"].iloc[-1])

# =========================================================
# 6. STORE DATA
# data[model][algo][priority] = value
# =========================================================
data = {
    model: {
        algo: {priority: None for priority in priority_order}
        for algo in algo_order
    }
    for model in model_order
}

all_values = []

for file_path in csv_paths:
    try:
        model, algo, priority = extract_info_from_path(file_path)
        value = get_last_global_best_value(file_path)

        if model in data and algo in data[model] and priority in data[model][algo]:
            data[model][algo][priority] = value
            if value is not None:
                all_values.append(value)
        else:
            print(f"Skipped unexpected file: {file_path}")
            print(f"Parsed -> model={model}, algo={algo}, priority={priority}")

    except Exception as e:
        print(f"Error reading file:\n{file_path}\nReason: {e}\n")

if not all_values:
    raise ValueError("No valid values found. Check the file paths and CSV contents.")

# =========================================================
# 7. CREATE 4x3 GRID OF BAR PLOTS
# =========================================================
fig, axes = plt.subplots(
    nrows=len(model_order),
    ncols=len(algo_order),
    figsize=(9, 9),
    squeeze=False
)

global_max = max(all_values)
y_padding = 0.15 * global_max if global_max > 0 else 1

for i, model in enumerate(model_order):
    for j, algo in enumerate(algo_order):
        ax = axes[i, j]

        vals = [data[model][algo][p] for p in priority_order]
        plot_vals = [v if v is not None else 0 for v in vals]
        # x = range(len(priority_order))
        x = [0, 0.5, 1.0, 1.5]  # Custom x positions for better spacing

        bars = ax.bar(x, plot_vals, width=0.4)

        # Priority names below bars
        ax.set_xticks(list(x))
        ax.set_xticklabels(priority_order, fontsize=9)

        # Common y-scale across all subplots
        ax.set_ylim(0, global_max + y_padding)

        # Add value labels above bars
        for bar, val in zip(bars, vals):
            if val is not None:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.02 * global_max,
                    f"{val:.3f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold"
                )
            else:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    0.02 * global_max,
                    "N/A",
                    ha="center",
                    va="bottom",
                    fontsize=9
                )

        ax.grid(axis="y", linestyle="--", alpha=0.4)

        # Column headers
        if i == 0:
            ax.set_title(algo, fontsize=14, fontweight="bold", pad=12)

        # Row headers
        if j == 0:
            ax.set_ylabel(model, fontsize=13, fontweight="bold", labelpad=20)
        else:
            ax.tick_params(axis="y", labelleft=False)
            ax.set_ylabel("")

# =========================================================
# 8. MAIN TITLE
# =========================================================
# fig.suptitle(
#     "Best global_best_value for Each Model-Algorithm Combination Across Priorities",
#     fontsize=18,
#     fontweight="bold",
#     y=0.98
# )

plt.tight_layout(rect=[0.04, 0.04, 1, 0.96])

# Optional save
save_path = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Bar_Graphs\Bar_graph_image.png"
plt.savefig(save_path, dpi=300, bbox_inches="tight")
print(f"Figure saved at: {save_path}")

plt.show()