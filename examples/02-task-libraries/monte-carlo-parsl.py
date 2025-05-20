import parsl
import time

from parsl.app.app import python_app
from parsl.config import Config
from parsl.executors.threads import ThreadPoolExecutor
from random import random

@python_app
def pi(num_points):
    time.sleep(3)
    inside = 0
    for i in range(num_points):
        x, y = random(), random() 
        if x**2 + y**2 < 1:
            inside += 1

    return (inside*4 / num_points)

@python_app
def mean(a, b, c):
    time.sleep(3)
    return (a + b + c) / 3

# Load Parsl config
local_threads = Config(
    executors=[
        ThreadPoolExecutor(
            max_threads=3,
            label='local_threads'
        )
    ]
)
parsl.load(local_threads)
start_time = time.time_ns()

# Estimate three values for PI through a Monte Carlo method
a, b, c = pi(10**6), pi(10**6), pi(10**6)

# Compute the mean of the three estimates
mean_pi  = mean(a, b, c)

# Print the results
print("Average: {:.5f}".format(mean_pi.result()))
print("Execution time (without Parsl initialization): "
      f"{(time.time_ns() - start_time) / (10**9)}")