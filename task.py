################################
# Verrecchia Thomas            #
# Summer - 2022                #
# Internship Kansas University #
################################

# A class implementing the concept of a Task. A Task has certain parameters (w,p,d,c) and can be assigned with the
# number of processors that will be used to complete this task.

from math import *
from model import Model
from enum import Enum


class Status(Enum):
    BLOCKED = 0
    AVAILABLE = 1
    PROCESSING = 2
    PROCESSED = 3


class Task:

    def __init__(self, w, p, d, c, status: Status = Status.BLOCKED, allocation=None, needed_time=None, starting_time=None, ):
        """
        :param w: The total parallelizable work of the task
        :param p: The maximum degree of parallelism of the task
        :param d: The sequential work of the task
        :param c: The communication overhead
        :param status: Can take the values 0 (non available), 1 (available), 2 (in the queue or being processed),
                       3 (processed).
        :param allocation: If None, the algorithm "allocate_processor" has not been run yet, else it's the number
                           of processor needed for the completion of the task.
        :param needed_time: The time needed by the task to be processed ( it depends on the allocation)
        :param starting_time: The time when the task start being processed.
        """
        self._w = w
        self._p = p
        self._d = d
        self._c = c
        self._status: Status = status
        self._allocation = allocation
        self._needed_time = needed_time
        self._starting_time = starting_time

    ## Getters and Setters
    ############################################################

    def get_w(self):
        return self._w

    def get_p(self):
        return self._p

    def get_d(self):
        return self._d

    def get_c(self):
        return self._c

    def get_status(self) -> Status:
        return self._status

    def get_allocation(self):
        return self._allocation

    def get_needed_time(self):
        return self._needed_time

    def get_starting_time(self):
        return self._starting_time

    def set_w(self, value):
        self._w = value

    def set_p(self, value):
        if value == 0:
            raise ValueError("p must be different from 0")
        self._p = value

    def set_d(self, value):
        self._d = value

    def set_c(self, value):
        self._c = value

    def set_status(self, value: Status):
        self._status = value

    def set_allocation(self, value):
        if value >= 1:
           self._allocation = value
               

    def set_needed_time(self, value):
        self._needed_time = value

    def set_starting_time(self, value):
        self._starting_time = value

    ## Methods
    ############################################################

    def __lt__(self, other):
        if self.get_needed_time() is None:
            return False
        if other.get_needed_time() is None:
            return True
        return self.get_needed_time() + self.get_starting_time() < other.get_needed_time() + other.get_starting_time()

    def get_execution_time(self, nb_processors, speedup_model: Model):
        """
        Return the execution time for a given task,speedup model ( Amdahl, Communication, General, Roofline ).
        """
        if self.get_p() == 0:
            raise ValueError("p must be different from 0")
       
        if nb_processors < 1:
            raise ValueError("The number of processors must be superior to 1")
        return speedup_model.time(self, nb_processors) 

    def get_area(self, number_of_processors, speedup_model: Model):
        """Return the area of a task depending on the number of processor allocated and the speedup model"""
        return self.get_execution_time(number_of_processors, speedup_model) * number_of_processors

    def get_p_max(self, P, speedup_model: Model):
        """"Allocating more than p_max processors to the task will no longer decrease its execution time"""
        return speedup_model.p_max(self, P)

    def allocate_processor_algo(self, P, mu_tild, alpha,Beta1, speedup_model: Model,version):
        """
        Return the number of processors needed to compute a given task. It's the implementation of the algorithm 2
        from the paper.

        - version = 0 : thm.e first version of the algorithm.
        - version = 1 : the second version of the algorith


        """

        # Step 1 : Initial Allocation
        w = self.get_w()
        p = self.get_p()
        d = self.get_d()
        c = self.get_c()

        # p_max = self.get_p_max(P, speedup_model)
        # t_min = self.get_minimum_execution_time(p_max, speedup_model)
        # a_min = self.get_minimum_area(1, speedup_model)#execution_time * p = a
       
        
        # Alpha_min = inf
        # final_nb_processors = -1
        # Upper_range = ceil(mu_tild * P)
        # for i in range(1, p_max  + 1):
        #     Alpha = self.get_area(i, speedup_model) / a_min[0]
        #     Beta = self.get_execution_time(i, speedup_model) / t_min[0]

        #     if Beta < (1 - 2 * mu_tild) / (mu_tild * (1 - mu_tild)):
        #         if Alpha < Alpha_min:
        #             Alpha_min = Alpha
        #             final_nb_processors = i 

        p_max = self.get_p_max(P, speedup_model)
        t_min = self.get_execution_time(p_max, speedup_model)
        a_min = self.get_execution_time(1, speedup_model)

        if version == 0:
            Alpha_min = inf
            final_nb_processors = -1
            upper_range = ceil(mu_tild * P)
            for i in range(1, upper_range + 1):
                AR = self.get_area(i, speedup_model) / a_min
                TR = self.get_execution_time(i, speedup_model) / t_min
                
                if AR >=1 and AR <= Beta1:
                    if TR < Alpha_min:
                        Alpha_min = TR
                        final_nb_processors = i                         
        
        self.set_allocation(final_nb_processors)
        
        
        

    def get_minimum_execution_time(self, P, speedup_model: Model):
        """Return the minimum execution time"""
        t_min = inf
        p_min = -1
        for p in range(1, self.get_p_max(P, speedup_model) + 1):
            execution_time = self.get_execution_time(p, speedup_model)
            if execution_time < t_min:
                t_min = execution_time
                p_min = p
        return [t_min, p_min]

    def get_minimum_area(self, P, speedup_model: Model):
        """Return the minimum area ( Processors needed x execution times )"""
        area_min = 100000000000
        p_min = -1
        for p in range(1, self.get_p_max(P, speedup_model) + 1):
            execution_time = self.get_execution_time(p, speedup_model)
            if execution_time * p < area_min:
                area_min = execution_time * p
                p_min = p
        return [area_min, p_min]

    def allocate_processor_Min_time(self, P, mu, speedup_model: Model):
        """Allocate the processor to minimize the execution time of the task"""
        self.set_allocation(self.get_minimum_execution_time(P, speedup_model)[1])

    def allocate_processor_Min_area(self, P, mu, speedup_model: Model):
        """Allocate the processor to minimize the area of the task"""
        self.set_allocation(self.get_minimum_area(P, speedup_model)[1])
