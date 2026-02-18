import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def draw_heatmap(csv_file, save_file=None):
    df = pd.read_csv(csv_file)

  
    p1_full = np.round(np.arange(0.1, 1.0, 0.1), 1)  # 0.1..0.9

    # Pivot: rows=P1 (y), cols=P2 (x)
    heatmap_data = df.pivot(index="P1", columns="P2", values="value")
    heatmap_data = heatmap_data.reindex(index=p1_full)
    heatmap_data = heatmap_data.sort_index(axis=1)

    values = heatmap_data.values
    data = np.ma.masked_invalid(values)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(data, origin="lower", aspect="auto", cmap="viridis")
    fig.colorbar(im, ax=ax)

    # ticks/labels
    ax.set_yticks(np.arange(heatmap_data.shape[0]))
    ax.set_yticklabels(heatmap_data.index)   # will show 0.1..0.9

    ax.set_xticks(np.arange(heatmap_data.shape[1]))
    ax.set_xticklabels(heatmap_data.columns)


    ax.set_ylabel(r"$\mu$")
    ax.set_xlabel(r"$\alpha$")
   
    #ax.set_title("Heatmap of Value over P1 and P2")

    # write values in cells
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            v = values[i, j]
            if np.isfinite(v):
                ax.text(j, i, f"{v:.3f}", ha="center", va="center", color="white", fontsize=9)

# f"{v:.2f}, str(v)

    if save_file is not None:
        plt.savefig(save_file, dpi=300, bbox_inches="tight")
    plt.tight_layout()
    plt.show()

csv_file_path = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Priority_Processor\BO_MTSA\combo_results_Roofline.csv"
save_file = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Priority_Processor\BO_MTSA\Roofline_heatmap.png"

draw_heatmap(csv_file_path, save_file)
