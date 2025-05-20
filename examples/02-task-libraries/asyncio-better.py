import asyncio

a, b, c, d, e = "A", "B", "C", "D", "E"

async def r():
  await asyncio.sleep(1)
  return a, b


async def s(t):
  await asyncio.sleep(1)
  a, b = await t
  print(a)
  print(b)
  await asyncio.sleep(1)
  return c, d, e


async def t(t):
  await asyncio.sleep(1)
  a, _, _ = await t
  print(a)


async def u(t):
  await asyncio.sleep(1)
  _, a, b = await t
  print(a)
  print(b)


async def main():
  t1 = asyncio.create_task(r())
  t2 = asyncio.create_task(s(t1))
  t3 = asyncio.create_task(t(t2))
  t4 = asyncio.create_task(u(t2))
  await asyncio.gather(t3, t4)


if __name__ == '__main__':
  asyncio.run(main())