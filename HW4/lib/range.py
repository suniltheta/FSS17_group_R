
from num import Numb
from sample import Sample
import config
the = config

class _class:
    def __init__(self, x, t):
        self.x = x
        self.cohen = the.chop_cohen
        self.m = the.chop_m
        self.size = len(t)
        self.ranges = []
        self.now = None
        self.num = None
        self.hi = -2**63
        self.epsilon = None
        self.enough = None


class Range:
    def __init__(self):
        self._all = Sample()
        self.n = 0
        self.hi = -2**63
        self.lo = 2**63
        self.span = 2**64

    def update(self, one, x):
        if x != the.ignore:
            self._all.update(one)
            self.n = self.n + 1
            if x > self.hi:
                self.hi = x
            if x < self.lo:
                self.lo = x
            self.span = self.hi - self.lo
        return x

    def nextRange(self, i):
        i.now = Range()
        if not i.ranges:
            i.ranges = []
        i.ranges.append(i.now)

    def rangeManager(self, t, x):
        _ = _class(x, t)
        self.nextRange(_)
        numb = Numb()
        _.num = numb.updates(t, _.x)
        _.hi = _.num.hi
        _.enough = _.size ** _.m
        _.epsilon = _.num.sd * _.cohen
        return _

    def function(self, t, xi, last=0):
        def temp(p):
            return p

        x = xi or temp
        t = sorted(t, key=lambda k: k != the.ignore and x(k))
        i = self.rangeManager(t, x)

        for j, one in enumerate(t):
            x1 = x(one)
            if x1 != the.ignore:
                i.now.update(one, x1)
                if j > 0 and x1 > last and i.now.n > i.enough and i.now.span > i.epsilon and i.num.hi - x1> i.epsilon and i.num.n - j > i.enough:
                    self.nextRange(i)
                # i.now.update(one, x1)
                last = x1
        return i.ranges


