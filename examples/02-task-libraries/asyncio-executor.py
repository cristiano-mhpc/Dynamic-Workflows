import asyncio
import time

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

a, b, c, d, e = "A", "B", "C", "D", "E"

def r():
  time.sleep(1)
  return a, b


def s(a, b):
  time.sleep(1)
  print(a)
  print(b)
  time.sleep(1)
  return c, d, e


def t(a):
  time.sleep(1)
  print(a)


def u(a, b):
  time.sleep(1)
  print(a)
  print(b)


async def main():
  loop = asyncio.get_event_loop()
  with ThreadPoolExecutor(max_workers=2) as executor:
  # with ProcessPoolExecutor(max_workers=2) as executor:
    a, b = await loop.run_in_executor(executor, r)
    c, d, e = await loop.run_in_executor(executor, s, a, b)
    await asyncio.gather(
      loop.run_in_executor(executor, t, c),
      loop.run_in_executor(executor, u, d, e)
    )


if __name__ == '__main__':
  asyncio.run(main())