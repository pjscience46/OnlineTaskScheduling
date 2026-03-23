import os
import time
import csv
import sys
import itertools
import logging
import random as pyrandom
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Tuple, Dict, Any, List

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from processors import *
from utils import *
from statistics import *

# -------------------------------
# Inputs
# -------------------------------
version = int(input("Enter algorithm version number [0-MAST, 1-MTSA, 2-MTPA, 3-Fair] : "))
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

# -------------------------------
# Folder / parameter setup
# -------------------------------
if version == 0:
    parameter = "beta"
    folder = f"BO_MAST/{priority_name}/Results/"
elif version == 1:
    parameter = "alpha"
    folder = f"BO_MTSA/{priority_name}/Results/"
elif version == 2:
    parameter = "gamma"
    folder = f"BO_MTPA/{priority_name}/Results/"
elif version == 3:
    parameter = None
    folder = f"BO_Fair/{priority_name}/Results/"
else:
    raise ValueError("Invalid version")

# -------------------------------
# Parameter ranges
# -------------------------------
if version == 0:   # MAST
    P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
    P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2

elif version == 1: # MTSA
    P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
    P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.2

elif version == 2: # MTPA
    P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02
    P2_MIN, P2_MAX, P2_STEP = 0.0, 1.0, 0.05

elif version == 3: # Fair
    P1_MIN, P1_MAX, P1_STEP = 0.1, 0.90, 0.02

# -------------------------------
# Directories / files
# -------------------------------
result_directory = folder
os.makedirs(result_directory, exist_ok=True)

# BO / Search settings
try:
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
    SKLEARN_OK = True
except Exception:
    SKLEARN_OK = False

N_INITIAL = 5 #change
MAX_EVALS = 100
KAPPA = 1.0
SAT_PATIENCE = 10
MIN_IMPROVEMENT = 0.0

OUTPUT_DIR = folder

if priority_num == 0:
    TERMINAL_LOG_TXT = os.path.join(OUTPUT_DIR, "TERMINAL_LOG_FCFS_TXT.txt")
    COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results_FCFS.csv")
elif priority_num == 1:
    TERMINAL_LOG_TXT = os.path.join(OUTPUT_DIR, "TERMINAL_LOG_Allocation_TXT.txt")
    COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results_Alloc.csv")
elif priority_num == 2:
    TERMINAL_LOG_TXT = os.path.join(OUTPUT_DIR, "TERMINAL_LOG_Length_TXT.txt")
    COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results_Length.csv")
else:
    TERMINAL_LOG_TXT = os.path.join(OUTPUT_DIR, "TERMINAL_LOG_Area_TXT.txt")
    COMBO_RESULTS_CSV = os.path.join(OUTPUT_DIR, "combo_results_Area.csv")

# -------------------------------
# Utility functions
# -------------------------------
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

def create_empty_csv(mu, par, directory, file_name):
    file_path = os.path.join(directory, file_name)
    with open(file_path, "w") as file:
        pass

def build_index(values: List[float]) -> Dict[float, int]:
    return {v: i for i, v in enumerate(values)}

def manhattan_grid_distance(
    a: Tuple[float, float],
    b: Tuple[float, float],
    idx1: Dict[float, int],
    idx2: Dict[float, int]
) -> int:
    return abs(idx1[a[0]] - idx1[b[0]]) + abs(idx2[a[1]] - idx2[b[1]])

def to_X_2d(pairs: List[Tuple[float, float]]) -> np.ndarray:
    return np.array([[p1, p2] for (p1, p2) in pairs], dtype=float)

def to_X_1d(points: List[float]) -> np.ndarray:
    return np.array([[p1] for p1 in points], dtype=float)

def fit_surrogate(X: np.ndarray, y: np.ndarray):
    if not SKLEARN_OK:
        raise RuntimeError("scikit-learn not available. Install: pip install scikit-learn")

    n_features = X.shape[1]
    kernel = (
        ConstantKernel(1.0, (1e-3, 1e3))
        * Matern(length_scale=[0.1] * n_features, nu=2.5)
        + WhiteKernel(1e-6)
    )

    gp = GaussianProcessRegressor(
        kernel=kernel,
        normalize_y=True,
        n_restarts_optimizer=2,
        random_state=0
    )
    gp.fit(X, y)
    return gp

def propose_next_2d(
    unevaluated: List[Tuple[float, float]],
    gp,
    global_best_pair: Tuple[float, float],
    idx1: Dict[float, int],
    idx2: Dict[float, int],
    kappa: float
) -> Tuple[float, float]:
    Xcand = to_X_2d(unevaluated)
    mu, sigma = gp.predict(Xcand, return_std=True)
    lcb = mu - kappa * sigma

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

def propose_next_1d(
    unevaluated: List[float],
    gp,
    global_best_p1: float,
    idx1: Dict[float, int],
    kappa: float
) -> float:
    Xcand = to_X_1d(unevaluated)
    mu, sigma = gp.predict(Xcand, return_std=True)
    lcb = mu - kappa * sigma

    best_idx = None
    best_lcb = float("inf")
    best_dist = float("inf")

    for i, p1 in enumerate(unevaluated):
        score = float(lcb[i])
        dist = abs(idx1[p1] - idx1[global_best_p1])

        if score < best_lcb - 1e-12:
            best_lcb = score
            best_dist = dist
            best_idx = i
        elif abs(score - best_lcb) <= 1e-12 and dist < best_dist:
            best_dist = dist
            best_idx = i

    return unevaluated[best_idx]

# -------------------------------
# Evaluation
# -------------------------------
def evaluate_one_combination_return_value(p1: float, p2: Optional[float] = None) -> float:
    mu = p1
    par = p2

    if version == 0:
        file_name = f"mu_{mu:.2f}_beta_{par:.2f}.csv"
        alpha, beta, gamma = [None, par, None]
    elif version == 1:
        file_name = f"mu_{mu:.2f}_alpha_{par:.2f}.csv"
        alpha, beta, gamma = [par, None, None]
    elif version == 2:
        file_name = f"mu_{mu:.2f}_gamma_{par:.2f}.csv"
        alpha, beta, gamma = [None, None, par]
    else:
        file_name = f"mu_{mu:.2f}.csv"
        par = None
        alpha, beta, gamma = [None, None, None]

    combo_max_value = float("-inf")

    create_empty_csv(mu, par, result_directory, file_name)
    file_path = os.path.join(result_directory, file_name)

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["P", "n", "Algorithm Time", "Optimal Time", "Makespan Ratio"])

        args_list = [(folder, priority_num, mu, alpha, beta, gamma, version, writer)]

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(compute_and_save, *args) for args in args_list]
            for future in as_completed(futures):
                max_value = future.result()
                if max_value > combo_max_value:
                    combo_max_value = max_value

    print(combo_max_value)
    return combo_max_value

# -------------------------------
# Main
# -------------------------------
def main():
    ensure_dir(OUTPUT_DIR)

    tee = TeeStdout(TERMINAL_LOG_TXT)
    old_stdout = sys.stdout
    sys.stdout = tee

    try:
        p1_values = frange_inclusive(P1_MIN, P1_MAX, P1_STEP)
        idx1 = build_index(p1_values)

        # =========================================================
        # FAIR: 1-parameter search
        # =========================================================
        if version == 3:
            all_points = list(p1_values)
            pyrandom.shuffle(all_points)

            fields = ["eval_id", "P1", "value", "global_best_value", "global_best_P1"]
            write_csv_header_if_missing(COMBO_RESULTS_CSV, fields)

            evaluated = set()
            X_obs: List[float] = []
            y_obs: List[float] = []

            global_best_val = float("inf")
            global_best_p1: Optional[float] = None

            no_improve = 0
            eval_id = 0

            print("=== START Bayesian-like search for FAIR (1D, NO repeats) ===")
            print(f"Grid size: {len(all_points)} total combos")
            print(f"Initial random evals: {N_INITIAL}, Max evals: {MAX_EVALS}, kappa={KAPPA}\n")

            initial = []
            for p1 in all_points:
                if len(initial) >= min(N_INITIAL, len(all_points)):
                    break
                if p1 not in evaluated:
                    initial.append(p1)

            for p1 in initial:
                val = evaluate_one_combination_return_value(p1)

                eval_id += 1
                evaluated.add(p1)
                X_obs.append(p1)
                y_obs.append(val)

                if val + MIN_IMPROVEMENT < global_best_val:
                    global_best_val = val
                    global_best_p1 = p1
                    no_improve = 0
                else:
                    no_improve += 1

                append_csv_row(COMBO_RESULTS_CSV, fields, {
                    "eval_id": eval_id,
                    "P1": p1,
                    "value": val,
                    "global_best_value": global_best_val,
                    "global_best_P1": global_best_p1
                })

                print(f"[init {eval_id}/{min(N_INITIAL, len(all_points))}] {p1} -> {val:.6g} | best={global_best_val:.6g} @ {global_best_p1}")

                if eval_id >= MAX_EVALS:
                    break

            if global_best_p1 is None:
                print("No evaluations were run. Exiting.")
                return

            no_improve = 0

            while eval_id < min(MAX_EVALS, len(all_points)):
                if no_improve >= SAT_PATIENCE:
                    print(f"\nStopping: no improvement for {SAT_PATIENCE} steps (saturation).")
                    break

                X = to_X_1d(X_obs)
                y = np.array(y_obs, dtype=float)
                gp = fit_surrogate(X, y)

                unevaluated = [p1 for p1 in all_points if p1 not in evaluated]
                if not unevaluated:
                    print("\nNo more unseen combinations left.")
                    break

                next_p1 = propose_next_1d(
                    unevaluated=unevaluated,
                    gp=gp,
                    global_best_p1=global_best_p1,
                    idx1=idx1,
                    kappa=KAPPA
                )

                val = evaluate_one_combination_return_value(next_p1)

                eval_id += 1
                evaluated.add(next_p1)
                X_obs.append(next_p1)
                y_obs.append(val)

                improved = False
                if val + MIN_IMPROVEMENT < global_best_val:
                    global_best_val = val
                    global_best_p1 = next_p1
                    no_improve = 0
                    improved = True
                else:
                    no_improve += 1

                append_csv_row(COMBO_RESULTS_CSV, fields, {
                    "eval_id": eval_id,
                    "P1": next_p1,
                    "value": val,
                    "global_best_value": global_best_val,
                    "global_best_P1": global_best_p1
                })

                print(f"\n[step {eval_id}] proposed={next_p1} -> {val:.6g}")
                print(f"         best={global_best_val:.6g} @ {global_best_p1} | improved={improved} | no_improve={no_improve}/{SAT_PATIENCE}")

            print("\n=== FINAL ===")
            print(f"Evaluations run: {eval_id}/{min(MAX_EVALS, len(all_points))}")
            print(f"Best value: {global_best_val}")
            print(f"Best P1: {global_best_p1}")
            print(f"Saved CSV: {COMBO_RESULTS_CSV}")
            print(f"Saved terminal log: {TERMINAL_LOG_TXT}")

        # =========================================================
        # MAST / MTSA / MTPA: 2-parameter search
        # =========================================================
        else:
            p2_values = frange_inclusive(P2_MIN, P2_MAX, P2_STEP)
            idx2 = build_index(p2_values)

            all_pairs = list(itertools.product(p1_values, p2_values))
            pyrandom.shuffle(all_pairs)

            fields = ["eval_id", "P1", "P2", "value", "global_best_value", "global_best_P1", "global_best_P2"]
            write_csv_header_if_missing(COMBO_RESULTS_CSV, fields)

            evaluated = set()
            X_obs: List[Tuple[float, float]] = []
            y_obs: List[float] = []

            global_best_val = float("inf")
            global_best_pair: Optional[Tuple[float, float]] = None

            no_improve = 0
            eval_id = 0

            print("=== START Bayesian-like search (2D, NO repeats) ===")
            print(f"Grid size: {len(all_pairs)} total combos")
            print(f"Initial random evals: {N_INITIAL}, Max evals: {MAX_EVALS}, kappa={KAPPA}\n")

            initial = []
            for pair in all_pairs:
                if len(initial) >= min(N_INITIAL, len(all_pairs)):
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
                    "eval_id": eval_id,
                    "P1": p1,
                    "P2": p2,
                    "value": val,
                    "global_best_value": global_best_val,
                    "global_best_P1": global_best_pair[0] if global_best_pair else None,
                    "global_best_P2": global_best_pair[1] if global_best_pair else None,
                })

                print(f"[init {eval_id}/{min(N_INITIAL, len(all_pairs))}] {pair} -> {val:.6g} | best={global_best_val:.6g} @ {global_best_pair}")

                if eval_id >= MAX_EVALS:
                    break

            if global_best_pair is None:
                print("No evaluations were run. Exiting.")
                return

            no_improve = 0

            while eval_id < min(MAX_EVALS, len(all_pairs)):
                if no_improve >= SAT_PATIENCE:
                    print(f"\nStopping: no improvement for {SAT_PATIENCE} steps (saturation).")
                    break

                X = to_X_2d(X_obs)
                y = np.array(y_obs, dtype=float)
                gp = fit_surrogate(X, y)

                unevaluated = [pair for pair in all_pairs if pair not in evaluated]
                if not unevaluated:
                    print("\nNo more unseen combinations left.")
                    break

                next_pair = propose_next_2d(
                    unevaluated=unevaluated,
                    gp=gp,
                    global_best_pair=global_best_pair,
                    idx1=idx1,
                    idx2=idx2,
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
                    "eval_id": eval_id,
                    "P1": p1,
                    "P2": p2,
                    "value": val,
                    "global_best_value": global_best_val,
                    "global_best_P1": global_best_pair[0],
                    "global_best_P2": global_best_pair[1],
                })

                print(f"\n[step {eval_id}] proposed={next_pair} -> {val:.6g}")
                print(f"         best={global_best_val:.6g} @ {global_best_pair} | improved={improved} | no_improve={no_improve}/{SAT_PATIENCE}")

            print("\n=== FINAL ===")
            print(f"Evaluations run: {eval_id}/{min(MAX_EVALS, len(all_pairs))}")
            print(f"Best value: {global_best_val}")
            print(f"Best (P1, P2): {global_best_pair}")
            print(f"Saved CSV: {COMBO_RESULTS_CSV}")
            print(f"Saved terminal log: {TERMINAL_LOG_TXT}")

    finally:
        sys.stdout = old_stdout
        tee.close()

if __name__ == "__main__":
    main()