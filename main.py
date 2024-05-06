# main
import time

from processors import *
from utils import *
from statistics import *
import matplotlib.pyplot as plt
import logging

nb_iterations = 1

start_time = time.process_time_ns()

# Computations for the first version of the processor allocation algorithm (minimizing alpha)

#compute_and_save('regular','Results_mast_p1/Regular/',nb_iterations,version=0)
# compute_and_save('density','Results_p1_dp/Density/',nb_iterations,version=0)
# compute_and_save('Fat','Results_p1_dp/Fat/',nb_iterations,version=0)
# compute_and_save('jump','Results_p1_dp/Jump/',nb_iterations,version=0)
# compute_and_save('n', 'Results_p1_dp/n/', nb_iterations, version=0)
compute_and_save('p', 'Results_p1_dp/P/', nb_iterations, version=0)

# Computations for the second version of the processor allocation algorithm (minimizing beta)

# compute_and_save('regular','Results_p2_dp/Regular/',nb_iterations,version=1)
# compute_and_save('density','Results_p2_dp/Density/',nb_iterations,version=1)
# compute_and_save('Fat','Results_p2_dp/Fat/',nb_iterations,version=1)
# compute_and_save('jump','Results_p2_dp/Jump/',nb_iterations,version=1)
# compute_and_save('n', 'Results_p2_dp/n/', nb_iterations, version=1)
# compute_and_save('p', 'Results_p2_dp/P/', nb_iterations, version=1)

end_time = time.process_time_ns()

print(f"Finished computing in {(end_time-start_time)/(10**9):.3f}s")

# Displaying the results for the first version of the algorithm

#display_results('regular','Results_p1_dp/Regular/')
# display_results('density','Results_p1_dp/Density/')
# display_results('Fat','Results_p1_dp/Fat/')
# display_results('jump','Results_p1_dp/Jump/')
# display_results('n', 'Results_p1_dp/n/')
display_results('p', 'Results_p1_dp/P/')

# Displaying the results for the second version of the algorithm

# display_results('regular','Results_p2_dp/Regular/')
# display_results('density','Results_p2_dp/Density/')
# display_results('Fat','Results_p2_dp/Fat/')
# display_results('jump','Results_p2_dp/Jump/')
# display_results('n', 'Results_p2_dp/n/')
# display_results('p', 'Results_p2_dp/P/')

# To compare the two version of the processor allocation algorithm

#display_multiple_results("V4","V4_p1","Density","Merging_V4_and_V4_p1")
#display_multiple_results("V4","V4_p1","Fat","Merging_V4_and_V4_p1")
#display_multiple_results("V4","V4_p1","Jump","Merging_V4_and_V4_p1")
#display_multiple_results("V4","V4_p1","Regular","Merging_V4_and_V4_p1")
#display_multiple_results("V4", "V4_p1", "n", "Merging_V4_and_V4_p1")
#display_multiple_results("V4", "V4_p1", "p", "Merging_V4_and_V4_p1")

# To compare the two version of the processor allocation algorithm with standard parameters

#display_results_boxplot("p1_dp", "p2_dp", "Results_dp")
