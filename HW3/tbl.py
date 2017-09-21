import math
from num import Numb
from sym import Sym
from row import Row

import config
the = config

class Tbl:
    def __init__(self):
        self.rows = []
        self.spec = {}
        self.goals = []

        self.less = {}
        self.more = {}
        self.name = {}
        self.all = {'nums':{}, 'syms':{}, 'cols':{}} # all columns
        self.x = {'nums':{}, 'syms':{}, 'cols':{}} # independent columns
        self.y = {'nums':{}, 'syms':{}, 'cols':{}} # dependent columns

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
                self.all['syms'][p] = s
                self.all['cols'][p] = s
            elif isinstance(a, Numb):
                n = Numb(p)
                # n.pos(p)
                n.updates(result.get(key))
                self.all['nums'][p] = n
                self.all['cols'][p] = n
                if (key.find("<") > -1) or (key.find(">") > -1):
                    n.weight = b
                    self.goals.append(n)
            p = p + 1


        for l in range(length):
            cells = []
            for key in result.keys():
                cells.append(result.get(key)[l])
            self.add(cells, l)


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

    def get_ret(self):
        return self.ret

if __name__ == "__main__":
    tbl = Tbl()
