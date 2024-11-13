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

nb_iterations = 1
# mu_values = np.arange(0.6, 0.91, 0.1)
# Gama_values = np.arange(0, 1.05, 0.1)
mu_values = [0.3]
Gama_values = [1.5]
version = int(input("Enter algorithm version number : "))
if version == 0:
    parameter = 'Beta'
elif version == 1:
    parameter = 'Alpha'
elif version == 2:
    parameter = 'Gama'
def create_empty_csv(mu, G, directory, file_name):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as file:
        pass

def compute_and_save_wrapper(args):
    try:
        compute_and_save(*args)
        print(f"Completed computing for mu={args[4]}, {parameter} ={args[5]}, P={args[7]} , n={args[8]}")
    except Exception as e:
        print(f"Error computing for mu={args[4]}, {parameter}={args[5]}, P={args[7]},n={args[8]}: {e}")

start_time = time.process_time_ns()

model_name = input("Enter the Model Name: ")
if version == 0:
    folder = "Results_mast/n/"
elif version == 1:
    folder = "Results_mtsa/n/"
elif version == 2:
    folder = "Results_mtpa/n/"
result_directory = folder + model_name 
os.makedirs(result_directory, exist_ok=True)

num = 0

for mu in mu_values:
    for G in Gama_values:
        
        if version == 0:
            file_name = f"mu_{mu:.2f}_Beta_{G:.2f}.csv"
        elif version ==1 :
            file_name = f"mu_{mu:.2f}_Alpha_{G:.2f}.csv"
        elif version == 2:
            file_name = f"mu_{mu:.2f}_Gama_{G:.2f}.csv"

        create_empty_csv(mu, G, result_directory, file_name)
        file_path = os.path.join(result_directory, file_name)

        # p_list = [ 500,1000,1500,2000,1002500,3000,3500,4000,4500,5000]
        # n_list = [, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        p_list = [500]
        n_list = [100]
        all_combinations = list(itertools.product(p_list, n_list))

        # # Check if there are at least 100 unique combinations available
        # if len(all_combinations) < 1:
        #     print(f"Only {len(all_combinations)} unique combinations are possible.")
        # else:
        #     # Randomly sample 100 unique combinations
        #     random_combinations = random.sample(all_combinations, 1)
            
        

        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['P', 'n', 'Paper', 'Min Time', 'Time opt', 'mast'])
            args_list = [('n', folder ,model_name, nb_iterations, mu, G, version, i[0], i[1],writer)for i in all_combinations ]
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(compute_and_save_wrapper, args) for args in args_list]
                for future in as_completed(futures):
                    pass  # you can handle completed tasks here if needed

            f.close()

end_time = time.process_time_ns()
print(f"Finished computing in {(end_time - start_time) / (10**9):.3f}s")