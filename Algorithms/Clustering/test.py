from random import choice
from time import time


def run(a, b):
    start = time()
    m = a[:]
    n = b[:]
    stop = time()-start
    start = time()
    m = [i for i in set(a)]
    n = [i for i in set(b)]
    stop1 = time()-start
    print stop, stop1


def ch(c):
    a, b = [], []
    cho = choice(c)
    a.append(cho)
    c.remove(cho)
    cho = choice(c)
    b.append(cho)
    c.remove(cho)
    return a, b


c = range(40)
res = ch(c)
run(res[0], res[1])
