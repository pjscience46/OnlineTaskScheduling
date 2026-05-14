import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import PureWindowsPath
import numpy as np
from matplotlib.patches import Patch

# =========================================================
# 1. BASE PATH
# =========================================================
base_dir = r"C:\repos\EXTENSION_SCHEDULING\OnlineTaskScheduling"

# =========================================================
# 2. AUTO-GENERATE ALL CSV PATHS
# =========================================================
priority_folders = ["FCFS", "Length", "Area", "Allocation"]
algo_folders = ["BO_MAST", "BO_MTSA", "BO_MTPA"]

model_files = {
    "Roofline": "combo_results_Roofline.csv",
    "General": "combo_results_General.csv",
    "Amdahl": "combo_results_Amdahl.csv",
    "Communication": "combo_results_comm.csv"
}

csv_paths = []

for priority in priority_folders:
    for algo_folder in algo_folders:
        for _, file_name in model_files.items():
            path = rf"{base_dir}\{priority}\{algo_folder}\{file_name}"
            csv_paths.append(path)

# =========================================================
# 3. ORDER OF DISPLAY
# =========================================================
model_order = ["Roofline", "Communication", "Amdahl", "General"]
algo_order = ["MAST", "MTSA", "MTPA"]

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
# 4. NORMALIZATION MAPS
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
# 5. EXTRACT MODEL, ALGO, PRIORITY FROM FILE PATH
# =========================================================
def extract_info_from_path(file_path):
    p = PureWindowsPath(file_path)

    priority = p.parts[-3]
    algo_folder = p.parts[-2]
    filename = p.name

    model_raw = filename.replace("combo_results_", "").replace(".csv", "")

    algo = algo_map.get(algo_folder, algo_folder)
    model = model_map.get(model_raw, model_raw)

    return model, algo, priority

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
# =========================================================
box_data = {
    model: {
        algo: {priority: [] for priority in priority_order}
        for algo in algo_order
    }
    for model in model_order
}

best_data = {
    model: {
        algo: {priority: None for priority in priority_order}
        for algo in algo_order
    }
    for model in model_order
}

for file_path in csv_paths:
    try:
        model, algo, priority = extract_info_from_path(file_path)
        values, best_value = get_boxplot_values_and_best_value(file_path)

        if model in box_data and algo in box_data[model] and priority in box_data[model][algo]:
            box_data[model][algo][priority] = values
            best_data[model][algo][priority] = best_value
        else:
            print(f"Skipped unexpected file: {file_path}")
            print(f"Parsed -> model={model}, algo={algo}, priority={priority}")

    except Exception as e:
        print(f"Error reading file:\n{file_path}\nReason: {e}\n")

# =========================================================
# 8. Y-LIMIT FUNCTION
# =========================================================
def get_subplot_ylim(values_list, best_vals, model, algo):
    flat = []

    for vals in values_list:
        flat.extend(vals)

    flat = [v for v in flat if pd.notna(v)]
    best_vals = [v for v in best_vals if v is not None and pd.notna(v)]

    if not flat and not best_vals:
        return 0, 5

    combined = flat + best_vals

    if model == "Roofline" and algo == "MTPA":
        filtered = [v for v in combined if v < 20]
        combined_for_scale = filtered if len(filtered) > 0 else combined
    else:
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

        # If lower whisker overlaps with box bottom, move cosmetic cap slightly below.
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
# 10. CREATE 4x3 GRID OF BOXPLOTS
# =========================================================
fig, axes = plt.subplots(
    nrows=len(model_order),
    ncols=len(algo_order),
    figsize=(10, 10),
    squeeze=False
)

box_width = 0.28

for i, model in enumerate(model_order):
    for j, algo in enumerate(algo_order):
        ax = axes[i, j]

        positions = [0, 0.5, 1.0, 1.5]

        data_to_plot = []
        valid_positions = []
        valid_priorities = []

        subplot_values = []
        subplot_bests = []

        for pos, priority in zip(positions, priority_order):
            values = box_data[model][algo][priority]
            best_value = best_data[model][algo][priority]

            subplot_values.append(values)
            subplot_bests.append(best_value)

            if values:
                data_to_plot.append(values)
                valid_positions.append(pos)
                valid_priorities.append(priority)

        y_lower, y_upper = get_subplot_ylim(
            subplot_values,
            subplot_bests,
            model,
            algo
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

        # Draw visible lower cap lines after setting y-limits
        draw_visible_lower_caps(
            ax=ax,
            data_to_plot=data_to_plot,
            valid_positions=valid_positions,
            box_width=box_width,
            y_lower=y_lower,
            y_upper=y_upper
        )

        # Top global best value labels
        label_y = y_upper - 0.12 * (y_upper - y_lower)

        for pos, priority in zip(positions, priority_order):
            best_value = best_data[model][algo][priority]

            label_text = f"{best_value:.3f}" if best_value is not None else "N/A"

            ax.text(
                pos,
                label_y,
                label_text,
                ha="center",
                va="center",
                fontsize=10,
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
            fontsize=11
        )

        ax.tick_params(axis="y", labelsize=11)

        ax.set_axisbelow(True)
        ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)

        if i == 0:
            ax.set_title(
                algo,
                fontsize=18,
                fontweight="bold",
                pad=14
            )

        ax.set_ylabel("")

        if j == 0:
            ax.text(
                -0.30,
                0.5,
                model,
                transform=ax.transAxes,
                rotation=90,
                va="center",
                ha="center",
                fontsize=16,
                fontweight="bold"
            )

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
    fontsize=13,
    bbox_to_anchor=(0.5, 0.98)
)

plt.tight_layout(rect=[0.03, 0.03, 1, 0.92])

# =========================================================
# 12. SAVE FIGURE
# =========================================================
save_path = rf"{base_dir}\Box_Plots\Box_plot_image_final_with_bottom_caps.png"

os.makedirs(os.path.dirname(save_path), exist_ok=True)

plt.savefig(save_path, dpi=300, bbox_inches="tight")
print(f"Figure saved at: {save_path}")

plt.show()