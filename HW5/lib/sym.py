import math

import config
the = config

class Sym:
    def __init__(self, po = 0):
        self.data = []
        self.n = 0
        self.nk = 0
        self.counts = {}
        self.most = 0
        self.mode = ""
        self._ent = None
        self.pos = po
        self.syms = 0
        self.txt = ""
        self.bins = None

    def pos(self, val):
        self.pos = val

    def about(self):
        syms = 0
        for _, __ in enumerate(self.counts):
            syms = syms + 1
        self.syms = syms
        return [[self.pos], [self.txt], [self.n], [self.mode], [self.most], [self.syms]]

    def update(self, x):
        if x != the.ignore:
            self.mode = self.mode or x
            self._ent = None
            self.n = self.n + 1
            self.data.append(x)
            if not self.counts.get(x):
                self.nk = self.nk + 1
                self.counts[x] = 0
            seen = self.counts[x] + 1
            self.counts[x] = seen
            if seen > self.most:
                self.most, self.mode = seen, x

    def updates(self, items):
        for item in items:
            self.update(item)

    def norm(self, x):
        return x

    def distance(self, j, k):
        no = the.ignore
        if j == no and k == no:
            return 0, 0
        elif j == no:
            return 1, 1
        elif k == no:
            return 1, 1
        elif j == k:
            return 0, 1
        return 1, 1

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

    def ent(self):
        if self._ent == None:
            e = 0
            for key in self.counts.keys():
                temp = (self.counts.get(key)/self.n)
                e = e - temp * math.log(temp, 2)
            self._ent = e
        return self._ent


if __name__ == "__main__":
    sym = Sym()