from random import random
import time

def pi(num_points):
    time.sleep(1)
    inside = 0
    for i in range(num_points):
        x, y = random(), random() 
        if x**2 + y**2 < 1:
            inside += 1

    return (inside*4 / num_points)

def mean(a, b, c):
    time.sleep(1)
    return (a + b + c) / 3

# Estimate three values for PI through a Monte Carlo method
a, b, c = pi(10**6), pi(10**6), pi(10**6)

# Compute the mean of the three estimates
mean_pi  = mean(a, b, c)

# Print the results
print("Average: {:.5f}".format(mean_pi))