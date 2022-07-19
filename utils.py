################################
# Verrecchia Thomas            #
# Summer - 2022                #
# Internship Kansas University #
################################

# A bunch of usefull function to generate task graph and manipulate csv files.

from task import*
from random import*
import csv
import codecs
from numerics import*




def generate_task(w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds):
    """Generate a task based on the boundaries written in numerics"""
    w = uniform(w_bounds[0], w_bounds[1])
    p = randint(p_bounds[0], p_bounds[1])
    d = uniform(alpha_d_bounds[0], alpha_d_bounds[1]) / \
        10 ** (randint(r_d_bounds[0], r_d_bounds[1]))
    c = uniform(alpha_c_bounds[0], alpha_c_bounds[1]) * \
        2 ** (randint(r_c_bounds[0], r_c_bounds[1]))
    return Task(w, p, d, c)

def generate_n_tasks(n,w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds) :
    """Generate a list of n tasks based on the boundaries written in numerics"""
    output = []
    for i in range(n) :
        output += [generate_task(w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds)]
    return output

def extract_dependencies_from_csv(file,utf_code="utf-16") :
    """
    This function extract dependencies from a DAGGEN Output under a csv format.

    For some files you may need to change "utf-16" by "utf-8" depending on the method you used to create the csv files
    from the DAGGEN algorithm.

    """
    edges = []
    f = codecs.open(file,"rb",utf_code)
    reader = csv.reader(f)
    for row in reader :
        if len(row)==1 and row[0][0] != '/' and row[0][0] != 'd' and row[0][0] != '}':
            element = row[0][2:]
            i = 0
            while element[i] != ' ':
                i += 1
            first_node = int(element[0:i]) - 1
            while element[i] == "-" or element[i] == ">" or element[i] == " " :
                i += 1
            j=i
            while element[j] != ' ':
                j += 1
            second_node = int(element[i:j]) - 1
            edge = [first_node,second_node]
            edges += [edge]
    f.close()
    return edges

def generate_nodes_edges(n,w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds,dependency_file) :
    nodes = generate_n_tasks(n,w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds)
    edges = extract_dependencies_from_csv(dependency_file)
    for edge in edges :             # We need to pass from numbers to task objects
        edge[0] = nodes[edge[0]]
        edge[1] = nodes[edge[1]]
    return [nodes,edges]

def save_nodes_in_csv(n,w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds,file):
    """Saves a set of nodes and their parameters in a csv file"""
    nodes = generate_n_tasks(n,w_bounds, p_bounds, alpha_d_bounds, r_d_bounds, alpha_c_bounds, r_c_bounds)
    f = open(file, 'w',newline='')
    writer = csv.writer(f)
    writer.writerow(['w', 'p', 'd', 'c'])
    for task in nodes:
        w = task.get_w()
        p = task.get_p()
        d = task.get_d()
        c = task.get_c()
        writer.writerow([str(w),str(p),str(d),str(c)])
    f.close()

def load_nodes_from_csv(file):
    """Loads a set of nodes from a csv file"""
    f = open(file, 'r', newline='')
    reader = csv.reader(f)
    nodes = []
    for row in reader :
        if row[0] != 'w':
            w = float(row[0])
            p_tild = float(row[1])
            d = float(row[2])
            c = float(row[3])
            nodes += [Task(w,p_tild,d,c)]
    return nodes

