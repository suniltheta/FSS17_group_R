from myrandom import Myrandom
import math
import config
the = config
R = Myrandom()


class Sample:

    def __init__(self, most=None):
        self._all = []
        self.n = 0
        self.most = most or the.sample_most

    def update(self, x):
        if x != the.ignore:
            self.n = self.n + 1
            if len(self._all) < self.most:
                self._all.append(x)
            elif R.r() < len(self._all)/(self.n + 1e32):
                self._all[math.floor(R.r() * len(self._all))] = x
        return x
