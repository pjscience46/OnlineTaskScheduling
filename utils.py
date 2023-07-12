################################
# Verrecchia Thomas            #
# Summer - 2022                #
# Internship Kansas University #
################################
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

MODEL_LIST = [Power0Model()]


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


def compute_and_save(variation_parameter, result_directory, instances_nb, version):
    """

    :param variation_parameter: Can be : 'Fat', 'density', 'regular', 'jump', 'p', 'n'
    :param result_directory: A path to a directory containing 4 empty directories named 'Amdahl', 'communication',
                            'General', 'Roofline'.
    :param instances_nb: The number of different tasks graphs you want to run for each set of parameters. Must be picked
                         in the range [1,30]
    :return: Save the results in the corresponding directory depending on the speedup model
    """

    # Fixed parameters
    model_list = MODEL_LIST
    # name_list = ['Amdahl', 'Communication', 'General', 'Roofline']
    # mu_paper = [(1 - sqrt(8 * sqrt(2) - 11)) / 2, (23 - sqrt(313)) / 18, (33 - sqrt(738)) / 27, (3 - sqrt(5)) / 2]
    # alpha_paper = [(sqrt(2) + 1 + sqrt(2 * sqrt(2) - 1)) / 2, 4 / 3, 2, 1]
    P = 1500
    n = 500

    # Variations
    p_list = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    n_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # n_list = [1000]
    parameter_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # Used to variate Fat, density and regular
    # parameter_list = [0.1]
    jump = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Used to variate jump

    # for j in range(len(name_list)):
    start_time = time.process_time_ns()
    num = 1
    for idx, model in enumerate(model_list):
        # Opening the result file
        f = open(result_directory + str(model.name) +
                 "/all.csv", 'w', newline='')
        writer = csv.writer(f)
        writer.writerow([variation_parameter, 'Paper', 'Min Time', 'Time opt'])

        for i in range(1, instances_nb + 1):
            for k in range(len(parameter_list)):
                pc = num / (instances_nb * len(parameter_list) * len(MODEL_LIST))
                eta = ((time.process_time_ns() - start_time) / 1e9) * ((1 - pc) / pc)
                print(f"[{pc * 100:.2f} %]"
                      f" {model.name} model ({idx + 1}/{len(MODEL_LIST)}),"
                      f" instance {i:2d}/{instances_nb},"
                      f" parameter {k + 1:2d}/{len(parameter_list)}"
                      f" ETA: {int(eta)}s")
                num += 1
                if variation_parameter == 'Fat' or variation_parameter == 'density' or \
                        variation_parameter == 'regular':
                    daggen_file = "DAGGEN/" + variation_parameter + "_variation/" + variation_parameter + "=" + \
                                  str(parameter_list[k]) + "/" + str(i) + ".csv"
                    node_file = "TASKS/n=500/" + str(i) + ".csv"
                elif variation_parameter == 'jump':
                    daggen_file = "DAGGEN/" + variation_parameter + "_variation/" + variation_parameter + "=" + \
                                  str(jump[k]) + "/" + str(i) + ".csv"
                    node_file = "TASKS/n=500/" + str(i) + ".csv"

                elif variation_parameter == 'n':
                    daggen_file = "DAGGEN/" + variation_parameter + "_variation/" + variation_parameter + "=" + \
                                  str(n_list[k]) + "/" + str(i) + ".csv"
                    node_file = "TASKS/n=" + str(n_list[k]) + "/" + str(i) + ".csv"
                else:
                    daggen_file = "DAGGEN/density_variation/density=0.5/" + str(i) + ".csv"
                    node_file = "TASKS/n=500/" + str(i) + ".csv"

                nodes = load_nodes_from_csv(node_file)
                edges = extract_dependencies_from_csv(daggen_file)

                mu_tild = model.get_mu()
                alpha_tild = model.get_alpha()

                if variation_parameter == 'p':
                    p_tild = p_list[k]
                else:
                    p_tild = P

                task_graph = Graph(nodes, edges)
                processors = Processors(p_tild)

                if variation_parameter == 'n':
                    logging.debug("\nmodel : " + model.name,
                                  variation_parameter + " = " + str(n_list[k]) + ", file :" + str(i))
                elif variation_parameter == 'p':
                    logging.debug("model : " + model.name,
                                  variation_parameter + " = " + str(p_list[k]) + ", file :" + str(i))
                elif variation_parameter == 'jump':
                    logging.debug("model : " + model.name,
                                  variation_parameter + " = " + str(jump[k]) + ", file :" + str(i))
                else:
                    logging.debug("model : " + model.name,
                                  variation_parameter + " = " + str(parameter_list[k]) + ", file :" + str(i))
                logging.debug("Computing adjacency matrix...")
                adjacency = task_graph.get_adjacency()

                speedup_model = model

                time_opt = task_graph.get_T_opt(p_tild, adjacency, speedup_model=speedup_model)
                # print("start paper")
                time_algo_1 = processors.online_scheduling_algorithm(task_graph, 1, alpha=alpha_tild,
                                                                     adjacency=adjacency, mu_tild=mu_tild
                                                                     , speedup_model=speedup_model, P_tild=p_tild
                                                                     , version=version)
                # print("start min")
                time_algo_2 = processors.online_scheduling_algorithm(task_graph, 2, alpha=alpha_tild,
                                                                     adjacency=adjacency, mu_tild=mu_tild
                                                                     , speedup_model=speedup_model, P_tild=p_tild
                                                                     , version=version)
                # print("end")
                if variation_parameter == "Fat" or variation_parameter == "density" or variation_parameter == "regular":
                    writer.writerow([str(parameter_list[k]), str(time_algo_1), str(time_algo_2), str(time_opt)])
                elif variation_parameter == "jump":
                    writer.writerow([str(jump[k]), str(time_algo_1), str(time_algo_2), str(time_opt)])
                elif variation_parameter == "n":
                    writer.writerow([str(n_list[k]), str(time_algo_1), str(time_algo_2), str(time_opt)])
                else:
                    writer.writerow([str(p_list[k]), str(time_algo_1), str(time_algo_2), str(time_opt)])
        f.close()


def display_results(variation_parameter, result_directory):
    model_list = MODEL_LIST
    # name_list = ["Amdahl", "Communication", "General", "Roofline"]
    p_list = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    n_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    # n_list = [100, 200, 300]
    parameter_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    # parameter_list = [0.1, 0.5, 1]
    jump_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for model in model_list:
        Paper = [[] for i in range(10)]
        Min_time = [[] for i in range(10)]
        f = open(result_directory + model.name + "/all.csv", newline='')
        reader = csv.reader(f)
        for row in reader:
            if row[0] != variation_parameter:
                if (row[0] == "0.1") or (row[0] == "100") or (row[0] == "500" and variation_parameter == "p") \
                        or (row[0] == "1" and variation_parameter == "jump"):
                    index = 0
                if (row[0] == "0.2") or (row[0] == "2") or (row[0] == "200") or (row[0] == "1000"):
                    index = 1
                if (row[0] == "0.3") or (row[0] == "3") or (row[0] == "300") or (row[0] == "1500"):
                    index = 2
                if (row[0] == "0.4") or (row[0] == "4") or (row[0] == "400") or (row[0] == "2000"):
                    index = 3
                if (row[0] == "0.5") or (row[0] == "5") or (row[0] == "500" and variation_parameter == "n") \
                        or (row[0] == "2500"):
                    index = 4
                if (row[0] == "0.6") or (row[0] == "6") or (row[0] == "600") or (row[0] == "3000"):
                    index = 5
                if (row[0] == "0.7") or (row[0] == "7") or (row[0] == "700") or (row[0] == "3500"):
                    index = 6
                if (row[0] == "0.8") or (row[0] == "8") or (row[0] == "800") or (row[0] == "4000"):
                    index = 7
                if (row[0] == "0.9") or (row[0] == "9") or (row[0] == "900") or (row[0] == "4500"):
                    index = 8
                if (row[0] == "1" and (variation_parameter == "Fat" or variation_parameter == "density"
                                       or variation_parameter == "regular")) or \
                        (row[0] == "10" and variation_parameter == "jump") or \
                        (row[0] == "1000" and variation_parameter == 'n') \
                        or (row[0] == "5000"):
                    index = 9

                Paper[index] += [float(row[1]) / float(row[3])]
                Min_time[index] += [float(row[2]) / float(row[3])]
        f.close()
        f = open(result_directory + model.name + "/mean.csv", 'w', newline='')
        writer = csv.writer(f)
        mean_Paper = []
        mean_Time = []
        if variation_parameter == "density" or variation_parameter == "Fat" or variation_parameter == "regular":
            new_list = parameter_list
        elif variation_parameter == "jump":
            new_list = jump_list
        elif variation_parameter == "n":
            new_list = n_list
        else:
            new_list = p_list
        for k in new_list:
            if k == new_list[0]:
                index = 0
            if k == new_list[1]:
                index = 1
            if k == new_list[2]:
                index = 2
            if k == new_list[3]:
                index = 3
            if k == new_list[4]:
                index = 4
            if k == new_list[5]:
                index = 5
            if k == new_list[6]:
                index = 6
            if k == new_list[7]:
                index = 7
            if k == new_list[8]:
                index = 8
            if k == new_list[9]:
                index = 9

            writer.writerow([k, mean(Paper[index]), mean(Min_time[index])])
            mean_Paper += [mean(Paper[index])]
            mean_Time += [mean(Min_time[index])]
        f.close()

        # Graphic parameters for the display

        plt.plot(new_list, mean_Paper, label='Algo Paper')
        plt.plot(new_list, mean_Time, label='Min Time')
        # plt.boxplot([Paper[0],Min_time[0]])
        plt.xlabel(variation_parameter)
        plt.legend()
        plt.ylabel("Normalized Makespan")
        plt.title(model.name)
        plt.savefig(result_directory + variation_parameter + "_" + model.name)
        plt.show()


def display_multiple_results(version1, version2, variation_parameter, saving_directory):
    name_1 = "Paper " + version1
    name_2 = "Paper " + version2

    name_list = ["Amdahl", "Communication", "General", "Roofline"]

    for name in name_list:
        file_1 = "Results_" + version1 + "/" + variation_parameter + "/" + name + "/"
        file_2 = "Results_" + version2 + "/" + variation_parameter + "/" + name + "/"
        p_list = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
        n_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        parameter_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        jump_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        if variation_parameter == "Density" or variation_parameter == "Fat" or variation_parameter == "Regular":
            new_list = parameter_list
        elif variation_parameter == "Jump":
            new_list = jump_list
        elif variation_parameter == "n":
            new_list = n_list
        else:
            new_list = p_list

        f = open(file_1 + "/mean.csv", 'r', newline='')
        reader = csv.reader(f)
        mean_Paper_file_1 = []
        if version1 == "V1":
            if variation_parameter == "Density" or variation_parameter == "Fat" or variation_parameter == "Regular" \
                    or variation_parameter == "Jump":
                next(reader)
        for line in reader:
            mean_Paper_file_1 += [float(line[1])]
        f.close()
        f = open(file_2 + "/mean.csv", 'r', newline='')
        reader = csv.reader(f)
        mean_Paper_file_2 = []
        mean_Time = []
        for line in reader:
            mean_Paper_file_2 += [float(line[1])]
            mean_Time += [float(line[2])]

        # Display parameters
        ###############################################################################################################
        plt.plot(new_list, mean_Paper_file_1, label=name_1)
        plt.plot(new_list, mean_Paper_file_2, label=name_2)
        plt.plot(new_list, mean_Time, label='Min Time')
        plt.xlabel(variation_parameter)
        plt.legend()
        plt.title(variation_parameter + " , " + name)
        plt.ylabel("Normalized Makespan")
        plt.savefig(saving_directory + "/" + variation_parameter + "/" + name + ".png")
        plt.show()


def display_results_boxplot(version1, version2, saving_directory):
    name_list = ["Amdahl", "Communication", "General", "Roofline"]
    parameters = ["Density", "Fat", "Jump", "n", "p"]
    for name in name_list:
        Paper_V1 = []
        Paper_V2 = []
        Min_Time = []
        f = open("Results_" + version1 + "/P/" + name + "/all.csv", 'r', newline='')
        reader = csv.reader(f)
        for line in reader:
            if line[0] == "1500":
                Paper_V1 += [float(line[1]) / float(line[3])]
        f.close()
        f = open("Results_" + version2 + "/P/" + name + "/all.csv", 'r', newline='')
        reader = csv.reader(f)
        for line in reader:
            if line[0] == "1500":
                Paper_V2 += [float(line[1]) / float(line[3])]
                Min_Time += [float(line[2]) / float(line[3])]
        f.close()
        plt.boxplot([Paper_V1, Paper_V2, Min_Time])
        plt.xticks([1, 2, 3], ['Paper_' + version1, 'Paper_' + version2, 'Min Time'])
        plt.ylabel('Normalized Makespan')
        plt.savefig(saving_directory + "/" + name + "_Default_parameters.png")
        plt.show()
