# use this file====
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.ticker import LogLocator
# import glob
# import os

# # Main TASKS folder
# main_folder = r"C:\Users\pjsci\OneDrive\Documents\Thesis\Paper1\Extension\OnlineTaskScheduling.worktrees\origin-Onlineschedulingalgo_assorted\TASKS"

# # Get all csv files inside all subfolders
# all_files = glob.glob(os.path.join(main_folder, "n=*/", "*.csv"))

# print(f"Total files found: {len(all_files)}")

# # Read and combine
# df_list = [pd.read_csv(file) for file in all_files]
# df = pd.concat(df_list, ignore_index=True)

# print(f"Total rows combined: {len(df)}")
# # ----------------- LOG histograms for w, d, c -----------------

# import numpy as np
# import matplotlib.pyplot as plt

# for col in ["w", "d", "c"]:
#     x = df[col].dropna()
#     x = x[x > 0]

#     plt.figure()

#     weights = np.ones_like(x) * 100.0 / len(x)
#     plt.hist(x, bins=30, weights=weights)

#     ax = plt.gca()
#     ax.set_xscale("log")
#     ax.set_xlim(x.min(), x.max())

#     # ---- FIXED TICKS ----
#     log_min = int(np.floor(np.log10(x.min())))
#     log_max = int(np.ceil(np.log10(x.max())))

#     powers = np.arange(log_min, log_max + 1)
#     ticks = 10.0 ** powers

#     ax.set_xticks(ticks)
#     ax.set_xticklabels(
#         [fr"$\log_{{10}}(10^{{{p}}})$" for p in powers]
#     )

#     plt.title(f"{col} (All n Combined)")
#     plt.xlabel(col)
#     plt.ylabel("Percent (%)")
#     plt.show()
    
# for col in ["w", "d", "c"]:
#     x = df[col].dropna()

#     plt.figure()

#     # Convert counts to percent
#     weights = np.ones_like(x) * 100.0 / len(x)

#     plt.hist(x, bins=30, weights=weights)

#     plt.title(f"{col} (Normal Scale)")
#     plt.xlabel(col)
#     plt.ylabel("Percent (%)")

#     plt.show()

#============================================================

# p = df["p"].dropna()
# bins = np.linspace(1, 1024, 33)  # 33 edges -> 32 bins

# plt.figure()
# plt.hist(p, bins=bins)
# plt.title("Histogram of p ")
# plt.xlabel("p")
# plt.ylabel("count")
# #plt.xlim(1, 1024)
# plt.xticks([1, 256, 512, 768, 1024])
# plt.margins(x=0.05)  
# plt.show()

#====================================================================
#hist percent
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------- LOAD DATA --------------------

import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------- LOAD DATA --------------------

main_folder = r"C:\Users\m779p635\OneDrive - University of Kansas\Extension_Scheduling\OnlineTaskScheduling\TASKS"
#all_files = glob.glob(os.path.join(main_folder, "n=*/", "*.csv"))
all_files = glob.glob(os.path.join(main_folder, "n=1000", "1.csv"))
df_list = [pd.read_csv(file) for file in all_files]
df = pd.concat(df_list, ignore_index=True)


# -------------------- HISTOGRAM WITH PERCENTAGE without extra sub-ranges --------------------

# def plot_power_histogram(data, column_name, power_edges):
    
#     x = data[column_name].dropna()
#     x = x[x > 0]

#     total = len(x)

#     # Convert powers to actual bin edges
#     bins = [10.0 ** p for p in power_edges]

#     plt.figure()

#     # weights → convert counts to percentage
#     weights = np.ones_like(x) * 100.0 / total

#     plt.hist(x, bins=bins, weights=weights)

#     # Log scale (important)
#     plt.xscale("log")

#     # X-axis ticks as 10^p
#     plt.xticks(bins, [f"$10^{{{p}}}$" for p in power_edges])

#     plt.xlabel(column_name)
#     plt.ylabel("Percentage (%)")
#     plt.title(f"Histogram of {column_name} (Power-of-10 Bins)")

#     plt.show()


# # w: 10^2 to 10^5
# plot_power_histogram(df, "w", [2, 3, 4, 5])

# # d: 10^-3 to 10^0
# plot_power_histogram(df, "d", [-3, -2, -1, -0.5])

# # c: 10^-6 to 10^-2
# plot_power_histogram(df, "c", [-6, -5, -4, -3, -2])


#=====================================
#===hist with percent(values between ranges)===============

def plot_power_histogram(data, column_name, power_edges, step=0.5):
    x = data[column_name].dropna()
    x = x[x > 0]

    total = len(x)

    # Create bins with intermediate values inside the given range
    min_power, max_power = min(power_edges), max(power_edges)
    # bins = np.arange(min_power, max_power + step, step)  # includes intermediate powers
    # bins = 10.0 ** bins  # convert to actual bin values
    n_bins = 32

    bins = np.logspace(
        np.log10(x.min()),
        np.log10(x.max()),
        n_bins
    )

    

    plt.figure()

    # weights → convert counts to percentage
    #weights = np.ones_like(x) * 100.0 / total
    weights = np.ones_like(x) / total

    #plt.hist(x, bins=bins, weights=weights)
    plt.hist(
    x,
    bins=bins,
    weights=weights,
    edgecolor="black",
    linewidth=1.2,
    rwidth=0.95
)

    # Log scale (important)
    plt.xscale("log")
    

    # X-axis ticks as 10^p
    ticks = np.arange(min_power, max_power + step, step)
    plt.xticks(10.0 ** ticks, [f"$10^{{{p}}}$" for p in ticks])

    if column_name == "w":
        plt.xlabel(r"$w$ (total parallelizable work)", fontsize=14)
    elif column_name == "d":
        plt.xlabel(r"$d^\prime$ (sequential fraction)", fontsize=14)
    elif column_name == "c":
        plt.xlabel(r"$c^\prime$ (communication overhead)", fontsize=14)
    
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.ylabel("Frequency", fontsize=14)
   # plt.title(f"Histogram of {column_name} ")

    plt.show()

# # Examples:

# w: 10^2 to 10^5 with 0.5 steps → 2,2.5,3,3.5,...,5
plot_power_histogram(df, "w", [2, 5], step=0.5)

# d: 10^-3 to 10^0 with 0.5 steps → -3, -2.5, -2, -1.5, -1, -0.5, 0
plot_power_histogram(df, "d", [-3, -0.5], step=0.5)

# c: 10^-6 to 10^-2 with 1 step → -6, -5, -4, -3, -2
plot_power_histogram(df, "c", [-6, -2], step=1)

p = df["p"].dropna()
p = p[p > 0]   # optional, only if you want positive values

total = len(p)

bins = np.linspace(1, 1024, 33)  # 33 edges -> 32 bins

plt.figure()

# Convert counts → percentage
#weights = np.ones_like(p) * 100.0 / total
weights = np.ones_like(p) / total


#plt.hist(p, bins=bins, weights=weights)
plt.hist(
    p,
    bins=bins,
    weights=weights,
    edgecolor="black",
    linewidth=1.2,
    rwidth=0.95
)

#plt.title("Histogram of p")
plt.xlabel(r'$\bar{p}(maximum degree of parallelism)$', fontsize=14)
plt.ylabel("Frequency", fontsize=14)

plt.xticks([1, 256, 512, 768, 1024], fontsize=14)
plt.yticks(fontsize=14)
plt.margins(x=0.05)

plt.show()


#=================Hist with count==================
#=========================================================
#==========================================================

# def plot_power_histogram_count(data, column_name, power_edges):
#     x = data[column_name].dropna()
#     x = x[x > 0]

#     bins = [10.0 ** p for p in power_edges]

#     plt.figure()
#     plt.hist(x, bins=bins)  # default counts
#     plt.xscale("log")
#     plt.xticks(bins, [f"$10^{{{p}}}$" for p in power_edges])
#     plt.xlabel(column_name)
#     plt.ylabel("Count")
#     plt.title(f"Histogram of {column_name} (Power-of-10 Bins)")
#     plt.show()


# # Example usage
# plot_power_histogram_count(df, "w", [2, 3, 4, 5])
# plot_power_histogram_count(df, "d", [-3, -2, -1, -0.5])
# plot_power_histogram_count(df, "c", [-6, -5, -4, -3, -2])


#================ Hist with count (values b/w ranges) =============
#==================================================================

# import numpy as np
# import matplotlib.pyplot as plt

# def plot_power_histogram_count(data, column_name, power_edges, step=0.5):
#     """
#     Plots a histogram of a column with bins in powers-of-10, including intermediate powers.
#     Y-axis shows counts (not percentage).
    
#     Parameters:
#     - data: pandas DataFrame
#     - column_name: str, column to plot
#     - power_edges: list or tuple, [min_power, max_power]
#     - step: float, step between powers for intermediate bins
#     """
#     x = data[column_name].dropna()
#     x = x[x > 0]  # only positive values for log-scale

#     # Create bins including intermediate powers
#     min_power, max_power = min(power_edges), max(power_edges)
#     bins = np.arange(min_power, max_power + step, step)  # intermediate powers
#     bins = 10.0 ** bins  # convert powers to actual values

#     plt.figure()
#     plt.hist(x, bins=bins)  # counts on y-axis
#     plt.xscale("log")

#     # X-axis ticks as 10^p
#     ticks = np.arange(min_power, max_power + step, step)
#     plt.xticks(10.0 ** ticks, [f"$10^{{{p}}}$" for p in ticks])

#     plt.xlabel(column_name)
#     plt.ylabel("Count")
#     plt.title(f"Histogram of {column_name} (Power-of-10 Bins)")

#     plt.show()


#     # w: 10^2 to 10^5 with 0.5 steps → 2, 2.5, 3, 3.5, ..., 5
# plot_power_histogram_count(df, "w", [2, 5], step=0.5)

# # d: 10^-3 to 10^0 with 0.5 steps → -3, -2.5, -2, -1.5, -1, -0.5, 0
# plot_power_histogram_count(df, "d", [-3, 0], step=0.5)

# # c: 10^-6 to 10^-2 with 1 step → -6, -5, -4, -3, -2
# plot_power_histogram_count(df, "c", [-6, -2], step=1)