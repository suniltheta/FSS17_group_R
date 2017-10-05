import math

import config
the = config

class Numb:
    def __init__(self, pos = 0):
        self.data = []
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        self.hi = -1e32
        self.lo = 1e32
        self.w = 1
        self.pos = pos
        self.weight = 0
        self.txt = ""
        self.bins = None

    def pos(self, val):
        self.pos = val

    def update(self, x):
        if x != the.ignore:
            self.n = self.n + 1
            self.data.append(x)
            if x < self.lo:
                self.lo = x
            if x > self.hi:
                self.hi = x
            delta = x - self.mu
            self.mu = self.mu + delta / self.n
            self.m2 = self.m2 + delta * (x - self.mu)
            if self.n > 1:
                self.sd = (self.m2 / (self.n - 1)) ** 0.5

    def about(self):
        return [[self.pos], [self.txt], [self.n], [self.mu], [self.sd], [self.lo], [self.hi]]

    def updates(self, items, f=None, all=None):
        all = all or Numb()
        def fun(x):
            return x
        f = f or fun
        for item in items:
            all.update(f(item))
        return all

    @staticmethod
    def updates(items, f=None, all=None):
        all = all or Numb()
        def fun(x):
            return x
        f = f or fun
        for item in items:
            all.update(f(item))
        return all

    def discretize(self, x):
        r = None
        if x == the.ignore:
            return x
        if not self.bins:
            return x
        for b in self.bins:
            r = b.label
            if x < b.most:
                break
        return r

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

    @staticmethod
    def hedges(i, j):
        nom = (i.n - 1)*i.sd**2 + (j.n - 1)*j.sd**2
        denom = (i.n - 1) + (j.n - 1)
        sp = math.sqrt(nom/denom)
        g = abs(i.mu - j.mu) / sp
        c = 1 - 3.0 / (4*(i.n + j.n - 2) - 1)
        return g * c > the.num_small

    @staticmethod
    def ttest1(df, first, last, crit):
        if df <= first:
            return crit[first]
        elif df >= last:
            return crit[last]
        else:
            n1 = first
            while n1 < last:
                n2 = n1*2
                if n1 <= df <= n2:
                    old, new = crit[n1], crit[n2]
                    return old + (new - old) * (df - n1)/(n2 - n1)
                n1 = n1*2

    @staticmethod
    def ttest(i, j):
        t = (i.mu - j.mu) / math.sqrt(max(10**-64, i.sd**2/i.n + j.sd**2/j.n ))
        a = i.sd**2/i.n
        b = j.sd**2/j.n
        df = (a + b)**2 / (10**-64 + a**2/(i.n-1) + b**2/(j.n - 1))
        c = Numb.ttest1(df=math.floor( df + 0.5 ), first=the.num_first, last= the.num_last, crit=the.num_criticals[the.num_conf])
        return abs(t) > c

    @staticmethod
    def same(i, j):
        return not (Numb.hedges(i, j) and Numb.ttest(i, j))


if __name__ == "__main__":
    num = Numb()

