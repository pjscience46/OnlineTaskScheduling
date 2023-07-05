################################
# Verrecchia Thomas            #
# Summer - 2022                #
# Internship Kansas University #
################################

# All the numerics we are going to use.

from math import *

w_bounds = [50, 4000000]  # float
p_bounds = [100, 800]  # int

# d = alpha/10^r
alpha_d_bounds = [0, 10]  # float
r_d_bounds = [2, 7]  # int

# c = alpha*2^r
alpha_c_bounds = [1, 2]  # float
r_c_bounds = [0, 3]  # int

mu = (3 - sqrt(5)) / 2
P = 1500
n = 500
