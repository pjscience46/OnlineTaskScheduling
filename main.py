# main
import os
import time
from processors import *
from utils import *
from statistics import *
import matplotlib.pyplot as plt
import logging
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools
import random

nb_iterations = 10
mu_values = np.arange(0.70, 0.79, 0.05)
beta_values = np.arange(1, 5, 0.5)
#mu_values = [0.9]
#beta_values = [5]

def create_empty_csv(mu, B, directory, file_name):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as file:
        pass

def compute_and_save_wrapper(args):
    try:
        compute_and_save(*args)
        print(f"Completed computing for mu={args[3]}, B={args[4]}, P={args[6]}")
    except Exception as e:
        print(f"Error computing for mu={args[3]}, B={args[4]}, P={args[6]}: {e}")

start_time = time.process_time_ns()
result_directory = "Results_mast/n/Roofline"
os.makedirs(result_directory, exist_ok=True)
num = 0

for mu in mu_values:
    for B in beta_values:
        file_name = f"mu_{mu:.2f}_beta_{B:.2f}.csv"
        create_empty_csv(mu, B, result_directory, file_name)
        file_path = os.path.join(result_directory, file_name)

        p_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4100, 4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000]
        n_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        all_combinations = list(itertools.product(p_list, n_list))

        # Check if there are at least 100 unique combinations available
        if len(all_combinations) < 100:
            print(f"Only {len(all_combinations)} unique combinations are possible.")
        else:
            # Randomly sample 100 unique combinations
            random_combinations = random.sample(all_combinations, 101)
            
        version = 0

        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['P', 'n', 'Paper', 'Min Time', 'Time opt', 'mast'])

            # Prepare arguments for compute_and_save_wrapper
            # for i in random_combinations:
            #     proc = i[0]
            #     n_tasks = i[1]
            args_list = [('n', 'Results_mast/n/', nb_iterations, mu, B, version, i[0], i[1],writer)for i in random_combinations ]

            # Use ThreadPoolExecutor for multithreading
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(compute_and_save_wrapper, args) for args in args_list]
                for future in as_completed(futures):
                    pass  # you can handle completed tasks here if needed

            f.close()

        num += 1
        pc = (num / 300)
        eta = ((time.process_time_ns() - start_time) / 1e9) * ((1 - pc) / pc)
        print(f" {num}."
              f"[{pc * 100:.2f} %]"
              f" Roofline model ,"
              f" mu :{mu},"
              f" Beta :{B},"
              f" ETA: {int(eta)}s")

end_time = time.process_time_ns()
print(f"Finished computing in {(end_time - start_time) / (10**9):.3f}s")
