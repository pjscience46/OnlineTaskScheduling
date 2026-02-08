
# I want this one closest to current best Also the program should randomly take few 
# combinations to execute at first, then it should develop a surrogate model based on
# the output of the first few combinations. now based on surrogate model it needs to identify the 
# next best cmbination to execute. Again once next best combination executes, the surrogate model needs to be
# updated util it reaches saturation. this isth idea, in the wholeprocess no cobination should be repeated and the
# whole exeution on the terminal
# needs to be saved in a text file.global valule needs to be maintained at each time.

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
        # mu_values = list(map(float, np.arange(0.3, 0.51, 0.02)))
        # paramter_values = list(map(float, np.arange(1, 1.51, 0.2)))
        P1_MIN, P1_MAX, P1_STEP = 0.3, 0.5, 0.02
        P2_MIN, P2_MAX, P2_STEP = 1.0, 1.5, 0.2
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

# for mu in mu_values:
#     for par in paramter_values:
        
#         if version == 0:         #Creates a new file for each iteration
#             file_name = f"mu_{mu:.2f}_beta_{par:.2f}.csv"
#             alpha, beta, gamma = [None , par,None]
#         elif version ==1 :
#             file_name = f"mu_{mu:.2f}_alpha_{par:.2f}.csv"
#             alpha, beta , gamma = [par, None , None]
#         elif version == 2:
#             file_name = f"mu_{mu:.2f}_gamma_{par:.2f}.csv"
#             alpha , beta , gamma = [None , None , par]

#         create_empty_csv(mu, par, result_directory, file_name)
#         file_path = os.path.join(result_directory, file_name)
#         with open(file_path, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['P', 'n' ,'Algorithm Time', 'Optimal Time', 'Makespan Ratio'])
#             args_list = [( folder ,model_name, mu, alpha, beta, gamma, version,writer) ]
#             with ThreadPoolExecutor() as executor: # multithreading implementation
#                 futures = [executor.submit(compute_and_save, *args) for args in args_list]
#                 for future in as_completed(futures):
#                     pass  

#             f.close()

#_________________
import os
import csv
import itertools
from typing import Optional, Tuple, Dict, Any, List


# Search controls (tune these)
MAX_EVALS = 30          # evaluate at most this many combinations (NOT all)
PATIENCE = 8            # stop after this many steps with no improvement
RANDOM_RESTARTS = 1  

# =========================
# 1) USER INPUTS (CHANGE THESE ANYTIME)
# =========================



OUTPUT_DIR = "results"
COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results.csv")
FINAL_MIN_TXT = os.path.join(OUTPUT_DIR, "final_minimum.txt")


# =========================
# 2) HELPERS
# =========================

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def frange_inclusive(vmin: float, vmax: float, step: float) -> List[float]:
    """Inclusive float range avoiding drift."""
    if step <= 0:
        raise ValueError("step must be > 0")
    n = int(round((vmax - vmin) / step))
    vals = [round(vmin + i * step, 10) for i in range(n + 1)]
    if abs(vals[-1] - vmax) > 1e-9:
        vals.append(round(vmax, 10))
    vals = [v for v in vals if v <= vmax + 1e-9]
    return vals

def write_csv_header_if_missing(path: str, fieldnames: List[str]) -> None:
    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=fieldnames).writeheader()

def append_csv_row(path: str, fieldnames: List[str], row: Dict[str, Any]) -> None:
    with open(path, "a", newline="") as f:
        csv.DictWriter(f, fieldnames=fieldnames).writerow(row)

def frange_inclusive(vmin: float, vmax: float, step: float) -> List[float]:
    if step <= 0:
        raise ValueError("step must be > 0")
    n = int(round((vmax - vmin) / step))
    vals = [round(vmin + i * step, 10) for i in range(n + 1)]
    if abs(vals[-1] - vmax) > 1e-9:
        vals.append(round(vmax, 10))
    return [v for v in vals if v <= vmax + 1e-9]

def build_index(values: List[float]) -> Dict[float, int]:
    return {v: i for i, v in enumerate(values)}

def get_neighbors(p1: float, p2: float,
                  p1_values: List[float], p2_values: List[float],
                  idx1: Dict[float, int], idx2: Dict[float, int]) -> List[Tuple[float, float]]:
    """4-neighborhood on the grid (up/down/left/right)."""
    i = idx1[p1]
    j = idx2[p2]
    neigh = []
    if i - 1 >= 0: neigh.append((p1_values[i - 1], p2))
    if i + 1 < len(p1_values): neigh.append((p1_values[i + 1], p2))
    if j - 1 >= 0: neigh.append((p1, p2_values[j - 1]))
    if j + 1 < len(p2_values): neigh.append((p1, p2_values[j + 1]))
    return neigh
# =========================
# 3) YOU PROVIDE THIS
# =========================

def evaluate_one_combination_return_value(p1: float, p2: float) -> float:
    mu = p1
    par = p2
    if version == 0:         #Creates a new file for each iteration
            file_name = f"mu_{mu:.2f}_beta_{par:.2f}.csv"
            alpha, beta, gamma = [None , par,None]
    elif version ==1 :
            file_name = f"mu_{mu:.2f}_alpha_{par:.2f}.csv"
            alpha, beta , gamma = [par, None , None]
    elif version == 2:
            file_name = f"mu_{mu:.2f}_gamma_{par:.2f}.csv"
            alpha , beta , gamma = [None , None , par]
    combo_max_value = float("-inf")
    create_empty_csv(mu, par, result_directory, file_name)
    file_path = os.path.join(result_directory, file_name)
    with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['P', 'n' ,'Algorithm Time', 'Optimal Time', 'Makespan Ratio'])
            args_list = [( folder ,model_name, mu, alpha, beta, gamma, version,writer) ]
            with ThreadPoolExecutor() as executor: # multithreading implementation
                futures = [executor.submit(compute_and_save, *args) for args in args_list]
                for future in as_completed(futures):
                    max_value = future.result()   # <-- this is returned by compute_and_save
                    if max_value > combo_max_value:
                        combo_max_value = max_value
            f.close()
    print(combo_max_value)
    return combo_max_value  
    
            
    
    
    # -----------------------------
    # TODO: YOUR CODE GOES HERE
    # -----------------------------
    raise NotImplementedError


# =========================
# 4) MAIN: FIND MINIMUM AMONG COMBINATIONS
# =========================

def main():
    ensure_dir(OUTPUT_DIR)

    # Build grid
    p1_values = frange_inclusive(P1_MIN, P1_MAX, P1_STEP)  # mu
    p2_values = frange_inclusive(P2_MIN, P2_MAX, P2_STEP)  # par

    idx1 = build_index(p1_values)
    idx2 = build_index(p2_values)

    fields = ["eval_id", "restart_id", "P1", "P2", "value"]
    write_csv_header_if_missing(COMBO_RESULTS_CSV, fields)

    global_best_val = float("inf")   # we want MIN among evaluated combos
    global_best_pair: Optional[Tuple[float, float]] = None

    eval_id = 0

    for restart_id in range(1, RANDOM_RESTARTS + 1):
        # pick a random start (or force a specific start)
        current = (random.choice(p1_values), random.choice(p2_values))

        # Track evaluated points to avoid repeating
        visited = set()
        no_improve = 0

        # Evaluate start
        p1, p2 = current
        value = evaluate_one_combination_return_value(p1, p2)
        eval_id += 1
        visited.add(current)

        append_csv_row(COMBO_RESULTS_CSV, fields, {
            "eval_id": eval_id, "restart_id": restart_id, "P1": p1, "P2": p2, "value": value
        })

        # Update global best
        if value < global_best_val:
            global_best_val = value
            global_best_pair = current

        print(f"[restart {restart_id}] start at {current} -> value={value}, global_best={global_best_val}@{global_best_pair}")

        # Local search loop
        while eval_id < MAX_EVALS:
            p1, p2 = current
            neighbors = get_neighbors(p1, p2, p1_values, p2_values, idx1, idx2)

            # Evaluate only unseen neighbors
            candidates = [nb for nb in neighbors if nb not in visited]
            if not candidates:
                # stuck (all neighbors already tried) -> stop this restart
                break

            # Find best neighbor by evaluating them
            best_nb = None
            best_nb_val = float("inf")

            for nb in candidates:
                if eval_id >= MAX_EVALS:
                    break
                nb1, nb2 = nb

                nb_val = evaluate_one_combination_return_value(nb1, nb2)
                eval_id += 1
                visited.add(nb)

                append_csv_row(COMBO_RESULTS_CSV, fields, {
                    "eval_id": eval_id, "restart_id": restart_id, "P1": nb1, "P2": nb2, "value": nb_val
                })

                if nb_val < best_nb_val:
                    best_nb_val = nb_val
                    best_nb = nb

                if nb_val < global_best_val:
                    global_best_val = nb_val
                    global_best_pair = nb

                print(f"  tried {nb} -> {nb_val} | global_best={global_best_val}@{global_best_pair}")

            # Move decision: go to improving neighbor if any
            current_val = value
            if best_nb is not None and best_nb_val < current_val:
                current = best_nb
                value = best_nb_val
                no_improve = 0
                print(f"  move to {current} (improved to {value})")
            else:
                no_improve += 1
                print(f"  no improvement step {no_improve}/{PATIENCE}")
                if no_improve >= PATIENCE:
                    break

    # Write final
    with open(FINAL_MIN_TXT, "w") as f:
        f.write(f"Minimum value among evaluated combinations: {global_best_val}\n")
        f.write(f"Best (P1,P2): {global_best_pair}\n")
        f.write(f"Total evaluated combinations: {eval_id}\n")

    print("\n=== FINAL (SEARCH, NOT ALL COMBOS) ===")
    print(f"Evaluated combos: {eval_id} (max allowed {MAX_EVALS})")
    print(f"Best minimum value = {global_best_val}")
    print(f"Best (P1,P2) = {global_best_pair}")
    print(f"Files written: {COMBO_RESULTS_CSV}, {FINAL_MIN_TXT}")


if __name__ == "__main__":
    main()