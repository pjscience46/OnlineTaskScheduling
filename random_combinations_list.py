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


parameters = []
pattern = r"--regular ([\d.]+) --fat ([\d.]+) --jump (\d+) -n \d+ --density ([\d.]+)"
row = 0
for i in result:
    P_value, n_value, random_file_number = i
    file_path = "GRAPHS/" + 'n'+ "=" +str(n_value) + "/" + "daggen_output_"+ str(random_file_number) + ".csv"
    with open(file_path, 'r') as file:
        content = file.read()

    match = re.search(pattern, content)
    if match:
            regular = float(match.group(1))
            fat = float(match.group(2))
            jump = int(match.group(3))
            density = float(match.group(4))
            row = row + 1
            parameters.append([row,P_value, n_value, random_file_number,regular,fat,jump,density])
            print(f"Row {row} added to the file")
    else:
        print(f"Pattern not found in file: {file_path}")
    
df = pd.DataFrame(parameters, columns=["Row","P", "n","File_Number","Regular","Fat","Jump","Density"])
df.to_csv('combinations.csv', index=False)


