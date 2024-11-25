import os
import csv
from random import uniform, randint
from math import pow


n_values = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

class gen_Task:
    def __init__(self, w, p, d_prime, c_prime):
        self.w = w
        self.p = p
        self.d_prime = d_prime
        self.c_prime = c_prime

    def get_w(self):
        return self.w

    def get_p(self):
        return self.p

    def get_d(self):
        return self.d_prime

    def get_c(self):
        return self.c_prime


def generate_task():
    """Generate a task based on the new parameter distributions."""
    w_bound = uniform(2, 5)
    w = pow(10, w_bound)  # w: X~U(2,5), w = 10^X
    p = randint(1, 1024)        # p: P~U(1,1024) randit - for random integeres,uniform generates decimal numbers too
    d_bound = uniform(-0.5, -3)
    d_prime = pow(10,d_bound )  # d: X~U(-0.5,-3), d = 10^X
    c_bound = uniform(-2, -6)
    c_prime = pow(10, c_bound)    # c: X~U(-2,-6), c = 10^X
    return gen_Task(w, p, d_prime, c_prime)


def generate_n_tasks(n):
    """Generate a list of n tasks using the new distributions."""
    return [generate_task() for _ in range(n)]


def save_nodes_in_csv(n, file_path):
    """Saves a set of nodes and their parameters in a CSV file."""
    nodes = generate_n_tasks(n)
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['w', 'p', 'd', 'c'])
        for task in nodes:
            writer.writerow([task.get_w(), task.get_p(), task.get_d(), task.get_c()])


def main():
    main_folder = "tasks"
    os.makedirs(main_folder, exist_ok=True)

    for n in n_values:
        n_folder = os.path.join(main_folder, f"n={n}")
        os.makedirs(n_folder, exist_ok=True)

        for i in range(1, 101):  # 100 iterations for each n value
            file_path = os.path.join(n_folder, f"{i}.csv")
            save_nodes_in_csv(n, file_path)
            print(f"Generated file: {file_path}")


if __name__ == "__main__":
    main()
