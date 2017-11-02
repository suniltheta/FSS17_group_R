import math
import copy
import sys
import os
import random
import config
from mylists import Mylists
from num import Numb
from sym import Sym
from row import Row
from csv import CSV
from tbl import Tbl
from sdtree import Sdtree
from superrange import Superrange

the = config
SUPER = Superrange()


def more(x, y):
    return x > y

def less(x, y):
    return x < y

class AttrVal:
    def __init__(self, attr=None, val=None, _stats=None, has=None):
        self.attr = attr
        self.val = val
        self._stats = _stats
        self.has = has

    def __str__(self):
        sun = "\"Attr: {} val: {}\"".format(self.attr, self.val)
        return sun

    def __repr__(self):
        return str(self)


class OutContrast:
    def __init__(self, i, j, ninc, muinc, inc, branch1, mu1, branch2, mu2):
        self.i, self.j, self.ninc, self.muinc, self.inc, self.branch1, self.mu1, self.branch2, self.mu2 = \
            i, j, ninc, muinc, inc, branch1, mu1, branch2, mu2

    def __str__(self):
        return ""
        pass
        # return "dont know what to return" #TODO: After fall break

    def __repr__(self):
        return str(self)


class CON:
    @staticmethod
    def has(branch):
        out = []
        for step in branch:
            out.append(AttrVal(attr=step.attr, val=step.val))
        return out

    @staticmethod
    def have(branches):
        for branch in branches:
            pass
            # branch.has = CON.has(branch)
        return branches

    @staticmethod
    def branches1(tr,out,b):
        if tr.attr:
            b.append(AttrVal(attr=tr.attr, val=tr.val, _stats=tr.stats))
        if len(b) > 0:
            out.append(b)
        for kid in tr._kids:
            CON.branches1(kid, out, copy.deepcopy(b))
        return out

    @staticmethod
    def branches(tr):
        return CON.have(CON.branches1(tr,[],[]))

    @staticmethod
    def member2(twin0, twins):
        for twin1 in twins:
            if twin0.attr == twin1.attr:
                twin0.val = twin1.val
                return True
        return False

    @staticmethod
    def delta(t1, t2):
        out = []
        for twin in t1:
            if not CON.member2(twin, t2):
                out.append(AttrVal(attr=twin.attr, val=twin.val))
        return out

    @staticmethod
    def contrasts(branches, better):
        for i, branch1 in enumerate(branches):
            out = []
            for j, branch2 in enumerate(branches):
                if i != j:
                    num1 = (Mylists.last(branch1))._stats
                    num2 = (Mylists.last(branch2))._stats
                    if better(num2.mu, num1.mu):
                        if not Numb.same(num1, num2):
                            inc = CON.delta(branch2, branch1)
                            if len(inc) > 0:
                                out.append(OutContrast(i=i, j=j, ninc=len(inc), muinc=num2.mu - num1.mu,
                                                       inc=inc, branch1=branch1, mu1=num1.mu,
                                                       branch2=branch2, mu2=num2.mu))
                            # inc = CON.delta(branch2.has, branch1.has)
                            # if len(inc) > 0:
                            #     out.append(OutContrast(i=i, j=j, ninc=len(inc),muinc=num2.mu - num1.mu,
                            #                             inc=inc, branch1=branch1.has, mu1=num1.mu,
                            #                             branch2=branch2.has, mu2=num2.mu))
            # print("")
            if len(out) > 0:
                out.sort(key=lambda x: x.muinc, reverse=True)
                print(i, "max mu", out[0])
            if len(out) > 0:
                out.sort(key=lambda x: x.ninc)
                print(i, "min inc", out[0])

    @staticmethod
    def plans(branches):
        return CON.contrasts(branches, more)

    @staticmethod
    def monitors(branches):
        return CON.contrasts(branches, less)
    
    @staticmethod
    def generateContrast(x, branches):
        if len(x._kids) == 0:
            branches.append(x)
            return
        else:
            for k in x._kids:
                CON.generateContrast(k, branches)

    @staticmethod
    def contrastBranches(branches):
        c = 0
        random.shuffle(branches)
        plans = []
        monitors = []
        for i, branch1 in enumerate(branches):
            out = []
            for j, branch2 in enumerate(branches[i+1:]):
                if i != j:
                    c = c + 1
                    if branch1.stats.mu == branch2.stats.mu:
                        print("{}.\t{}={} , {}={} are equal".format(c, branch1.attr, branch1.val, branch2.attr, branch2.val))
                    elif branch1.stats.mu > branch2.stats.mu:
                        # print("{}.\t{}={} , {}={} is a plan".format(c, branch1.attr, branch1.val, branch2.attr, branch2.val))
                        plans.append("{}={} , {}={}".format(branch1.attr, branch1.val, branch2.attr, branch2.val))
                    else:
                        # print("{}.\t{}={} , {}={} is a monitor".format(c, branch1.attr, branch1.val, branch2.attr, branch2.val))
                        monitors.append("{}={} , {}={}".format(branch1.attr, branch1.val, branch2.attr,
                                                                             branch2.val))

        print("\n==================== What to do: (plans= here to better) ")
        for i, plan in enumerate(plans):
            print("{}.\t{}".format(i, plan))

        print("\n==================== What to fear: (monitors = here to worse) ")
        for i, monitor in enumerate(monitors):
            print("{}.\t{}".format(i, monitor))



def test(f, y):
    the.tree_min = 8
    y = y or "dom"
    f = f or "auto.csv"
    x = Sdtree.grow(Tbl(f).discretizeRows(y), "dom")
    Sdtree.show(x)
    branches = []
    CON.generateContrast(x, branches)
    print("\n==================== Show branches \n\n")
    CON.contrastBranches(branches)

    # b = CON.branches(x)
    # print("\n==================== Show branches \n\n")
    # for j, val in enumerate(b):
    #     print(j, [x for x in val])
        # print(j, [str(x) for x in val])
    # print("\n==================== What to do: (plans= here to better) ")
    # CON.plans(b)
    # print("\n==================== What to fear: (monitors = here to worse) ")
    # CON.monitors(b)

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
