import os
import random
import pandas as pd

input_root = r"C:\Thesis\Paper1\Extension_Fair_algo\EXT_Fair_algo\OnlineTaskScheduling\TASKS_old"
output_root = r"C:\Thesis\Paper1\Extension_Fair_algo\EXT_Fair_algo\OnlineTaskScheduling\TASKS"

random.seed(123)

for root, dirs, files in os.walk(input_root):
    # Find relative path from TASKS_old
    relative_path = os.path.relpath(root, input_root)
    output_dir = os.path.join(output_root, relative_path)

    # Create matching output folder
    os.makedirs(output_dir, exist_ok=True)

    for file in files:
        if file.lower().endswith(".csv"):
            input_file = os.path.join(root, file)
            output_file = os.path.join(output_dir, file)

            df = pd.read_csv(input_file)
            df["speedup_model"] = [random.randint(0, 3) for _ in range(len(df))]
            df.to_csv(output_file, index=False)

            print(f"Saved: {output_file}")

print("Done.")