import math

import config
the = config

class Numb:
    def __init__(self, po = 0):
        self.data = []
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        self.hi = 1e32
        self.lo = -1e32
        self.w = 1
        self.pos = po
        self.weight = 0

    def pos(self, val):
        self.pos = val

    def update(self, x):
        if x != the.ignore:
            self.n = self.n + 1
            if x < self.lo:
                self.lo = x
            if x > self.hi:
                self.hi = x
            delta = x - self.mu
            self.mu = self.mu + delta / self.n
            self.m2 = self.m2 + delta * (x - self.mu)
            if self.n > 1:
                self.sd = (self.m2 / (self.n - 1)) ** 0.5

    def updates(self, items):
        for item in items:
            self.update(item)

    def norm(self, x):
        if x == the.ignore:
            return x
        return (x - self.lo) / (self.hi - self.lo + 1e-32)

    def distance(self, j, k):
        if j == the.ignore and k == the.ignore:
            return 0,0
        elif j == the.ignore:
            k = self.norm(k)
            j =  k < 0.5 and 1 or 0
        elif k == the.ignore:
            j = self.norm(j)
            k = j < 0.5 and 1 or 0
        else:
            j,k = self.norm(j), self.norm(k)
        return (abs(j-k))**2, 1


if __name__ == "__main__":
    num = Numb()

