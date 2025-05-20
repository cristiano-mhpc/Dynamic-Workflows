import asyncio
import time

from random import random


async def pi(num_points):
    time.sleep(1)
    inside = 0
    for i in range(num_points):
        x, y = random(), random() 
        if x**2 + y**2 < 1:
            inside += 1

    return (inside*4 / num_points)

async def mean(a, b, c):
    time.sleep(1)
    return await asyncio.gather(a + b + c) / 3

async def main ():
    # Estimate three values for PI through a Monte Carlo method
    a = asyncio.create_task(pi(10**6))
    b = asyncio.create_task(pi(10**6))
    c = asyncio.create_task(pi(10**6))

    # Compute the mean of the three estimates
    mean_pi  = asyncio.create_task(mean(a, b, c))

    # Print the results
    print("Average: {:.5f}".format(await mean_pi))

if __name__ == '__main__':
    asyncio.run(main())