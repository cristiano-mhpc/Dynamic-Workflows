import time

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


def main():
  a, b = r()
  c, d, e = s(a, b)
  t(c)
  u(d, e)

if __name__ == '__main__':
  main()