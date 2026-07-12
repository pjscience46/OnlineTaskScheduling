from pathlib import Path
import pandas as pd


def find_column(df, target_name):
    target_clean = target_name.lower().replace(" ", "").replace("_", "")

    for col in df.columns:
        col_clean = col.lower().replace(" ", "").replace("_", "")
        if col_clean == target_clean:
            return col

    return None


def calculate_mean_makespan_ratio(input_file_path):
    csv_file = Path(input_file_path.strip().strip('"'))

    if not csv_file.exists():
        print(f"\nFile not found:\n{csv_file}")
        return

    df = pd.read_csv(csv_file)

    if df.empty:
        print(f"\nFile is empty:\n{csv_file}")
        return

    makespan_col = find_column(df, "Makespan Ratio")

    if makespan_col is None:
        print(f"\nNo Makespan Ratio column found in:\n{csv_file}")
        print("Available columns:")
        print(list(df.columns))
        return

    mean_makespan_ratio = df[makespan_col].mean()

    print("\nMean Makespan Ratio Result")
    print("=" * 60)
    print(f"File                  : {csv_file}")
    print(f"Column                : {makespan_col}")
    print(f"Average Makespan Ratio: {mean_makespan_ratio:.6f}")


if __name__ == "__main__":
    input_file = input("Enter CSV file path: ")
    calculate_mean_makespan_ratio(input_file)