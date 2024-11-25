
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

MODEL_LIST = [RooflineModel(),AmdahlModel(),AmdahlModel(),CommunicationModel()]

#MODEL_LIST = [Roofline()]
def generate_task(w_bounds, p_bounds, d_prime_bounds, c_prime_bounds):
    """Generate a task based on the boundaries written in numerics"""
    w = uniform(w_bounds[0], w_bounds[1])
    p = randint(p_bounds[0], p_bounds[1])
    d_prime = uniform(dprime_bounds[0], dprime_bounds[1])
    c_prime = uniform(cprime_bounds[0], cprime_bounds[1])
    return Task(w, p, d_prime, c_prime)


def generate_n_tasks(n, w_bounds, p_bounds, d_prime_bounds, c_prime_bounds):
    """Generate a list of n tasks based on the boundaries written in numerics"""
    output = []
    for i in range(n):
        output += [generate_task(w_bounds, p_bounds, d_prime_bounds, c_prime_bounds)]
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


def generate_nodes_edges(n, w_bounds, p_bounds, d_prime_bounds, c_prime_bounds, dependency_file):
    nodes = generate_n_tasks(n, w_bounds, p_bounds, d_prime_bounds, c_prime_bounds)
    edges = extract_dependencies_from_csv(dependency_file)
    for edge in edges:  # We need to pass from numbers to task objects
        edge[0] = nodes[edge[0]]
        edge[1] = nodes[edge[1]]
    return [nodes, edges]


def save_nodes_in_csv(n, w_bounds, p_bounds, d_prime_bounds, c_prime_bounds, file):
    """Saves a set of nodes and their parameters in a csv file"""
    nodes = generate_n_tasks(n, w_bounds, p_bounds, d_prime_bounds, c_prime_bounds)
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


def compute_and_save(variation_parameter, result_directory,model_name,instances_nb,mu,alpha,beta,gamma,version, P,n,writer):
  
    model = {}
    if(model_name == 'General'):
        model = GeneralModel()
    elif(model_name == 'Roofline'):
        model = RooflineModel()
    elif(model_name == 'Amdahl'):
        model = AmdahlModel()
    elif(model_name == 'Communication'):
        model = CommunicationModel()

    for i in range(1, instances_nb + 1):

            daggen_file = "DAGGEN/" + variation_parameter + "_variation/" + variation_parameter + "=" + \
                            str(n) + "/" + str(i) + ".csv"
        
            node_file = "Tasks/n=" + str(n) + "/" + str(i) + ".csv"
            nodes = load_nodes_from_csv(node_file) #w,p,c,d
            edges = extract_dependencies_from_csv(daggen_file)
            task_graph = Graph(nodes, edges) #generate task graphs
            processors = Processors(P)
            adjacency = task_graph.get_adjacency()

            #opt time is max (Amin/p , cmin)
            time_opt = task_graph.get_T_opt(P, adjacency, speedup_model=model)
            # three Algorithms
            time_algo_1 = processors.online_scheduling_algorithm(task_graph, 1, alpha=alpha,beta=beta,gamma=gamma,
                                                                    adjacency=adjacency, mu=mu
                                                                    , speedup_model=model, P=P
                                                                   ,version=version)
            # Minimum time algorithm
            min_time = processors.online_scheduling_algorithm(task_graph, 2, alpha=alpha,beta=beta,gamma=gamma,
                                                                    adjacency=adjacency, mu=mu
                                                                    , speedup_model=model, P=P
                                                                   ,version=version)
            mtsa = (time_algo_1/time_opt)
            writer.writerow([str(P),str(n), str(time_algo_1), str(min_time), str(time_opt),str(mtsa)])
    

