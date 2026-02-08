
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
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any

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
        P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.1
        P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.5
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
import sys
import itertools
from typing import Optional, Tuple, Dict, Any, List
try:
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
    SKLEARN_OK = True
except Exception:
    SKLEARN_OK = False

# Search controls (tune these)
N_INITIAL = 6               # random initial evaluations
MAX_EVALS = 40              # total evaluations budget
KAPPA = 1.0                 # exploration/exploitation for LCB
SAT_PATIENCE = 8            # stop if no global best improvement for this many steps
MIN_IMPROVEMENT = 0.0   

# =========================
# 1) USER INPUTS (CHANGE THESE ANYTIME)
# =========================



OUTPUT_DIR = "bo_results"
COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results.csv")
TERMINAL_LOG_TXT = os.path.join(OUTPUT_DIR, "terminal_log.txt")


# =========================
# 2) HELPERS
# =========================

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def frange_inclusive(vmin: float, vmax: float, step: float) -> List[float]:
    if step <= 0:
        raise ValueError("step must be > 0")
    n = int(round((vmax - vmin) / step))
    vals = [round(vmin + i * step, 10) for i in range(n + 1)]
    # ensure inclusive end if floating drift
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
    """Redirect stdout to both terminal and a file."""
    def __init__(self, logfile_path: str):
        self.logfile_path = logfile_path
        self.terminal = sys.stdout
        self.log = open(logfile_path, "w", buffering=1)  # line-buffered

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

def to_X(pairs: List[Tuple[float, float]]) -> np.ndarray:
    return np.array([[p1, p2] for (p1, p2) in pairs], dtype=float)

def fit_surrogate(X: np.ndarray, y: np.ndarray):
    """
    Gaussian Process surrogate (best for BO).
    Requires sklearn. If not installed, we raise with a clear message.
    """
    if not SKLEARN_OK:
        raise RuntimeError(
            "scikit-learn not available. Install it or switch surrogate to a simple model.\n"
            "pip install scikit-learn"
        )

    # Kernel: Constant * Matern + White noise
    kernel = ConstantKernel(1.0, (1e-3, 1e3)) * Matern(length_scale=[0.1, 0.1], nu=2.5) + WhiteKernel(1e-6)
    gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, n_restarts_optimizer=2, random_state=0)
    gp.fit(X, y)
    return gp

def propose_next(
    unevaluated: List[Tuple[float, float]],
    gp,
    global_best_pair: Tuple[float, float],
    idx1: Dict[float, int], idx2: Dict[float, int],
    kappa: float
) -> Tuple[float, float]:
    """
    Select next point among unevaluated by:
      1) minimize LCB = mu - kappa*sigma  (for minimization)
      2) tie-break: closest to global best (Manhattan grid distance)
    """
    Xcand = to_X(unevaluated)
    mu, sigma = gp.predict(Xcand, return_std=True)
    lcb = mu - kappa * sigma

    best_idx = None
    best_lcb = float("inf")
    best_dist = float("inf")

    for i, pair in enumerate(unevaluated):
        score = float(lcb[i])
        dist = manhattan_grid_distance(pair, global_best_pair, idx1, idx2)

        # primary: lowest LCB
        if score < best_lcb - 1e-12:
            best_lcb = score
            best_dist = dist
            best_idx = i
        # tie-break: closest to best
        elif abs(score - best_lcb) <= 1e-12 and dist < best_dist:
            best_dist = dist
            best_idx = i

    return unevaluated[best_idx]
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

    # Redirect terminal output to a file too
    tee = TeeStdout(TERMINAL_LOG_TXT)
    old_stdout = sys.stdout
    sys.stdout = tee

    try:
        p1_values = frange_inclusive(P1_MIN, P1_MAX, P1_STEP)
        p2_values = frange_inclusive(P2_MIN, P2_MAX, P2_STEP)
        all_pairs = list(itertools.product(p1_values, p2_values))
        random.shuffle(all_pairs)

        idx1 = build_index(p1_values)
        idx2 = build_index(p2_values)

        # Output CSV
        fields = ["eval_id", "P1", "P2", "value", "global_best_value", "global_best_P1", "global_best_P2"]
        write_csv_header_if_missing(COMBO_RESULTS_CSV, fields)

        evaluated = set()         # NEVER repeat any combo
        X_obs: List[Tuple[float, float]] = []
        y_obs: List[float] = []

        global_best_val = float("inf")
        global_best_pair: Optional[Tuple[float, float]] = None

        no_improve = 0
        eval_id = 0

        print("=== START Bayesian-like search (NO repeats) ===")
        print(f"Grid size: {len(all_pairs)} total combos")
        print(f"Initial random evals: {N_INITIAL}, Max evals: {MAX_EVALS}, kappa={KAPPA}\n")

        # ---- 1) INITIAL RANDOM PHASE ----
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

        # ---- 2) SURROGATE LOOP ----
        while eval_id < MAX_EVALS:
            if no_improve >= SAT_PATIENCE:
                print(f"\nStopping: no improvement for {SAT_PATIENCE} steps (saturation).")
                break

            # Fit surrogate
            X = to_X(X_obs)
            y = np.array(y_obs, dtype=float)
            gp = fit_surrogate(X, y)

            # Candidate pool (unseen)
            unevaluated = [pair for pair in all_pairs if pair not in evaluated]
            if not unevaluated:
                print("\nNo more unseen combinations left.")
                break

            # Propose next best (LCB + closest-to-best tie-break)
            next_pair = propose_next(
                unevaluated=unevaluated,
                gp=gp,
                global_best_pair=global_best_pair,
                idx1=idx1, idx2=idx2,
                kappa=KAPPA
            )

            # Evaluate proposed
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