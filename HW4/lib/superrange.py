from sym import Sym
from num import Numb
from sample import Sample
from range import Range
import copy
import config
the = config

class _class:
    def __init__(self, most, label):
        self.most = most
        self.label = label

class outclass:
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

class Superrange:
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

    def labels(self, nums):
        out = []
        if type(nums) is dict:
            for key in nums.keys():
                val = _class(nums.get(key), key)
                out.append(val)
            return out
        for i, item in enumerate(nums):
            val = _class(item, i)
            out.append(val)
        return out

    def same(self, _):
        return _

    def sd(self, _):
        return  _.sd

    def ent(self, _):
        return _.ent()

    def below(self, x, y):
        return x * the.tree_ish < y

    def above(self, x, y):
        return x > y * the.tree_ish

    def function(self, things, x, y, nump=None, lessp=None):
        self.nump = nump == None and True or nump
        self.lessp = lessp == None and True or lessp
        better = self.lessp and self.below or self.above
        what = self.nump and Numb() or Sym()
        z = self.nump and self.sd or self.ent
        breaks = {}
        ranges = Range().function(things, x)

        def data(j):
            return ranges[j]._all._all

        def memo(here, stop, _memo, b4=None, inc=None):
            if stop > here:
                inc = 1
            else:
                inc = -1
            if stop != here:
                b4 = copy.deepcopy(memo(here+inc, stop, _memo))
            _memo[here] = what.updates(data(here), y, b4)
            return _memo[here]

        def combine(lo, hi, all, bin, lvl):
            best = z(all)
            lmemo = {}
            rmemo = {}
            memo(hi, lo, lmemo)
            memo(lo, hi, rmemo)
            cut, lbest, rbest = None, None, None

            for j in range(lo, hi):
                l = lmemo[j]
                r = rmemo[j+1]
                tmp = l.n / all.n * z(l) + r.n/all.n*z(r)
                if better(tmp, best):
                    cut = j
                    best = tmp
                    lbest = copy.deepcopy(l)
                    rbest = copy.deepcopy(r)

            if cut:
                bin = combine(lo, cut, lbest, bin, lvl+1) + 1
                bin = combine(cut+1, hi, rbest, bin, lvl+1)
            else:
                if bin not in breaks.keys():
                    breaks[bin] = -10**32
                if ranges[hi].hi > breaks[bin]:
                    breaks[bin] = ranges[hi].hi

            return bin

        combine(1, len(ranges)-1, memo(0, len(ranges)-1, {}), 1, 0)
        return self.labels(breaks)
