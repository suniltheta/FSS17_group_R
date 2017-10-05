import math
import copy
from mylists import Mylists
from num import Numb
from sym import Sym
from row import Row
from csv import CSV
from superrange import Superrange

import config
the = config
SUPER = Superrange()

class num_sym_col:
    def __init__(self):
        self.nums = []
        self.syms = []
        self.cols = []

class when_what_weight_where:
    def __init__(self, when, what, weight, where):
        self.when = when
        self.what = what
        self.weight = weight
        self.where = where


class Tbl:
    def __init__(self, file=False):
        self.rows = []
        self.spec = []
        self.goals = []

        self.less = []
        self.more = []
        self.name = {}
        # self.all = {'nums': {}, 'syms': {}, 'cols': {}}  # all columns
        self.all = num_sym_col()
        # self.x = {'nums': {}, 'syms': {}, 'cols': {}}  # independent columns
        self.x = num_sym_col()
        # self.y = {'nums': {}, 'syms': {}, 'cols': {}}  # dependent columns
        self.y = num_sym_col()

        if file:
            self.fromCSV(file)

    def categorize(self, text):
        spec = [
            {'when': "$", 'what': Numb(), 'weight': 1},
             # 'where': {self.all.get('cols'), self.x.get('cols'), self.all.get('nums'), self.x.get('nums')}},
            {'when': "%", 'what': Numb(), 'weight': 1},
             # 'where': {self.all.get('cols'), self.x.get('cols'), self.all.get('nums'), self.x.get('nums')}},
            {'when': "<", 'what': Numb(), 'weight': -1},
             # 'where': {self.all.get('cols'), self.y.get('cols'), self.all.get('nums'), self.goals, self.less, self.y.get('nums')}},
            {'when': ">", 'what': Numb(), 'weight': 1},
             # 'where': {self.all.get('cols'), self.y.get('cols'), self.all.get('nums'), self.goals, self.more, self.y.get('nums')}},
            {'when': "!", 'what': Sym(), 'weight': 1},
             # 'where': {self.all.get('cols'), self.y.get('syms'), self.y.get('cols'), self.all.get('syms')}},
            {'when': "", 'what': Sym(), 'weight': 1}
             # 'where': {self.all.get('cols'), self.x.get('cols'), self.all.get('syms'), self.x.get('syms')}},
        ]

        for want in spec:
            if text.find(want.get('when')) > -1:
                return want.get('what'), want.get('weight')#, want.get('where')

    def categories(self, txt):
        spec = [
            when_what_weight_where("$",    Numb(),     1,   [self.all.cols, self.x.cols, self.all.nums, self.x.nums]),
            when_what_weight_where("%",    Numb(),     1,   [self.all.cols, self.x.cols, self.all.nums, self.x.nums]),
            when_what_weight_where("<",     Numb(),    -1,  [self.all.cols, self.y.cols, self.all.nums, self.goals, self.less, self.y.nums]),
            when_what_weight_where(">",     Numb(),     1,  [self.all.cols, self.y.cols, self.all.nums, self.goals, self.more, self.y.nums]),
            when_what_weight_where("!",     Sym(),      1,  [self.all.cols, self.y.syms, self.y.cols,   self.all.syms]),
            when_what_weight_where("",      Sym(),      1,  [self.all.cols, self.x.cols, self.all.syms, self.x.syms])
            # {'when': "$", 'what': Numb(), 'weight': 1},
            # # 'where': {self.all.get('cols'), self.x.get('cols'), self.all.get('nums'), self.x.get('nums')}},
            # {'when': "%", 'what': Numb(), 'weight': 1},
            # # 'where': {self.all.get('cols'), self.x.get('cols'), self.all.get('nums'), self.x.get('nums')}},
            # {'when': "<", 'what': Numb(), 'weight': -1},
            # # 'where': {self.all.get('cols'), self.y.get('cols'), self.all.get('nums'), self.goals, self.less, self.y.get('nums')}},
            # {'when': ">", 'what': Numb(), 'weight': 1},
            # # 'where': {self.all.get('cols'), self.y.get('cols'), self.all.get('nums'), self.goals, self.more, self.y.get('nums')}},
            # {'when': "!", 'what': Sym(), 'weight': 1},
            # # 'where': {self.all.get('cols'), self.y.get('syms'), self.y.get('cols'), self.all.get('syms')}},
            # {'when': "", 'what': Sym(), 'weight': 1}
            # # 'where': {self.all.get('cols'), self.x.get('cols'), self.all.get('syms'), self.x.get('syms')}},
        ]
        for want in spec:
            if txt.find(want.when) > -1:
                return want.what, want.weight, want.where

    def consume(self, result):
        p = 0
        length = 5
        for key in result.keys():
            if p == 0:
                length = len(result.get(key))
            a, b= self.categorize(key)
            if isinstance(a, Sym):
                s= Sym(p)
                s.updates(result.get(key))
                # s.pos(p)
                self.all.syms[p] = s
                self.all.cols[p] = s
            elif isinstance(a, Numb):
                n = Numb(p)
                # n.pos(p)
                n.updates(result.get(key))
                self.all.nums[p] = n
                self.all.cols[p] = n
                if (key.find("<") > -1) or (key.find(">") > -1):
                    n.weight = b
                    self.goals.append(n)
            p = p + 1


        for l in range(length):
            cells = []
            for key in result.keys():
                cells.append(result.get(key)[l])
            self.add(cells, l)

    def header(self, cells):
        self.spec = cells
        for col, cell in enumerate(cells):
            what, weight, wheres = self.categories(cell)
            one = what
            one.pos = col
            one.txt = cell
            one.what = what
            one.weight = weight
            self.name[one.txt] = one
            for _, where in enumerate(wheres):
                where.append(one)
        return self

    def data(self, cells, old=False):
        new = Row().update(cells, self)
        self.rows.append(new)
        if old:
            new.id = old.id
        return new

    def update(self, cells):
        if len(self.spec) == 0:
            return self.header(cells)
        else:
            return self.data(cells)

    def add(self, cells, id):
        row = Row(id)
        row.update(cells)
        self.rows.append(row)

    def calculate_dom(self):
        self.b4 = {}
        self.ret = []
        for row in self.rows:
            if not self.b4.get(row.id):
                dom_val = row.dominate(self)
                self.b4[row.id] = {
                    'dom_val':dom_val,
                    'val':row
                }
                self.ret.append(self.b4[row.id])

    def copy(self, _from):
        j = Tbl()
        j.header(copy.deepcopy(self.spec))
        for r in _from:
            j.data(copy.deepcopy(r.cells), r)
        # if _from == "full":
        #     print(" ********** SUNIL ********** ")
        #     pass
        # elif type(_from) is int or type(_from) is float: # TODO: Check if type coming is number
        #     print(" ********** SUNIL ********** ")
        #     pass
        # elif type(_from) is type(Tbl()):
        #     for r in _from:
        #         j.data(copy.deepcopy(r.cells), r)

        return j

    def show(self):
        def worker(t):
            if len(t) > 0:
                print("")
                rows = []
                rows.append(None)
                cols = []
                for _, head in enumerate(t):
                    about = head.what.about()
                    row, col = [], []
                    for i in range(len(about)):
                        for col, val in enumerate(about[i]):
                            cols.append(col)
                            row.append(val)
                    rows[0] = cols
                    rows.append(row)
            Mylists.mprint(rows," |  ")
        worker(self.all.syms)
        worker(self.all.nums)

    # def dom(self):
    #     b4 = []
    #     def ffun(r):
    #         if not b4[r.id]:
    #             b4[r.id] = r.dominate(self)
    #         return b4[r.id]
    #     return lambda r: ffun(r)

    @staticmethod
    def dom(t):
        b4 = {}
        def ffun(r):
            if not b4.get(r.id):
                b4[r.id] = r.dominate(t)
            return b4[r.id]
        return lambda r: ffun(r)

    @staticmethod
    def yfun(y):
        # TODO: Add other goal function returns below and corresponding function before this method
        if y == 'dom':
            return lambda t: Tbl.dom(t)


    def funs(self, y):
        # Depending on y value do "local funs={goaln=goaln, goal1=goal1,dom=dom,goallast=goallast}"
        return self.dom(self)

    def discretizeHeaders(self, spec):
        out = []
        if spec:
            for _, val in enumerate(spec):
                out.append(val.replace("$",""))
        return out

    def discretizeRows(self, y):
        j = Tbl().header(self.discretizeHeaders(self.spec))
        yfun = Tbl.dom(self)
        for head in self.x.nums:
            cooked = j.all.cols[head.pos]
            x = lambda r: r.cells[cooked.pos]
            cooked.bins = SUPER.function(self.rows, x, yfun)
            # for key, value in enumerate(cooked.bins):
            #     print(" Super {}\t{} [label={} most={} ]".format(cooked.txt, key, value.label, value.most))

        for r in self.rows:
            tmp = copy.deepcopy(r.cells)
            for head in self.x.nums:
                cooked = j.all.cols[head.pos]
                old = tmp[cooked.pos]
                new = cooked.discretize(old)
                tmp[cooked.pos] = new
            j.data(tmp, r)
        return j


    def fromCSV(self, f):
        CSV(f, lambda cells: self.update(cells))
        return self

    def get_ret(self):
        return self.ret

if __name__ == "__main__":
    # tbl = Tbl()
    tb1 = Tbl("auto.csv")
    # tb1.show()
