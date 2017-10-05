import math
import copy
import sys
import os
from mylists import Mylists
from num import Numb
from sym import Sym
from row import Row
from csv import CSV
from tbl import Tbl
from superrange import Superrange

import config
the = config

SUPER = Superrange()


class Col:
    def __init__(self, pos, what):
        self.pos, self.what, self.nums, self.n = pos, what, {}, 0


class KeyVal:
    def __init__(self, key, val):
        self.key, self.val = key, val


class Sdtree:
    def __init__(self,t,yfun,pos=0,attr=None,val=None):
        self._t = t
        self._kids = []
        self.yfun = yfun
        self.pos = pos
        self.attr = attr
        self.val = val
        self.stats = Numb.updates(t.rows, yfun)

    def grow1(self, yfun, rows, lvl, b4, pos, attr, val):
        def pad():
            return "%-20s".format("| " * lvl)

        def likeAbove():
            sun = self._t.copy(rows)
            return sun

        if len(rows) >= the.tree_min:
            if lvl <= the.tree_maxDepth:
                here = (lvl == 0) and self or Sdtree(likeAbove(), yfun, pos, attr, val)
                if here.stats.sd < b4:
                    if lvl > 0:
                        self._kids.append(here)

                    cuts = Sdtree.order(here._t, yfun)
                    cut = cuts[0]
                    kids = {}
                    for r in rows:
                        val = r.cells[cut.pos]
                        if val != the.ignore:
                            rows1 = kids.get(val) or []
                            rows1.append(r)
                            kids[val] = rows1
                    for val in sorted(kids.keys()):
                        rows1 = kids[val]
                        if len(rows1) < len(rows):
                            here.grow1(yfun, rows1, lvl + 1, here.stats.sd, cut.pos, cut.what, val)

    @staticmethod
    def order(t, y):
        def xpect(col):
            tmp = 0
            for key in col.nums.keys():
                x = col.nums[key]
                tmp = tmp + x.sd * x.n / col.n
            return tmp

        def whatif(head, y):
            col = Col(head.pos, head.txt)
            for row in t.rows:
                x = row.cells[col.pos]
                if x != the.ignore:
                    col.n = col.n + 1
                    if x not in col.nums.keys():
                        col.nums[x] = Numb()  # TODO
                    col.nums[x].update(y(row))
            return KeyVal(xpect(col), col)

        out = []
        for h in t.x.cols:
            out.append(whatif(h, y))
        out.sort(key=lambda x: x.key)
        return [item.val for item in out]


    @staticmethod
    def grow(t, y):
        # yfun = Tbl.yfun(y)(t) # TODO: Check if this also works
        yfun = Tbl.dom(t)
        root = Sdtree(t, yfun)
        root.grow1(yfun, t.rows, 0, 10**32, None, None, None)
        # above, yfun, rows, lvl, b4, pos, attr, val
        return root

    @staticmethod
    def show(tr, lvl=0):
        def pad():
            return "| "* (lvl-1)
        def left(x):
            return "%-20s"%x

        lvl = lvl or 0
        suffix = ""
        if len(tr._kids) == 0 or lvl == 0:
            suffix = "n=%s mu=%-.2f sd=%-.2f"%(tr.stats.n, tr.stats.mu, tr.stats.sd)
        if lvl == 0:
            print("\n{}".format(suffix))
        else:
            # must_be = left( "{}{} = {}".format(pad(), tr.attr or "", tr.val or ""))
            print(left( "{}{} = {}".format(pad(), str(tr.attr) or "", str(tr.val) or "")), "\t:", suffix)
        for j in range(len(tr._kids)):
            Sdtree.show(tr._kids[j], lvl+1)

    @staticmethod
    def leaf(tr, cells, bins, lvl):
        lvl = lvl or 0
        for j, kid in enumerate(tr._kids):
            pos, val = kid.pos, kid.val
            if cells[kid.pos] == kid.val:
                return Sdtree.leaf(kid, cells, bins, lvl+1)
        return tr


def test(f, y):
    the.tree_min = 10
    y = y or "dom"
    f = f or "auto.csv"

    tb1 = Tbl(f)
    t2 = tb1.discretizeRows(y)

    # for head in t2.x.cols:
    #     if head.bins:
    #         print(len(head.bins), head.txt)

    tr = Sdtree.grow(t2, y)
    # print(tr)
    Sdtree.show(tr)
    # print(t2.spec)

if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     file_name = "../data/" + "auto.csv"#sys.argv[1]
    #     if not os.path.exists(file_name):
    #         print("File {} does not exist in current path\n".format(file_name))
    #     else:
    #         print("File {} exist in current path\n".format(file_name))
    #         test(sys.argv[1], "dom")
    # else:
    #      print("Please enter the .csv file name which is present in /data subfolder")
    test("auto.csv", "dom")
