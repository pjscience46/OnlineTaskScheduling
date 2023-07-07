################################
# Verrecchia Thomas            #
# Summer - 2022                #
# Internship Kansas University #
################################

# This class implement our set of processors

from numerics import *
from graph import *
import csv
from math import *
from datetime import datetime
from model import *


class Processors:

    def __init__(self, nb_processors):
        self._nbProcessors = nb_processors
        self._availableProcessors = nb_processors
        self._time = 0

    # Getters and Setters
    ############################################################

    def get_nbProcessors(self):
        return self._nbProcessors

    def get_availableProcessors(self):
        return self._availableProcessors

    def get_time(self):
        return self._time

    def set_nbProcessors(self, value):
        self._nbProcessors = value

    def set_availableProcessors(self, value):
        self._availableProcessors = value

    def set_time(self, value):
        self._time = value

    # Methods
    ############################################################

    def online_scheduling_algorithm(self, task_graph, allocation_function, alpha, save_in_logs=True, adjacency=[],
                                    P_tild=P, mu_tild=mu, speedup_model: Model = GeneralModel(), version=0):
        """"
        Given a task graph, this function calculate the time needed to complete every task of the task graph.
        It's the implementation of the algorithm 1 from the paper. Concerning the allocation_function :
        1 : allocate_processor_algo
        2 : allocate_processor_Min_time
        3 : allocate_processor_Min_area
        """

        print("  ---- Starting ----")
        print("Number of processors :", self.get_nbProcessors())
        if allocation_function == 1:
            print("Allocation algorithm : Paper")
        elif allocation_function == 2:
            print("Allocation algorithm : Min Time")
        elif allocation_function == 3:
            print("Allocation algorithm : Min Area")

        Q = []  # Initialize a waiting queue Q
        B_P = []  # List of the task being processed
        nodes = task_graph.get_nodes()
        new_task_available = False

        if save_in_logs:
            name = "logs/" + datetime.now().strftime("%m_%d_%Y-%H.%M.%S") + ".csv"
            log = open(name, 'w', newline='')
            writer = csv.writer(log)
            writer.writerow(['Time', 'Waiting Queue', 'Processors Queue', 'Number of available processors'])

        for task in nodes:  # Insert all tasks without parents in the waiting queue
            if not task_graph.get_parents(nodes.index(task), adjacency):
                if allocation_function == 1:
                    task.allocate_processor_algo(P_tild, mu_tild, alpha, speedup_model, version)
                elif allocation_function == 2:
                    task.allocate_processor_Min_time(P_tild, mu_tild, speedup_model)
                elif allocation_function == 3:
                    task.allocate_processor_Min_area(P_tild, mu_tild, speedup_model)
                task.set_needed_time(task.get_execution_time(task.get_allocation(), speedup_model))
                Q += [task]
                task.set_status(2)

        while Q != [] or B_P != []:

            # Cleaning of the processors
            for task in B_P:
                if self.get_time() - task.get_starting_time() >= task.get_needed_time():
                    del B_P[B_P.index(task)]
                    task.set_status(3)
                    for task_offspring in task_graph.get_offsprings(nodes.index(task), adjacency):
                        if nodes[task_offspring].get_status() == 0:
                            parents = task_graph.get_parents(task_offspring, adjacency)
                            available = True
                            for parent in parents:
                                if nodes[parent].get_status() != 3:
                                    available = False
                            if available:
                                nodes[task_offspring].set_status(1)
                    self.set_availableProcessors(self.get_availableProcessors() + task.get_allocation())
                    new_task_available = True

            # Processor allocation
            if self.get_time() == 0 or new_task_available:
                new_task_available = False
                for task in nodes:
                    if task.get_status() == 1:
                        if allocation_function == 1:
                            task.allocate_processor_algo(P_tild, mu_tild, alpha, speedup_model, version)
                        elif allocation_function == 2:
                            task.allocate_processor_Min_time(P_tild, mu_tild, speedup_model)
                        elif allocation_function == 3:
                            task.allocate_processor_Min_area(P_tild, mu_tild, speedup_model)
                        task.set_needed_time(task.get_execution_time(task.get_allocation(), speedup_model))
                        Q += [task]
                        task.set_status(2)

            # Writing the status in the log
            if save_in_logs:
                line = [self.get_time(), [nodes.index(task) for task in Q], [nodes.index(task) for task in B_P],
                        self.get_availableProcessors()]
                writer.writerow(line)

            # List Scheduling
            for i in range(2):  # When we only look at the list Q one time it doesn't get every element ?????
                for task in Q:
                    if self.get_availableProcessors() >= task.get_allocation():
                        B_P += [task]
                        del Q[Q.index(task)]
                        task.set_starting_time(self.get_time())
                        self.set_availableProcessors(self.get_availableProcessors() - task.get_allocation())

            # Incrementing time
            minimum_time_left = float('inf')
            for task in B_P:
                time_left = ceil(task.get_needed_time() - (self.get_time() - task.get_starting_time()))
                if time_left < minimum_time_left:
                    minimum_time_left = time_left
            if minimum_time_left != float('inf'):
                self.set_time(self.get_time() + minimum_time_left)

        if save_in_logs:
            log.close()

        # Resetting the status and the clock of the processors
        task_graph.init_status()
        final_time = self.get_time()
        print("Total Execution time :", self.get_time(), "seconds")
        self.set_time(0)
        return final_time
