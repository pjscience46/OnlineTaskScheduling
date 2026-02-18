import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


data = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\TASKS\n=1000\1.csv"  
df = pd.read_csv(data)
out_dir = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\Histograms_ext"
os.makedirs(out_dir, exist_ok=True)

# ----------------- LOG histograms for w, d, c -----------------
for col in ["w", "d", "c"]:
    x = df[col].dropna()
    x = x[x > 0]  # log requires positive values

    plt.figure()
    plt.hist(np.log10(x), bins=30)
    plt.title(f"Histogram of log10({col})")
    plt.xlabel(f"log10({col})")
    plt.ylabel("count")
    save_path = os.path.join(out_dir, f"hist_{col}.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


p = df["p"].dropna()
bins = np.linspace(1, 1024, 33)  # 33 edges -> 32 bins

plt.figure()
plt.hist(p, bins=bins)
plt.title("Histogram of p ")
plt.xlabel("p")
plt.ylabel("count")
#plt.xlim(1, 1024)
plt.xticks([1, 256, 512, 768, 1024])
plt.margins(x=0.05)  


save_path = os.path.join(out_dir, "hist_p.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Saved histograms to: {out_dir}")