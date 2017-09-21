import random
from myrandom import Myrandom
from num import Numb
from range import Range
from range import rangefunction
# import range
# from superrange import Superrange
import config

the = config
R = Myrandom()
RANGE = Range()
# SUPER = Superrange()

def x(z):
    return z[0]


def y(z):
    return z[-1]


def klass(z):
    if z < 0.2:
        return 0.2 + 2 * R.r() / 100
    elif z < 0.6:
        return 0.6 + 2 * R.r() / 100
    else:
        return 0.9 + 2 * R.r() / 100


def main():
    t = []
    n = Numb()
    for _ in range(1, 50):
        # w = random.random()
        w = R.r()
        kla = klass(w)
        n.update(kla)
        t.append([w, kla])

    print("{}".format("\nWe have many unsupervised ranges."))
    for j, one in enumerate(rangefunction(t, x)):
        print(" x\t{} [span:{} lo:{} n:{} hi:{}]".format(j, one.span, one.lo, one.n, one.hi))

    print("{}".format("\nWe have fewer supervised ranges."))

    pass


if __name__ == "__main__":
    R.seed(1)
    main()
