import os
import glob
import pandas as pd
import numpy as np

# # -------------------- LOAD ALL CSV FILES --------------------

# main_folder = r"C:\Users\pjsci\OneDrive\Documents\Thesis\Paper1\Extension\OnlineTaskScheduling.worktrees\origin-Onlineschedulingalgo_assorted\TASKS"

# all_files = glob.glob(os.path.join(main_folder, "n=*/", "*.csv"))

# print(f"\nTotal files found: {len(all_files)}")

# df_list = [pd.read_csv(file) for file in all_files]
# df = pd.concat(df_list, ignore_index=True)

# print(f"Total rows combined: {len(df):,}")


# # -------------------- POWER-OF-10 RANGE HISTOGRAM --------------------

# def print_power10_ranges(data, column_name):
#     print(f"\n=======================================")
#     print(f"Column: {column_name}")
#     print(f"=======================================")

#     x = data[column_name].dropna()
#     x = x[x > 0]

#     total = len(x)

#     print(f"Total {column_name} values: {total:,}\n")

#     log_min = int(np.floor(np.log10(x.min())))
#     log_max = int(np.ceil(np.log10(x.max())))

#     powers = np.arange(log_min, log_max)

#     for p in powers:
#         lower = 10.0 ** p
#         upper = 10.0 ** (p + 1)

#         count = np.sum((x >= lower) & (x < upper))
#         percent = (count / total) * 100

#         print(f"Range 10^{p}  to  10^{p+1}  -->  "
#               f"{count:,} records  |  {percent:.2f}% of total {column_name}")

#     print("\n")


# # -------------------- RUN FOR w, d, c --------------------

# for col in ["w", "d", "c"]:
#     print_power10_ranges(df, col)





# #++++++++++Assort all tasks==============================================
# #==========================================================================
# import os
# import glob
# import pandas as pd

# # -------------------- MAIN FOLDER --------------------

main_folder = r"C:\Thesis\Paper1\Extension_Fair_algo\EXT_Fair_algo\OnlineTaskScheduling\TASKS"

print("Main folder exists:", os.path.exists(main_folder))
print("Absolute path:", os.path.abspath(main_folder))

# -------------------- GET ALL CSV FILES --------------------

all_files = glob.glob(os.path.join(main_folder, "n=*/", "*.csv"))
print(f"Total files found: {len(all_files)}")

# -------------------- READ AND CONCAT --------------------

df_list = [pd.read_csv(file) for file in all_files]
df = pd.concat(df_list, ignore_index=True)

print(f"Total rows combined: {len(df):,}")

# -------------------- SAVE COMBINED CSV --------------------

output_path = os.path.join(main_folder, "assorted_tasks.csv")

df.to_csv(output_path, index=False)

# -------------------- VERIFY SAVE --------------------

if os.path.exists(output_path):
    print("\n✅ File successfully saved at:")
    print(output_path)
    print("File size (MB):", round(os.path.getsize(output_path)/1e6, 2))
else:
    print("\n❌ File was NOT saved.")