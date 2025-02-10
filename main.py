
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

if version == 0 :
    if model_num == 0:
        mu_values = list(map(float, np.arange(0.3, 0.51, 0.02)))
        paramter_values = list(map(float, np.arange(1, 1.51, 0.2)))
    elif model_num == 1:
        mu_values = list(map(float, np.arange(0.1, 0.31, 0.02)))
        paramter_values = list(map(float, np.arange(1, 2.01, 0.2)))
    elif model_num == 2:
        mu_values = list(map(float, np.arange(0.1, 0.51, 0.02)))
        paramter_values = list(map(float, np.arange(1, 1.51, 0.2)))
    elif model_num == 3:
        mu_values = list(map(float, np.arange(0.1, 0.51, 0.02)))
        paramter_values = list(map(float, np.arange(1, 1.51, 0.2)))

elif version == 1:
    if model_num == 0:
        mu_values = list(map(float, np.arange(0.3, 0.51, 0.02)))
        paramter_values = list(map(float, np.arange(1, 5.01, 0.2)))
    elif model_num == 1:
        mu_values = list(map(float, np.arange(0.1, 0.41, 0.02)))
        paramter_values = list(map(float, np.arange(2.5, 4.01, 0.2)))
    elif model_num == 2:
        mu_values = list(map(float, np.arange(0.1, 0.51, 0.02)))
        paramter_values = list(map(float, np.arange(2, 5.01, 0.2)))
    elif model_num == 3:
        mu_values = list(map(float, np.arange(0.1, 0.21, 0.02)))
        paramter_values = list(map(float, np.arange(2, 3.01, 0.2)))

elif version == 2:
    if model_num == 0:
        mu_values = list(map(float, np.arange(0.3, 0.51, 0.02)))
        paramter_values = list(map(float, np.arange(0, 1.01, 0.05)))
    elif model_num == 1:
        mu_values = list(map(float, np.arange(0.1, 0.31, 0.02)))
        paramter_values = list(map(float, np.arange(0, 0.21, 0.05)))
    elif model_num == 2:
        mu_values = list(map(float, np.arange(0.1, 0.51, 0.02)))
        paramter_values = list(map(float, np.arange(0, 0.11, 0.05)))
    elif model_num == 3:
        mu_values = list(map(float, np.arange(0.1, 0.21, 0.02)))
        paramter_values = list(map(float, np.arange(0, 0.21, 0.05)))

result_directory = folder + model_name 
os.makedirs(result_directory, exist_ok=True)  #checks and create dir if needed ,exist_ok=True will not raise an error if the directory already exists

def create_empty_csv(mu, par, directory, file_name):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as file: #open the file , w-write pemission
        pass

for mu in mu_values:
    for par in paramter_values:
        
        if version == 0:         #Creates a new file for each iteration
            file_name = f"mu_{mu:.2f}_beta_{par:.2f}.csv"
            alpha, beta, gamma = [None , par,None]
        elif version ==1 :
            file_name = f"mu_{mu:.2f}_alpha_{par:.2f}.csv"
            alpha, beta , gamma = [par, None , None]
        elif version == 2:
            file_name = f"mu_{mu:.2f}_gamma_{par:.2f}.csv"
            alpha , beta , gamma = [None , None , par]

        create_empty_csv(mu, par, result_directory, file_name)
        file_path = os.path.join(result_directory, file_name)
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['P', 'n' ,'Algorithm Time', 'Optimal Time', 'Makespan Ratio'])
            args_list = [( folder ,model_name, mu, alpha, beta, gamma, version,writer) ]
            with ThreadPoolExecutor() as executor: # multithreading implementation
                futures = [executor.submit(compute_and_save, *args) for args in args_list]
                for future in as_completed(futures):
                    pass  

            f.close()

