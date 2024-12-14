import itertools
import random
import pandas as pd
import re
import csv
import os


P = [128, 256, 512, 1024, 2048, 4096, 8192]
n = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

# Generate all combinations of P and n
all_combinations = list(itertools.product(P, n))
unique_combinations = set()
result = []
row = 0
while len(result) < 1000:  # Ensure exactly 1000 unique entries
    # Randomly pick a combination of P and n
    P_value, n_value = random.choice(all_combinations)
    # Generate a random number within the range
    random_file_number = random.randint(1, 100)
    # Check if the combination is unique
    if (P_value, n_value, random_file_number) not in unique_combinations:
        # Add the unique combination to the set and the result list
        unique_combinations.add((P_value, n_value, random_file_number))
        result.append([P_value, n_value, random_file_number])
        row = row+1
        print(f"Row {row} added to the file")

    
df = pd.DataFrame(result, columns=["P", "n","Index"])
df.to_csv('combinations.csv', index=False)


