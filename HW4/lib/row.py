import math
import config
import copy

from id import ID
from sym import Sym
from num import Numb

the = config

class Row:
    def __init__(self):
        self.id =  id(self) #ID.new()
        self.cells = []

    def update(self, cells, t=False):
        if not t:
            self.cells = cells
            return
        self.cells = copy.deepcopy(cells)
        for head in t.all.cols:
            head.what.update(cells[head.pos])
        return self

    def dominate1(self, row, t):
        e, n = 2.71828, len(t.goals)
        sum1, sum2 = 0, 0
        for goal in t.goals:
            w = goal.weight
            x = goal.norm(self.cells[goal.pos])
            y = goal.norm(row.cells[goal.pos])
            sum1 = sum1 - e ** (w * (x - y) / n)
            sum2 = sum2 - e ** (w * (y - x) / n)
        return sum1/(n + 1e-32) < sum2/(n + 1e-32)

    def dominate(self, t, f=None):
        f = f or self.dominate1
        tmp = 0
        for row in t.rows:
            if self.id != row.id:
                if f(row, t):
                    tmp = tmp + 1
        return tmp

    def __str__(self):
        s=""
        for x in self.cells:
            s = s +", "+ str(x)
        return s


if __name__ == "__main__":
    row = Row()
