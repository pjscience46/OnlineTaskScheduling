#!/bin/bash

# Number of iterations for each n
iterations_per_n=100
# Directory to store output files
output_dir="GRAPHS"
mkdir -p "$output_dir"

# Loop to run daggen for n = 100, 200, ..., 1000
for ((x=1; x<=10; x++)); do
    n=$((x * 100))
    n_dir="$output_dir/n=$n"
    mkdir -p "$n_dir"  # Create a directory for each n value

    for ((i=1; i<=iterations_per_n; i++)); do
        # Generate random values for each parameter
        fat=$(awk -v min=0.1 -v max=0.9 -v seed1=$RANDOM 'BEGIN{srand(seed1); print min+rand()*(max-min)}')
        density=$(awk -v min=0.1 -v max=0.9 -v seed2=$RANDOM 'BEGIN{srand(seed2); print min+rand()*(max-min)}')
        regular=$(awk -v min=0.1 -v max=0.9 -v seed3=$RANDOM 'BEGIN{srand(seed3); print min+rand()*(max-min)}')
        jump=$((RANDOM % 10 + 1))

        # Output file for each run, saved as CSV
        output_file="$n_dir/daggen_output_$i.csv"

        # Run daggen with the generated parameters and store output
        ./daggen --dot --regular "$regular" --fat "$fat" --jump "$jump" -n "$n" --density "$density" > "$output_file"

        echo "Run $i for n=$n completed with regular=$regular, fat=$fat, jump=$jump, density=$density"
    done
done

echo "All $iterations_per_n runs completed for each value of n. Outputs are saved in $output_dir/"

