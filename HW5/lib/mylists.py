from myrandom import Myrandom

class Mylists:
    def __init__(self):
        self.R = Myrandom()

    def member(self, x, t):
        if type(t) is list:
            for item in t:
                if x == item:
                    return True
            return False
        elif type(t) is dict:
            for key in t.keys():
                if x == t.get(key):
                    return True
            return False
        else:
            return False

    def first(self, x):
        if type(x) is list and len(x) > 0:
            return x[0]
        else:
            return None

    def last(self, x):
        if type(x) is list and len(x) > 0:
            return x[-1]
        else:
            return None

    @staticmethod
    def mprint(ts, sep):
        sep = sep or ", "
        fmt, w = {}, {}
        def width(col, x):
            if not w.get(col):
                w[col] = 0
            tmp = len(str(x))
            if tmp > w.get(col):
                w[col] = tmp
                fmt[col] = "{}{}{}".format("%", tmp, "s")

        for _, t in enumerate(ts):
            for col, x in enumerate(t):
                width(col, x)

        for i, t in enumerate(ts):
            # TODO: currently printing, in future write to a file
            def dic_to_list(dic):
                out = []
                for key in dic.keys():
                    out.append(dic.get(key))
                return out
            print(str.format("".format(sep.join(dic_to_list(fmt)),"\n"), *t))
