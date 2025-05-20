import asyncio

a, b, c, d, e = "A", "B", "C", "D", "E"

async def r():
  await asyncio.sleep(1)
  return a, b


async def s(a, b):
  await asyncio.sleep(1)
  print(a)
  print(b)
  await asyncio.sleep(1)
  return c, d, e


async def t(a):
  await asyncio.sleep(1)
  print(a)


async def u(a, b):
  await asyncio.sleep(1)
  print(a)
  print(b)


async def main():
  a, b = await r()
  c, d, e = await s(a, b)
  await t(c)
  await u(d, e)

if __name__ == '__main__':
  asyncio.run(main())