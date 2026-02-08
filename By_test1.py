# my actual functio is different from p1*p2. so just gie blank with comments where i need to place 
# the function. also I want the combinations to give in the range not all values becaus i may increae 
# or decrase range. Also undeer each combination I have 1000 different configuration to run and need
# to find the max values among thse 1000 configs and shold represnet the max value as rsult for thst
# cobination. at the end I need to find the minimum value among al the combinations. For this, give
# code also specify where is hould give 1000 combinations and also I want the result of every
# conofiguratiin shuld be wrutten in a file. and the file shold be accessibale while calculatinif
# the max vlues and min of all values.



# import csv
# import os
# import itertools
# from dataclasses import dataclass
# from typing import Dict, Any, List, Tuple, Iterable, Optional


# # =========================
# # 1) USER INPUTS
# # =========================

# # Range-based grid (you can expand later by changing min/max/step only)
# P1_MIN, P1_MAX, P1_STEP = 1.0, 5.0, 0.5
# P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.5

# # How many (P1,P2) combinations to evaluate (hard cap)
# MAX_COMBO_EVALS = 50

# # Stopping behavior (neighbor-first local search usually needs some runway)
# MIN_EVALS_BEFORE_STOP = 20
# PATIENCE = 10          # stop after this many combos with no improvement in best minimax
# MIN_DELTA = 0.0        # improvement threshold to reset patience

# # Where to write outputs
# OUTPUT_DIR = "results"
# ALL_CONFIG_RESULTS_CSV = os.path.join(OUTPUT_DIR, "all_config_results.csv")
# COMBO_SUMMARY_CSV = os.path.join(OUTPUT_DIR, "combo_summary.csv")
# FINAL_BEST_TXT = os.path.join(OUTPUT_DIR, "final_best.txt")


# # =========================
# # 2) HELPERS
# # =========================

# def frange_inclusive(vmin: float, vmax: float, step: float) -> List[float]:
#     """
#     Inclusive float range that avoids typical float drift.
#     Example: 1.0..5.0 step 0.5 -> [1.0,1.5,...,5.0]
#     """
#     if step <= 0:
#         raise ValueError("step must be > 0")
#     n = int(round((vmax - vmin) / step))
#     vals = [round(vmin + i * step, 10) for i in range(n + 1)]
#     # Ensure last is vmax if close
#     if abs(vals[-1] - vmax) > 1e-9:
#         vals.append(round(vmax, 10))
#     # Remove any overshoot
#     vals = [v for v in vals if v <= vmax + 1e-9]
#     return vals

# def ensure_dir(path: str) -> None:
#     os.makedirs(path, exist_ok=True)

# def write_csv_header_if_missing(path: str, fieldnames: List[str]) -> None:
#     if not os.path.exists(path):
#         with open(path, "w", newline="") as f:
#             w = csv.DictWriter(f, fieldnames=fieldnames)
#             w.writeheader()

# def append_csv_row(path: str, fieldnames: List[str], row: Dict[str, Any]) -> None:
#     with open(path, "a", newline="") as f:
#         w = csv.DictWriter(f, fieldnames=fieldnames)
#         w.writerow(row)

# def build_index_map(values: List[float]) -> Dict[float, int]:
#     return {v: i for i, v in enumerate(values)}

# def manhattan_index_distance(p1: float, p2: float,
#                              base_p1: float, base_p2: float,
#                              idx1: Dict[float, int], idx2: Dict[float, int]) -> int:
#     return abs(idx1[p1] - idx1[base_p1]) + abs(idx2[p2] - idx2[base_p2])

# def neighbor_ordered_candidates(all_pairs: List[Tuple[float, float]],
#                                 center: Tuple[float, float],
#                                 idx1: Dict[float, int], idx2: Dict[float, int]) -> List[Tuple[float, float]]:
#     """
#     Returns all_pairs sorted by Manhattan distance from center in grid index-space.
#     Nearest first => "try nearby values always".
#     """
#     c1, c2 = center
#     ranked = []
#     for (p1, p2) in all_pairs:
#         if (p1, p2) == center:
#             continue
#         d = manhattan_index_distance(p1, p2, c1, c2, idx1, idx2)
#         ranked.append((d, (p1, p2)))
#     ranked.sort(key=lambda x: x[0])
#     return [pair for _, pair in ranked]


# # =========================
# # 3) YOU PROVIDE THESE TWO THINGS
# # =========================

# def get_1000_configs_for_combo(p1: float, p2: float) -> Iterable[Dict[str, Any]]:
#     """
#     IMPORTANT: This is where you provide the 1000 configurations.

#     Options you can implement here:
#       A) Read configs from a CSV/JSON file (same 1000 for all combos)
#       B) Generate them programmatically
#       C) Use different 1000 per (p1,p2)

#     Must yield dict-like configs with at least a unique 'config_id'.

#     Example placeholder yields 1000 dummy configs:
#     """
#     for i in range(1000):
#         yield {"config_id": i}
#     # Replace this with your real config generation or file loading.


# def run_one_config(p1: float, p2: float, cfg: Dict[str, Any]) -> float:
#     """
#     IMPORTANT: This is your REAL expensive function.
#     It must return a SINGLE numeric value for this config under this (p1,p2).

#     For your case, this might run the simulation and return the makespan ratio,
#     or it might return the max ratio across a scenario set inside the config.
#     YOU decide.

#     Replace the 'raise NotImplementedError' with your actual computation.
#     """
#     # ----------------------------
#     # TODO: PUT YOUR REAL FUNCTION HERE
#     # Example outline:
#     #
#     # 1) Prepare input files / command args using p1,p2,cfg
#     # 2) Run the workflow / simulation
#     # 3) Parse outputs
#     # 4) Return numeric metric
#     #
#     # return metric_value
#     # ----------------------------
#     raise NotImplementedError("Replace this with your real config evaluation.")


# # =========================
# # 4) EVALUATE ONE (P1,P2) COMBINATION
# # =========================

# @dataclass
# class ComboResult:
#     combo_id: int
#     p1: float
#     p2: float
#     combo_max_over_1000: float

# def evaluate_combo(combo_id: int, p1: float, p2: float) -> ComboResult:
#     """
#     Runs 1000 configs, writes EVERY config result, and returns max over those 1000.
#     """
#     max_val = float("-inf")

#     # Per-config output schema
#     config_fields = ["combo_id", "P1", "P2", "config_id", "value"]
#     write_csv_header_if_missing(ALL_CONFIG_RESULTS_CSV, config_fields)

#     for cfg in get_1000_configs_for_combo(p1, p2):
#         config_id = cfg.get("config_id")
#         if config_id is None:
#             raise ValueError("Each config must include a unique 'config_id'.")

#         # Run your real function
#         value = run_one_config(p1, p2, cfg)

#         # Write every config result to file immediately (so it's always accessible)
#         append_csv_row(
#             ALL_CONFIG_RESULTS_CSV,
#             config_fields,
#             {"combo_id": combo_id, "P1": p1, "P2": p2, "config_id": config_id, "value": value}
#         )

#         # Update max over 1000
#         if value > max_val:
#             max_val = value

#     return ComboResult(combo_id=combo_id, p1=p1, p2=p2, combo_max_over_1000=max_val)


# # =========================
# # 5) MAIN: NEIGHBOR-FIRST SEARCH OVER (P1,P2)
# # =========================

# def main():
#     ensure_dir(OUTPUT_DIR)

#     p1_values = frange_inclusive(P1_MIN, P1_MAX, P1_STEP)
#     p2_values = frange_inclusive(P2_MIN, P2_MAX, P2_STEP)

#     idx1 = build_index_map(p1_values)
#     idx2 = build_index_map(p2_values)

#     all_pairs = list(itertools.product(p1_values, p2_values))
#     evaluated = set()

#     # We start from the minimum corner (you can change this start point)
#     current_best_pair = (p1_values[0], p2_values[0])

#     best_minimax = float("inf")  # MIN over combos of (MAX over 1000 configs)
#     best_pair: Optional[Tuple[float, float]] = None

#     no_improve = 0
#     combo_id = 0

#     # Combo summary schema
#     combo_fields = ["combo_id", "P1", "P2", "combo_max_over_1000", "best_minimax_so_far"]
#     write_csv_header_if_missing(COMBO_SUMMARY_CSV, combo_fields)

#     while combo_id < MAX_COMBO_EVALS:
#         # stopping: patience (after minimum evals)
#         if combo_id >= MIN_EVALS_BEFORE_STOP and no_improve >= PATIENCE:
#             print(f"Stopping: no improvement for {PATIENCE} combos (patience).")
#             break

#         # Pick next pair: nearest neighbors around current best pair
#         candidates = neighbor_ordered_candidates(all_pairs, current_best_pair, idx1, idx2)

#         next_pair = None
#         # Try nearest unseen neighbor first
#         for pair in candidates:
#             if pair not in evaluated:
#                 next_pair = pair
#                 break

#         # If all neighbors exhausted (rare), pick any remaining
#         if next_pair is None:
#             for pair in all_pairs:
#                 if pair not in evaluated:
#                     next_pair = pair
#                     break

#         # Nothing left
#         if next_pair is None:
#             print("No more (P1,P2) pairs to evaluate.")
#             break

#         combo_id += 1
#         p1, p2 = next_pair
#         evaluated.add(next_pair)

#         print(f"\n=== Combo {combo_id:02d}/{MAX_COMBO_EVALS}: P1={p1}, P2={p2} ===")

#         # Evaluate this combo by running 1000 configs and taking max
#         result = evaluate_combo(combo_id, p1, p2)

#         # Update minimax best
#         if result.combo_max_over_1000 + MIN_DELTA < best_minimax:
#             best_minimax = result.combo_max_over_1000
#             best_pair = (p1, p2)
#             current_best_pair = (p1, p2)  # center search around new best
#             no_improve = 0
#         else:
#             no_improve += 1

#         # Write combo summary (so you can inspect progress at any time)
#         append_csv_row(
#             COMBO_SUMMARY_CSV,
#             combo_fields,
#             {
#                 "combo_id": result.combo_id,
#                 "P1": result.p1,
#                 "P2": result.p2,
#                 "combo_max_over_1000": result.combo_max_over_1000,
#                 "best_minimax_so_far": best_minimax,
#             }
#         )

#         print(f"Combo max over 1000 configs = {result.combo_max_over_1000}")
#         print(f"Best minimax so far = {best_minimax} @ {best_pair}")

#     # Final output
#     with open(FINAL_BEST_TXT, "w") as f:
#         f.write(f"Best minimax (min over combos of max over 1000 configs): {best_minimax}\n")
#         f.write(f"Best (P1,P2): {best_pair}\n")

#     print("\n=== FINAL ===")
#     print(f"Best minimax = {best_minimax}")
#     print(f"Best (P1,P2) = {best_pair}")
#     print(f"\nFiles written:")
#     print(f"  - All config results: {ALL_CONFIG_RESULTS_CSV}")
#     print(f"  - Combo summary:      {COMBO_SUMMARY_CSV}")
#     print(f"  - Final best:         {FINAL_BEST_TXT}")


# if __name__ == "__main__":
#     main()




import os
import csv
import itertools
from typing import Optional, Tuple, Dict, Any, List


# =========================
# 1) USER INPUTS (CHANGE THESE ANYTIME)
# =========================

P1_MIN, P1_MAX, P1_STEP = 1.0, 5.0, 0.5
P2_MIN, P2_MAX, P2_STEP = 1.0, 5.0, 0.5

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


# =========================
# 3) YOU PROVIDE THIS
# =========================

def evaluate_one_combination_return_value(p1: float, p2: float) -> float:
    """
    YOU implement this.

    It must return ONE numeric value for the (p1,p2) combination.
    In your case, that value is:
        value(p1,p2) = MAX over 1000 configs (whatever metric you compute)

    Example:
        return max(run_config(cfg, p1, p2) for cfg in configs_1000)

    Put your real logic here.
    """
    # -----------------------------
    # TODO: YOUR CODE GOES HERE
    # -----------------------------
    raise NotImplementedError


# =========================
# 4) MAIN: FIND MINIMUM AMONG COMBINATIONS
# =========================

def main():
    ensure_dir(OUTPUT_DIR)

    p1_values = frange_inclusive(P1_MIN, P1_MAX, P1_STEP)
    p2_values = frange_inclusive(P2_MIN, P2_MAX, P2_STEP)

    all_pairs = list(itertools.product(p1_values, p2_values))

    fields = ["combo_id", "P1", "P2", "value"]  # value = your returned metric for the combo
    write_csv_header_if_missing(COMBO_RESULTS_CSV, fields)

    best_min_value = float("inf")  # MIN over combos of value(p1,p2)
    best_pair: Optional[Tuple[float, float]] = None

    for combo_id, (p1, p2) in enumerate(all_pairs, start=1):
        print(f"Evaluating combo {combo_id}/{len(all_pairs)}: P1={p1}, P2={p2}")

        # Your function returns the per-combo value (already max-over-configs on your side)
        value = evaluate_one_combination_return_value(p1, p2)

        # Write each combo's result immediately (persistent + accessible)
        append_csv_row(COMBO_RESULTS_CSV, fields, {
            "combo_id": combo_id,
            "P1": p1,
            "P2": p2,
            "value": value,
        })

        # Track global minimum
        if value < best_min_value:
            best_min_value = value
            best_pair = (p1, p2)

        print(f"  value={value} | best_min={best_min_value} @ {best_pair}")

    # Final result written to a file
    with open(FINAL_MIN_TXT, "w") as f:
        f.write(f"Minimum value among all combinations: {best_min_value}\n")
        f.write(f"Best (P1,P2) combination: {best_pair}\n")

    print("\n=== FINAL ===")
    print(f"Minimum value = {best_min_value}")
    print(f"Best (P1,P2)  = {best_pair}")
    print(f"\nFiles written:")
    print(f"  - Combo results: {COMBO_RESULTS_CSV}")
    print(f"  - Final min:     {FINAL_MIN_TXT}")


if __name__ == "__main__":
    main()

