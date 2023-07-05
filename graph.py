################################
# Verrecchia Thomas            #
# Summer - 2022                #
# Internship Kansas University #
################################

# This class implement the well known concept of graph, in our case the nodes are tasks (see clas Task) and the graph is
# a directed acyclic graph (DAG)

from task import Task
import numpy as np


class Graph:

    def __init__(self, nodes=None, edges=None):
        self._nodes = nodes  # a list of task [ task1, task2 ... ]
        self._edges = edges  # a list of edge [[ task1, task2],[task3, task4],...]  where task1 is parent
        # to task2 ...

    # Getters and Setters
    ############################################################

    def get_nodes(self):
        return self._nodes

    def get_edges(self):
        return self._edges

    def set_nodes(self, value):
        self._nodes = value

    def set_edges(self, value):
        self._edges = value

    # Methods
    ############################################################

    def add_node(self, node):
        """Nodes must contain only Task objects"""
        nodes = self.get_nodes()
        nodes += [node]
        self.set_nodes(nodes)

    def add_edge(self, edge):
        """Edges must contain only [int,int] objects refering to a certain task in the nodes list"""
        edges = self.get_edges()
        edges += [edge]
        self.set_edges(edges)

    def get_adjacency(self):
        """Return the adjacency matrix of the graph."""
        nodes = self.get_nodes()
        edges = self.get_edges()
        adjacency = np.zeros((len(nodes), len(nodes)))

        # for i in range(len(nodes)):
        #     for j in range(len(nodes)):
        #        if [i, j] in edges:
        #            adjacency[i, j] = 1
        for [i, j] in edges:
            adjacency[i, j] = 1
        return adjacency

    def get_offsprings(self, task, adjacency=[]):
        """Return a list of the offsprings of a certain task. The argument 'task' take an int value corresponding
        to the index of the task in the nodes list"""
        offsprings = []
        nodes = self.get_nodes()
        if adjacency == []:
            adjacency = self.get_adjacency()
        for i in range(len(nodes)):

            if adjacency[task, i] == 1:
                offsprings += [i]

        return offsprings

    def get_parents(self, task, adjacency=[]):
        """Return a list of the parents of a certain task. The argument 'task' take an int value corresponding
        to the index of the task in the nodes list"""
        parents = []
        nodes = self.get_nodes()
        if adjacency == []:
            adjacency = self.get_adjacency()
        for i in range(len(nodes)):
            if adjacency[i, task] == 1:
                parents += [i]
        return parents

    def get_A_min(self, P, speedup_model):
        """A_min is the sum of all the minimum area of each tasks"""
        A_min = 0
        for task in self.get_nodes():
            A_min += task.get_minimum_area(P, speedup_model)[0]
        return A_min

    def get_C_min(self, P, adjacency, speedup_model):
        """C_min is the minimal execution time for the graph"""
        nodes = self.get_nodes()
        maximum_weight = 0
        weights = [0 for i in range(len(nodes))]
        offspring = []
        print("Selecting starting nodes...")

        # Selecting the tasks without parents as starting points
        for index_task in range(len(nodes)):
            if self.get_parents(index_task, adjacency) == []:
                offspring += [index_task]
        print("Calculating Optimal time...")
        compteur = 0
        while offspring != []:
            compteur += 1
            index_task = offspring[0]
            weight = nodes[index_task].get_minimum_execution_time(P, speedup_model)[0]
            p_weight = 0
            for index_parent in self.get_parents(index_task, adjacency):
                if p_weight < weights[index_parent]:
                    p_weight = weights[index_parent]
            weight += p_weight
            if weight > maximum_weight:
                maximum_weight = weight
            weights[index_task] = weight
            offspring.remove(index_task)
            offspring += self.get_offsprings(index_task, adjacency)
            new_list = []  # Avoiding duplicate
            for i in offspring:
                if i not in new_list:
                    new_list.append(i)
            offspring = new_list
        return maximum_weight

    def get_T_opt(self, P, adjacency, speedup_model):
        """Return the inferior bound for T optimal for a given graph"""
        output = max(self.get_A_min(P, speedup_model) / P, self.get_C_min(P, adjacency, speedup_model))
        print("Optimal execution time :", output)
        return output

    def init_status(self):
        """Reset the status of each task in the graph"""
        for task in self.get_nodes():
            task.set_status(0)
