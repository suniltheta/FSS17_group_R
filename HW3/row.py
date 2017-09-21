import math
import config

from sym import Sym
from num import Numb

the = config


def new_id():
    id = id + 1
    return id

class Row:
    def __init__(self, id):
        self.id = id
        self.cells = []

    def update(self, cells):
        self.cells = cells

    # def create(self):
    #     self.id = new_id()

    def dominate1(self, row, t):
        e, n = 2.71828, len(t.goals)
        sum1, sum2 = 0, 0
        for goal in t.goals:
            w = goal.weight
            x = goal.norm(self.cells[goal.pos])
            y = goal.norm(row.cells[goal.pos])
            sum1 = sum1 - e ** (w * (x - y) / n)
            sum2 = sum2 - e ** (w * (y - x) / n)
        return sum1/n < sum2/n

    def dominate(self, t, f=None):
        f = f or self.dominate1
        tmp = 0
        for row in t.rows:
            if self.id != row.id:
                if f(row, t):
                    tmp = tmp + 1
        return tmp


if __name__ == "__main__":
    row = Row()
