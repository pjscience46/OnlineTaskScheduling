import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import PureWindowsPath
import numpy as np
from matplotlib.patches import Patch

# =========================================================
# 1. BASE PATH
# =========================================================
base_dir = r"C:\Thesis\Paper1\Extension_Fair_algo\EXT_Fair_algo\OnlineTaskScheduling"

# =========================================================
# 2. PRIORITY FOLDER -> FILE SUFFIX
# Allocation folder uses combo_results_Alloc.csv
# =========================================================
priority_file_map = {
    "FCFS": "FCFS",
    "Length": "Length",
    "Allocation": "Alloc",
    "Area": "Area"
}

# =========================================================
# 3. ALGORITHM FOLDER -> DISPLAY NAME
# =========================================================
algo_folder_map = {
    "BO_Fair": "FAIR",
    "BO_MAST": "MAST",
    "BO_MTSA": "MTSA",
    "BO_MTPA": "MTPA"
}

algo_order = ["FAIR", "MAST", "MTSA", "MTPA"]

priority_order = ["FCFS", "Allocation", "Area", "Length"]

priority_labels = {
    "FCFS": "FIFO",
    "Allocation": "procs",
    "Area": "area",
    "Length": "length"
}

priority_colors = {
    "FCFS": "#7fcdbb",
    "Allocation": "#fc8d62",
    "Area": "#a6d854",
    "Length": "#c994c7"
}

# =========================================================
# 4. AUTO-GENERATE ALL CSV PATHS
# =========================================================
csv_paths = []

for priority_folder, file_suffix in priority_file_map.items():
    for algo_folder in algo_folder_map.keys():
        path = rf"{base_dir}\{priority_folder}\{algo_folder}\combo_results_{file_suffix}.csv"
        csv_paths.append(path)

# =========================================================
# 5. EXTRACT ALGO AND PRIORITY FROM PATH
# =========================================================
def extract_info_from_path(file_path):
    p = PureWindowsPath(file_path)

    priority_folder = p.parts[-3]
    algo_folder = p.parts[-2]

    algo = algo_folder_map.get(algo_folder, algo_folder)

    return algo, priority_folder

# =========================================================
# 6. READ VALUES FROM CSV
# =========================================================
def get_boxplot_values_and_best_value(file_path):
    df = pd.read_csv(file_path)

    if df.empty:
        return [], None

    if "value" not in df.columns:
        raise ValueError(f"'value' column not found in file:\n{file_path}")

    box_values = df["value"].dropna().astype(float).tolist()

    if "global_best_value" in df.columns and not df["global_best_value"].dropna().empty:
        best_value = float(df["global_best_value"].dropna().iloc[-1])
    else:
        best_value = min(box_values) if box_values else None

    return box_values, best_value

# =========================================================
# 7. STORE DATA
# box_data[algo][priority] = list of BO values
# best_data[algo][priority] = final global_best_value
# =========================================================
box_data = {
    algo: {priority: [] for priority in priority_order}
    for algo in algo_order
}

best_data = {
    algo: {priority: None for priority in priority_order}
    for algo in algo_order
}

for file_path in csv_paths:
    if not os.path.exists(file_path):
        print(f"File not found, skipped:\n{file_path}\n")
        continue

    try:
        algo, priority = extract_info_from_path(file_path)
        values, best_value = get_boxplot_values_and_best_value(file_path)

        if algo in box_data and priority in box_data[algo]:
            box_data[algo][priority] = values
            best_data[algo][priority] = best_value
        else:
            print(f"Skipped unexpected file: {file_path}")
            print(f"Parsed -> algo={algo}, priority={priority}")

    except Exception as e:
        print(f"Error reading file:\n{file_path}\nReason: {e}\n")

# =========================================================
# 8. Y-LIMIT FUNCTION
# Used only for MAST, MTSA, MTPA.
# FAIR uses fixed scale separately.
# =========================================================
def get_subplot_ylim(values_list, best_vals):
    flat = []

    for vals in values_list:
        flat.extend(vals)

    flat = [v for v in flat if pd.notna(v)]
    best_vals = [v for v in best_vals if v is not None and pd.notna(v)]

    if not flat and not best_vals:
        return 0, 5

    combined = flat + best_vals

    # Ignore extreme upper outliers for scaling
    upper_cut = np.percentile(combined, 95)
    filtered = [v for v in combined if v <= upper_cut]

    combined_for_scale = filtered if len(filtered) > 0 else combined

    y_min = min(combined_for_scale)
    y_max = max(combined_for_scale)

    data_range = y_max - y_min

    if data_range <= 0:
        padding_bottom = 0.5
        padding_top = 1.2
    else:
        padding_bottom = 0.25 * data_range
        padding_top = 0.50 * data_range

    lower = max(0, y_min - padding_bottom)
    upper = y_max + padding_top

    if upper - lower < 1.0:
        upper = lower + 1.0

    return lower, upper

# =========================================================
# 9. CUSTOM LOWER CAP FUNCTION
# =========================================================
def draw_visible_lower_caps(ax, data_to_plot, valid_positions, box_width, y_lower, y_upper):
    """
    Draws a visible lower cap line for every box.

    This fixes the visual issue where the box starts directly from the bottom
    because min value and Q1 are same or very close.
    """
    y_range = y_upper - y_lower
    tiny_offset = 0.015 * y_range

    for vals, pos in zip(data_to_plot, valid_positions):
        if not vals:
            continue

        vals = np.array(vals, dtype=float)
        vals = vals[~np.isnan(vals)]

        if len(vals) == 0:
            continue

        min_val = np.min(vals)
        q1 = np.percentile(vals, 25)

        if abs(min_val - q1) < 1e-8:
            cap_y = min_val - tiny_offset
        else:
            cap_y = min_val

        cap_half_width = box_width * 0.28

        ax.hlines(
            y=cap_y,
            xmin=pos - cap_half_width,
            xmax=pos + cap_half_width,
            colors="black",
            linewidth=1.5,
            zorder=8,
            clip_on=False
        )

# =========================================================
# 10. CREATE ONE ROW OF BOXPLOTS
# =========================================================
fig, axes = plt.subplots(
    nrows=1,
    ncols=len(algo_order),
    figsize=(13, 3.8),
    squeeze=False
)

box_width = 0.28
positions = [0, 0.5, 1.0, 1.5]

for j, algo in enumerate(algo_order):
    ax = axes[0, j]

    data_to_plot = []
    valid_positions = []
    valid_priorities = []

    subplot_values = []
    subplot_bests = []

    for pos, priority in zip(positions, priority_order):
        values = box_data[algo][priority]
        best_value = best_data[algo][priority]

        subplot_values.append(values)
        subplot_bests.append(best_value)

        if values:
            data_to_plot.append(values)
            valid_positions.append(pos)
            valid_priorities.append(priority)

    # =====================================================
    # Y-axis scale
    # FAIR only uses fixed y-axis.
    # MAST, MTSA, MTPA use original automatic y-axis scaling.
    # =====================================================
    if algo == "FAIR":
        y_lower, y_upper = 3.35, 3.45
    else:
        y_lower, y_upper = get_subplot_ylim(
            subplot_values,
            subplot_bests
        )

    if data_to_plot:
        bp = ax.boxplot(
            data_to_plot,
            positions=valid_positions,
            widths=box_width,
            patch_artist=True,
            showmeans=False,
            showfliers=True,

            medianprops=dict(
                color="black",
                linewidth=1.5,
                zorder=4
            ),

            boxprops=dict(
                linewidth=1.4,
                color="black",
                zorder=3
            ),

            whiskerprops=dict(
                linewidth=1.3,
                color="black",
                zorder=3
            ),

            capprops=dict(
                linewidth=1.3,
                color="black",
                zorder=3
            ),

            flierprops=dict(
                marker="o",
                markerfacecolor="white",
                markeredgecolor="black",
                markersize=3,
                linestyle="none",
                zorder=1
            )
        )

        for box, priority in zip(bp["boxes"], valid_priorities):
            box.set_facecolor(priority_colors[priority])
            box.set_edgecolor("black")
            box.set_alpha(1.0)
            box.set_zorder(3)

    ax.set_ylim(y_lower, y_upper)

    # FAIR tick marks: 3.00, 3.25, 3.50, 3.75
    if algo == "FAIR":
        ax.set_yticks(np.arange(3.35, 3.46, 0.01))

    draw_visible_lower_caps(
        ax=ax,
        data_to_plot=data_to_plot,
        valid_positions=valid_positions,
        box_width=box_width,
        y_lower=y_lower,
        y_upper=y_upper
    )

    # =====================================================
    # Top global best value labels
    # =====================================================
    label_y = y_upper - 0.12 * (y_upper - y_lower)

    for pos, priority in zip(positions, priority_order):
        best_value = best_data[algo][priority]

        label_text = f"{best_value:.3f}" if best_value is not None else "N/A"

        ax.text(
            pos,
            label_y,
            label_text,
            ha="center",
            va="center",
            fontsize=9,
            fontweight="bold",
            zorder=20,
            clip_on=False,
            bbox=dict(
                facecolor="white",
                edgecolor="none",
                alpha=0.92,
                pad=0.25
            )
        )

    ax.set_xticks(positions)
    ax.set_xticklabels(
        [priority_labels[p] for p in priority_order],
        fontsize=10
    )

    ax.tick_params(axis="y", labelsize=10)

    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)

    ax.set_title(
        algo,
        fontsize=15,
        fontweight="bold",
        pad=10
    )

    ax.set_ylabel("")

    for side in ["bottom", "left", "top", "right"]:
        ax.spines[side].set_visible(True)
        ax.spines[side].set_color("black")
        ax.spines[side].set_linewidth(1.1)
        ax.spines[side].set_zorder(10)

    ax.tick_params(
        axis="both",
        which="both",
        direction="out",
        length=4,
        width=1.0,
        colors="black"
    )

# =========================================================
# 11. LEGEND
# =========================================================
legend_handles = [
    Patch(facecolor=priority_colors["FCFS"], edgecolor="black", label="FIFO"),
    Patch(facecolor=priority_colors["Allocation"], edgecolor="black", label="procs"),
    Patch(facecolor=priority_colors["Area"], edgecolor="black", label="area"),
    Patch(facecolor=priority_colors["Length"], edgecolor="black", label="length"),
]

fig.legend(
    handles=legend_handles,
    loc="upper center",
    ncol=4,
    frameon=True,
    fontsize=11,
    bbox_to_anchor=(0.5, 1.08)
)

plt.tight_layout(rect=[0.02, 0.02, 1, 0.92])

# =========================================================
# 12. SAVE FIGURE
# =========================================================
save_dir = rf"{base_dir}\Box_Plots"
save_path = rf"{save_dir}\Box_plot_one_row_all_algorithms.png"

os.makedirs(save_dir, exist_ok=True)

plt.savefig(save_path, dpi=300, bbox_inches="tight")
print(f"Figure saved at: {save_path}")

plt.show()