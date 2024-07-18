
import time

# A bunch of useful function to generate task graph and manipulate csv files.

from task import *
from random import *
import csv
import codecs
from numerics import *
from processors import *
from statistics import *
import matplotlib.pyplot as plt
from logging import log
from model import *

MODEL_LIST = [RooflineModel()]

#MODEL_LIST = [Roofline()]
def generate_task(w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds):
    """Generate a task based on the boundaries written in numerics"""
    w = uniform(w_bounds[0], w_bounds[1])
    p = randint(p_bounds[0], p_bounds[1])
    d = uniform(alpha_d_bounds[0], alpha_d_bounds[1]) / \
        10 ** (randint(r_d_bounds[0], r_d_bounds[1]))
    c = uniform(alpha_c_bounds[0], alpha_c_bounds[1]) * \
        2 ** (randint(r_c_bounds[0], r_c_bounds[1]))
    return Task(w, p, d, c)


def generate_n_tasks(n, w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds):
    """Generate a list of n tasks based on the boundaries written in numerics"""
    output = []
    for i in range(n):
        output += [generate_task(w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds)]
    return output


def extract_dependencies_from_csv(file, utf_code="utf-16"):
    """
    This function extract dependencies from a DAGGEN Output under a csv format.

    For some files you may need to change "utf-16" by "utf-8" depending on the method you used to create the csv files
    from the DAGGEN algorithm.

    """
    edges = []
    f = codecs.open(file, "rb", utf_code)
    reader = csv.reader(f)
    for row in reader:
        if len(row) == 1 and row[0][0] != '/' and row[0][0] != 'd' and row[0][0] != '}':
            element = row[0][2:]
            i = 0
            while element[i] != ' ':
                i += 1
            first_node = int(element[0:i]) - 1
            while element[i] == "-" or element[i] == ">" or element[i] == " ":
                i += 1
            j = i
            while element[j] != ' ':
                j += 1
            second_node = int(element[i:j]) - 1
            edge = [first_node, second_node]
            edges += [edge]
    f.close()
    return edges


def generate_nodes_edges(n, w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds,
                         dependency_file):
    nodes = generate_n_tasks(n, w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds)
    edges = extract_dependencies_from_csv(dependency_file)
    for edge in edges:  # We need to pass from numbers to task objects
        edge[0] = nodes[edge[0]]
        edge[1] = nodes[edge[1]]
    return [nodes, edges]


def save_nodes_in_csv(n, w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds, file):
    """Saves a set of nodes and their parameters in a csv file"""
    nodes = generate_n_tasks(n, w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds)
    f = open(file, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['w', 'p', 'd', 'c'])
    for task in nodes:
        w = task.get_w()
        p = task.get_p()
        d = task.get_d()
        c = task.get_c()
        writer.writerow([str(w), str(p), str(d), str(c)])
    f.close()


def load_nodes_from_csv(file):
    """Loads a set of nodes from a csv file"""
    f = open(file, 'r', newline='')
    reader = csv.reader(f)
    nodes = []
    for row in reader:
        if row[0] != 'w':
            w = float(row[0])
            p_tild = float(row[1])
            d = float(row[2])
            c = float(row[3])
            nodes += [Task(w, p_tild, d, c)]
    return nodes


def compute_and_save(variation_parameter, result_directory,instances_nb,mu,B,version, P,n,writer):
  
    # Fixed parameters
    model_list = MODEL_LIST
    #n_list = [100]
    # parameter_list = [0.5]
    jump = [1]
    # Variations
    #p_list = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    n_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    
    parameter_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # Used to variate Fat, density and regular
    
    #jump = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Used to variate jump

    # for j in range(len(name_list)):
    start_time = time.process_time_ns()
    num = 1
    # f = open(result_directory + "Roofline" +
    #              "/all.csv", 'w', newline='')
    # writer = csv.writer(f)
    # writer.writerow(['P',variation_parameter, 'Paper', 'Min Time', 'Time opt','Comment'])

    model = MODEL_LIST[0]

    for i in range(1, instances_nb + 1):
    
        #for k in range(len(n_list)):
            # pc = num / (instances_nb * len(n_list) * len(MODEL_LIST))
            # eta = ((time.process_time_ns() - start_time) / 1e9) * ((1 - pc) / pc)
            # # print(f"[{pc * 100:.2f} %]"
            # #         f" {model.name} model ,"
            # #         f" instance {i:2d}/{instances_nb},"
            # #         f" parameter {k + 1:2d}/{len(n_list)}"
            # #         f" ETA: {int(eta)}s")
            # num += 1
            

            daggen_file = "DAGGEN/" + variation_parameter + "_variation/" + variation_parameter + "=" + \
                            str(n) + "/" + str(i) + ".csv"
            node_file = "TASKS/n=" + str(n) + "/" + str(i) + ".csv"

            nodes = load_nodes_from_csv(node_file) #w,p,c,d
            edges = extract_dependencies_from_csv(daggen_file)

            mu_tild = mu #constant value depends up on model
            Beta1 = B
            alpha_tild = model.get_alpha() #constant value depends up on model
            p_tild = P

            task_graph = Graph(nodes, edges) #generate task graphs
            processors = Processors(p_tild)

            if variation_parameter == 'n':
                logging.debug("\nmodel : " + model.name,
                                variation_parameter + " = " + str(n) + ", file :" + str(i))
            
            logging.debug("Computing adjacency matrix...")
            adjacency = task_graph.get_adjacency()

            speedup_model = model
            #opt time is max (Amin/p , cmin)
            time_opt = task_graph.get_T_opt(p_tild, adjacency, speedup_model=speedup_model)
            # print("start paper")
            time_algo_1 = processors.online_scheduling_algorithm(task_graph, 1, alpha=alpha_tild,Beta1=Beta1,
                                                                    adjacency=adjacency, mu_tild=mu_tild
                                                                    , speedup_model=speedup_model, P_tild=p_tild
                                                                   ,version=version)
            # print("start min")
            min_time = processors.online_scheduling_algorithm(task_graph, 2, alpha=alpha_tild,Beta1=Beta1,
                                                                    adjacency=adjacency, mu_tild=mu_tild
                                                                    , speedup_model=speedup_model, P_tild=p_tild
                                                                   ,version=version)
            mtpa = (time_algo_1/time_opt)
            writer.writerow([str(P),str(n), str(time_algo_1), str(min_time), str(time_opt),str(mtpa)])
    

def normalize_list(data_list, mean_value):
    if mean_value == 0:
        return data_list  # Avoid division by zero, return original data if mean is zero
    return [(abs(x - mean_value)) / abs(mean_value) for x in data_list]
