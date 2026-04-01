import os
import sys
import time

# Ensure the project root (where `processors.py` lives) is on `sys.path`.
# When this file is executed from a nested folder, prepend the first
# ancestor that contains `processors.py` so imports like `from processors import *`
# work reliably.
p = os.path.abspath(os.path.dirname(__file__))
for _ in range(8):
    if os.path.exists(os.path.join(p, "processors.py")):
        if p not in sys.path:
            sys.path.insert(0, p)
        break
    p = os.path.abspath(os.path.join(p, ".."))

from processors import *
from utils import *
from statistics import *
import matplotlib.pyplot as plt
import logging
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools
import os
import csv
import sys
import itertools
from typing import Optional, Tuple, Dict, Any, List
import random as pyrandom
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any




version = int(input("Enter algorithm version number[0-MAST, 1-MTSA, 2-MTPA] : "))
if version == 0:
    parameter = 'beta'
    folder = "FCFS/BO_MAST/Results_mast/"     #change
    sub_folder = "BO_MAST" #change
elif version == 1:
    parameter = 'alpha'
    folder = "FCFS/BO_MTSA/Results_mtsa/"
    sub_folder = "BO_MTSA"
elif version == 2:
    parameter = 'gamma'
    folder = "FCFS/BO_MTPA/Results_mtpa/"
    sub_folder = "BO_MTPA"

model_num = int(input("Enter the Model Number [0-Roofline , 1-Amdahl, 2-Communication , 3-General]: "))
if model_num == 0:
    model_name = "Roofline"
elif model_num == 1:
    model_name = 'Amdahl'
elif model_num == 2:
    model_name = 'Communication'
elif model_num == 3:
    model_name = 'General'

priority_num = int(input("Enter the Priority Number [0-FCFS, 1-Allocation, 2-Length, 3-Area]: "))

if priority_num == 0:
    priority_name = "FCFS"
elif priority_num == 1:
    priority_name = "Allocation"
elif priority_num == 2:
    priority_name = "Length"
elif priority_num == 3:
    priority_name = "Area"
else:
    raise ValueError("Invalid priority number")

if version == 0:
    if model_num == 0:  
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2
    elif model_num == 1:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2
    elif model_num == 2:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2
    elif model_num == 3:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2

elif version == 1:
    if model_num == 0:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2
    elif model_num == 1:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2
    elif model_num == 2:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2
    elif model_num == 3:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2

elif version == 2:
    if model_num == 0:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 0.0, 1.0, 0.05
    elif model_num == 1:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 0.0, 1.0, 0.05
    elif model_num == 2:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 0.0, 1.0, 0.05
    elif model_num == 3:
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
        P2_MIN, P2_MAX, P2_STEP = 0.0, 1.0, 0.05

result_directory = folder + model_name
os.makedirs(result_directory, exist_ok=True)

def create_empty_csv(mu, par, directory, file_name):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as file:
        pass

# -------------------------------
# BO / Search settings
# -------------------------------
try:
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
    SKLEARN_OK = True
except Exception:
    SKLEARN_OK = False

N_INITIAL = 20
MAX_EVALS = 100
KAPPA = 1.0
SAT_PATIENCE = 10
MIN_IMPROVEMENT = 0.0 # Minimum improvement to reset saturation counter (set to 0 for any improvement)

main_folder = priority_name #change
          #change

# Full path
OUTPUT_DIR = os.path.join(main_folder, sub_folder)



if model_num == 1:
    TERMINAL_LOG_TXT = os.path.join(OUTPUT_DIR, "TERMINAL_LOG_Amdahl_TXT.txt")
    COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results_Amdahl.csv")
elif model_num == 2:
    TERMINAL_LOG_TXT = os.path.join(OUTPUT_DIR, "TERMINAL_LOG_Communication_TXT.txt")
    COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results_comm.csv")
elif model_num == 0:
    TERMINAL_LOG_TXT = os.path.join(OUTPUT_DIR, "TERMINAL_LOG_Roofline_TXT.txt")
    COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results_Roofline.csv")
else:
    TERMINAL_LOG_TXT = os.path.join(OUTPUT_DIR, "TERMINAL_LOG_General_TXT.txt")
    COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results_General.csv")

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def frange_inclusive(vmin: float, vmax: float, step: float) -> List[float]:
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

class TeeStdout:
    def __init__(self, logfile_path: str):
        self.logfile_path = logfile_path
        self.terminal = sys.stdout
        self.log = open(logfile_path, "w", buffering=1)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def close(self):
        self.log.close()

def build_index(values: List[float]) -> Dict[float, int]:
    return {v: i for i, v in enumerate(values)}

def manhattan_grid_distance(a: Tuple[float, float], b: Tuple[float, float],
                            idx1: Dict[float, int], idx2: Dict[float, int]) -> int:
    return abs(idx1[a[0]] - idx1[b[0]]) + abs(idx2[a[1]] - idx2[b[1]])
#If two candidates look equally good,choose the one closer to current best on grid.


def to_X(pairs: List[Tuple[float, float]]) -> np.ndarray:
    return np.array([[p1, p2] for (p1, p2) in pairs], dtype=float)

def fit_surrogate(X: np.ndarray, y: np.ndarray):
    if not SKLEARN_OK:
        raise RuntimeError("scikit-learn not available. Install: pip install scikit-learn")

    kernel = ConstantKernel(1.0, (1e-3, 1e3)) * Matern(length_scale=[0.1, 0.1], nu=2.5) + WhiteKernel(1e-6)
    gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, n_restarts_optimizer=2, random_state=0)
    #GaussianProcessRegressor is a powerful surrogate model for Bayesian Optimization, providing both predictions and uncertainty estimates. 
    # The chosen kernel combines a Matern kernel (for smoothness) with a WhiteKernel (for noise). Normalizing the target values can help with optimization performance. Multiple restarts of the optimizer can help find better hyperparameters for the kernel.
    gp.fit(X, y)
    return gp

def propose_next(
    unevaluated: List[Tuple[float, float]],
    gp,
    global_best_pair: Tuple[float, float],
    idx1: Dict[float, int], idx2: Dict[float, int],
    kappa: float
) -> Tuple[float, float]:
    Xcand = to_X(unevaluated)
    mu, sigma = gp.predict(Xcand, return_std=True)
    #mu is the predicted ratio value and sigma is uncertainty at those points. These are used to compute the acquisition function, which guides the search for the next evaluation point.
    lcb = mu - kappa * sigma 
    # Lower Confidence Bound acquisition function: balances exploration (high sigma) and exploitation (low mu). The kappa parameter controls this balance. A higher kappa encourages exploring uncertain regions, while a lower kappa focuses on areas predicted to have low values.

    best_idx = None
    best_lcb = float("inf")
    best_dist = float("inf")

    for i, pair in enumerate(unevaluated):
        score = float(lcb[i])
        dist = manhattan_grid_distance(pair, global_best_pair, idx1, idx2)

        if score < best_lcb - 1e-12:
            best_lcb = score
            best_dist = dist
            best_idx = i
        elif abs(score - best_lcb) <= 1e-12 and dist < best_dist:
            best_dist = dist
            best_idx = i

    return unevaluated[best_idx]

def evaluate_one_combination_return_value(p1: float, p2: float) -> float:
    mu = p1
    par = p2

    if version == 0:
        file_name = f"mu_{mu:.2f}_beta_{par:.2f}.csv"
        alpha, beta, gamma = [None, par, None]
    elif version == 1:
        file_name = f"mu_{mu:.2f}_alpha_{par:.2f}.csv"
        alpha, beta, gamma = [par, None, None]
    else:
        file_name = f"mu_{mu:.2f}_gamma_{par:.2f}.csv"
        alpha, beta, gamma = [None, None, par]

    combo_max_value = float("-inf")

    create_empty_csv(mu, par, result_directory, file_name)
    file_path = os.path.join(result_directory, file_name)

    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['P', 'n', 'Algorithm Time', 'Optimal Time', 'Makespan Ratio'])

        args_list = [(folder, model_name, mu, alpha, beta, gamma, version, writer, priority_num)]

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(compute_and_save, *args) for args in args_list]
            for future in as_completed(futures):
                max_value = future.result()
                if max_value > combo_max_value:
                    combo_max_value = max_value

    print(combo_max_value)
    return combo_max_value

def main():
    ensure_dir(OUTPUT_DIR)

    tee = TeeStdout(TERMINAL_LOG_TXT) # Teestandard output to both terminal and file
    old_stdout = sys.stdout
    sys.stdout = tee

    try:
        p1_values = frange_inclusive(P1_MIN, P1_MAX, P1_STEP)
        p2_values = frange_inclusive(P2_MIN, P2_MAX, P2_STEP)

        all_pairs = list(itertools.product(p1_values, p2_values))

       
        pyrandom.shuffle(all_pairs) # Randomize order to avoid bias in initial evaluations

        idx1 = build_index(p1_values) 
        idx2 = build_index(p2_values)

        fields = ["eval_id", "P1", "P2", "value", "global_best_value", "global_best_P1", "global_best_P2"]
        write_csv_header_if_missing(COMBO_RESULTS_CSV, fields)

        evaluated = set()
        X_obs: List[Tuple[float, float]] = [] # List of evaluated (P1, P2) pairs
        y_obs: List[float] = [] # Corresponding list of observed values (makespan ratios)

        global_best_val = float("inf")
        global_best_pair: Optional[Tuple[float, float]] = None

        no_improve = 0 # Counter for consecutive evaluations without improvement (for saturation stopping)
        eval_id = 0

        print("=== START Bayesian-like search (NO repeats) ===")
        print(f"Grid size: {len(all_pairs)} total combos")
        print(f"Initial random evals: {N_INITIAL}, Max evals: {MAX_EVALS}, kappa={KAPPA}\n") 
        #kappa is the exploration-exploitation parameter for the acquisition function
        # Larger kappa encourages trying uncertain/unexplored parameter regions, while smaller kappa focuses on
        # the currently best-predicted values (more greedy search).


        # Initial random evaluations
        initial = []
        for pair in all_pairs:
            if len(initial) >= N_INITIAL:
                break
            if pair not in evaluated:
                initial.append(pair)

        for pair in initial:
            p1, p2 = pair
            val = evaluate_one_combination_return_value(p1, p2)

            eval_id += 1
            evaluated.add(pair)
            X_obs.append(pair)
            y_obs.append(val)

            if val + MIN_IMPROVEMENT < global_best_val:
                global_best_val = val
                global_best_pair = pair
                no_improve = 0
            else:
                no_improve += 1

            append_csv_row(COMBO_RESULTS_CSV, fields, {
                "eval_id": eval_id, "P1": p1, "P2": p2, "value": val,
                "global_best_value": global_best_val,
                "global_best_P1": global_best_pair[0] if global_best_pair else None,
                "global_best_P2": global_best_pair[1] if global_best_pair else None,
            })

            print(f"[init {eval_id}/{N_INITIAL}] {pair} -> {val:.6g} | best={global_best_val:.6g} @ {global_best_pair}")

            if eval_id >= MAX_EVALS:
                break

        if global_best_pair is None:
            print("No evaluations were run. Exiting.")
            return
        no_improve = 0
        # Surrogate loop
        while eval_id < MAX_EVALS:
            if no_improve >= SAT_PATIENCE:
                print(f"\nStopping: no improvement for {SAT_PATIENCE} steps (saturation).")
                break

            X = to_X(X_obs)
            y = np.array(y_obs, dtype=float)
            gp = fit_surrogate(X, y)

            unevaluated = [pair for pair in all_pairs if pair not in evaluated]
            if not unevaluated:
                print("\nNo more unseen combinations left.")
                break

            next_pair = propose_next(
                unevaluated=unevaluated,
                gp=gp,
                global_best_pair=global_best_pair,
                idx1=idx1, idx2=idx2,
                kappa=KAPPA
            )

            p1, p2 = next_pair
            val = evaluate_one_combination_return_value(p1, p2)

            eval_id += 1
            evaluated.add(next_pair)
            X_obs.append(next_pair)
            y_obs.append(val)

            improved = False
            if val + MIN_IMPROVEMENT < global_best_val:
                global_best_val = val
                global_best_pair = next_pair
                no_improve = 0
                improved = True
            else:
                no_improve += 1

            append_csv_row(COMBO_RESULTS_CSV, fields, {
                "eval_id": eval_id, "P1": p1, "P2": p2, "value": val,
                "global_best_value": global_best_val,
                "global_best_P1": global_best_pair[0],
                "global_best_P2": global_best_pair[1],
            })

            print(f"\n[step {eval_id}] proposed={next_pair} -> {val:.6g}")
            print(f"         best={global_best_val:.6g} @ {global_best_pair} | improved={improved} | no_improve={no_improve}/{SAT_PATIENCE}")

        print("\n=== FINAL ===")
        print(f"Evaluations run: {eval_id}/{MAX_EVALS}")
        print(f"Best value: {global_best_val}")
        print(f"Best (P1,P2): {global_best_pair}")
        print(f"Saved CSV: {COMBO_RESULTS_CSV}")
        print(f"Saved terminal log: {TERMINAL_LOG_TXT}")

    finally:
        sys.stdout = old_stdout
        tee.close()

if __name__ == "__main__":
    main()
