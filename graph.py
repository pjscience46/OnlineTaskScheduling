################################
# Verrecchia Thomas            #
# Summer - 2022                #
# Internship Kansas University #
################################

# This class implement the well known concept of graph, in our case the nodes are tasks (see clas Task) and the graph is
# a directed acyclic graph (DAG)

from task import Task
import numpy as np
import logging
from task import Status


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

        for [i, j] in edges:
            adjacency[i, j] = 1
        return adjacency

    def get_children(self, task, adjacency=None):
        """Return a list of the children of a certain task. The argument 'task' take an int value corresponding
        to the index of the task in the nodes list"""
        children = []
        nodes = self.get_nodes()
        if adjacency is None:
            adjacency = self.get_adjacency()
        for i in range(len(nodes)):
            if adjacency[task, i] == 1:
                children += [i]

        return children

    def get_parents(self, task, adjacency=None):
        """Return a list of the parents of a certain task. The argument 'task' take an int value corresponding
        to the index of the task in the nodes list"""
        parents = []
        nodes = self.get_nodes()
        if adjacency is None:
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
        weights = [0 for _ in range(len(nodes))]

        logging.debug("Selecting starting nodes...")

        free_nodes = []
        free_nodes_set = set()
        # Selecting the tasks without parents as starting points
        for index_task in range(len(nodes)):
            if not self.get_parents(index_task, adjacency):
                free_nodes += [index_task]
                free_nodes_set.add(index_task)
        logging.debug("Calculating Optimal time...")

        idx = 0
        while idx < len(free_nodes):
            index_task = free_nodes[idx]
            idx += 1
            weight = nodes[index_task].get_minimum_execution_time(P, speedup_model)[0]
            p_weight = 0
            for index_parent in self.get_parents(index_task, adjacency):
                if p_weight < weights[index_parent]:
                    p_weight = weights[index_parent]
            weight += p_weight
            if weight > maximum_weight:
                maximum_weight = weight
            weights[index_task] = weight

            for children in self.get_children(index_task, adjacency):
                if children not in free_nodes_set:
                    free_nodes_set.add(children)
                    free_nodes.append(children)

        return maximum_weight

    def get_T_opt(self, P, adjacency, speedup_model):
        """Return the inferior bound for T optimal for a given graph"""
        output = max(self.get_A_min(P, speedup_model) / P, self.get_C_min(P, adjacency, speedup_model))
        logging.debug("Optimal execution time :", output)
        return output

    def init_status(self):
        """Reset the status of each task in the graph"""
        for task in self.get_nodes():
            task.set_status(Status.BLOCKED)
