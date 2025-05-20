import ray
import time

from random import random

@ray.remote
def pi(num_points):
    inside = 0
    time.sleep(1)
    for i in range(num_points):
        x, y = random(), random() 
        if x**2 + y**2 < 1:
            inside += 1
    return (inside*4 / num_points)

@ray.remote
def mean(a, b, c):
    time.sleep(1)
    return (a + b + c) / 3

# Initialise Ray
ray.init()
start_time = time.time_ns()

# Estimate three values for PI through a Monte Carlo method
a = pi.remote(10**6)
b = pi.remote(10**6)
c = pi.remote(10**6)

# Compute the mean of the three estimates
mean_pi  = mean.remote(a, b, c)

# Print the results
print("Average: {:.5f}".format(ray.get(mean_pi)))
print("Execution time (without Ray initialization): "
      f"{(time.time_ns() - start_time) / (10**9)}")