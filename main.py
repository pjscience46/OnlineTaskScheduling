
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
mu_values = [0.2]
paramter_values = [3.5]

version = int(input("Enter algorithm version number[0-MAST, 1-MTSA, 2-MTPA] : "))
if version == 0:
    parameter = 'beta'
    folder = "Results_mast/"
elif version == 1:
    parameter = 'alpha'
    folder = "Results_mtsa/"
elif version == 2:
    parameter = 'gamma'
    folder = "Results_mtpa/"

model_num = int(input("Enter the Model Number [0-Roofline , 1-Amdahl, 2-Communication , 3-General]: "))
if model_num == 0:
    model_name = "Roofline"
elif model_num == 1:
    model_name = 'Amdahl'
elif model_num == 2:
    model_name = 'Communication'
elif model_num == 3:
    model_name = 'General'

result_directory = folder + model_name 
os.makedirs(result_directory, exist_ok=True)  #checks and create dir if needed ,exist_ok=True will not raise an error if the directory already exists

def create_empty_csv(mu, G, directory, file_name):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as file: #open the file , w-write pemission
        pass

def compute_and_save_wrapper(args):
    try:
        # Extracting version and parameters
        version = args[8]  
        alpha, beta, gamma = args[5], args[6], args[7]  
        
        # Choose the parameter based on version
        if version == 0:  # Use beta
            parameter_value = beta
        elif version == 1:  # Use alpha
            parameter_value = alpha
        elif version == 2:  # Use gamma
            parameter_value = gamma
        else:
            raise ValueError(f"Unsupported version: {version}")

        # Call the actual function
        compute_and_save(*args)
        print(f"Completed computing for mu={args[4]}, {parameter}={parameter_value}, P={args[9]}, n={args[10]}")
    except Exception as e:
        print(f"Error computing for mu={args[4]}, {parameter}={parameter_value}, P={args[9]}, n={args[10]}: {e}")


for mu in mu_values:
    for p in paramter_values:
        
        if version == 0:         #Creates a new file for each iteration
            file_name = f"mu_{mu:.2f}_beta_{p:.2f}.csv"
            alpha, beta, gamma = [None , p,None]
        elif version ==1 :
            file_name = f"mu_{mu:.2f}_alpha_{p:.2f}.csv"
            alpha, beta , gamma = [p, None , None]
        elif version == 2:
            file_name = f"mu_{mu:.2f}_gamma_{p:.2f}.csv"
            alpha , beta , gamma = [None , None , p]

        create_empty_csv(mu, p, result_directory, file_name)
        file_path = os.path.join(result_directory, file_name)

        # p_list = [128,256,512,1024,2048,4096,8192]
        # n_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        p_list = [1000]
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
            args_list = [('n', folder ,model_name, nb_iterations, mu, alpha, beta, gamma, version, i[0], i[1],writer)for i in all_combinations ]
            with ThreadPoolExecutor() as executor: # multithreading implementation
                futures = [executor.submit(compute_and_save_wrapper, args) for args in args_list]
                for future in as_completed(futures):
                    pass  

            f.close()

