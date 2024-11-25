
from numerics import *
from graph import *
from task import Status
import csv
from math import *
from datetime import datetime
from models import *
from sortedcontainers import SortedList
import logging


class Processors:

    def __init__(self, nb_processors):
        self.nb_processors = nb_processors
        self.available_processors = nb_processors
        self.time = 0

    # Getters and Setters
    ############################################################

    def get_nb_processors(self):
        return self.nb_processors

    def get_available_processors(self):
        return self.available_processors

    def get_time(self):
        return self.time

    def set_nb_processors(self, value):
        self.nb_processors = value

    def set_available_processors(self, value):
        self.available_processors = value

    def set_time(self, value):
        self.time = value

    # Methods
    ############################################################

    def online_scheduling_algorithm(self, task_graph, allocation_function, alpha, beta,gamma,save_in_logs=False, adjacency=[],
                                    P=P, mu=mu, speedup_model: Model = GeneralModel(), version=0):
        """"
        Given a task graph, this function calculate the time needed to complete every task of the task graph.
        It's the implementation of the algorithm 1 from the paper. Concerning the allocation_function :
        1 : allocate_processor_algo
        2 : allocate_processor_Min_time
        3 : allocate_processor_Min_area
        """

        waiting_queue = set()  # Initialize a waiting queue Q
        process_list = []  # List of the task being processed
        nodes = task_graph.get_nodes()

        for task in nodes:  # Insert all tasks without parents in the waiting queue
            if not task_graph.get_parents(nodes.index(task), adjacency):
                if allocation_function == 1:
                    task.allocate_processor_algo(P, mu, alpha,beta,gamma, speedup_model, version)
                elif allocation_function == 2:
                    task.allocate_processor_Min_time(P, mu, speedup_model)
                elif allocation_function == 3:
                    task.allocate_processor_Min_area(P, mu, speedup_model)
                allocation = task.get_allocation()
                
                task.set_needed_time(task.get_execution_time(task.get_allocation(), speedup_model))
                waiting_queue.add(task)
                task.set_status(Status.PROCESSING)
            
        while waiting_queue or process_list:
            # Cleaning of the processors
            available_tasks = set()
            if process_list:
                task = min(process_list)
                process_list.remove(task)
                task.set_status(Status.PROCESSED)
                self.available_processors += task.get_allocation()
                for child in task_graph.get_children(nodes.index(task), adjacency):
                    if nodes[child].get_status() == Status.BLOCKED:
                        parents = task_graph.get_parents(child, adjacency)
                        available = True
                        for parent in parents:
                            if nodes[parent].get_status() != Status.PROCESSED:
                                available = False
                                break
                        if available:
                            nodes[child].set_status(Status.AVAILABLE)
                            available_tasks.add(nodes[child])

            # Processor allocation
            for task in available_tasks:
                if allocation_function == 1:
                    task.allocate_processor_algo(P, mu, alpha,beta,gamma, speedup_model, version)
                elif allocation_function == 2:
                    task.allocate_processor_Min_time(P, mu, speedup_model)
                elif allocation_function == 3:
                    task.allocate_processor_Min_area(P, mu, speedup_model)
                allocation1 = task.get_allocation()
                
                task.set_needed_time(task.get_execution_time(task.get_allocation(), speedup_model))
                waiting_queue.add(task)
                task.set_status(Status.PROCESSING)

            # List Scheduling
            to_remove = set()
            for task in waiting_queue:
                if self.get_available_processors() >= task.get_allocation():
                    process_list.append(task)
                    to_remove.add(task)
                    task.set_starting_time(self.get_time())
                    self.available_processors -= task.get_allocation()
            for el in to_remove:
                waiting_queue.remove(el)

            # Incrementing time
            if process_list:
                next_task = min(process_list)
                self.time = next_task.get_needed_time() + next_task.get_starting_time()

        # Resetting the status and the clock of the processors
        task_graph.init_status()
        final_time = self.get_time()
        logging.debug("Total Execution time :", self.get_time(), "seconds")
        self.set_time(0)
        return final_time