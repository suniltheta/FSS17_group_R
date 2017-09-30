import re
import config
the = config

notsep = "{}{}{}".format("([^", the.sep, "]+)")
dull = "['\"\t\n\r]*"
padding = "%s*(.-)%s*"
comments = "#.*"


class WME:
    def __init__(self, fn):
        self.fn = fn
        self.first = True
        self.use = {}


class CSV:
    def __init__(self, src, function):
        self.withEachLine(src, WME(function))

    def incomplete(self, txt):
        return txt[-1] == the.sep

    def ignored(self, txt):
        return txt.find(the.ignore) < 0

    files = {"csv": True, "txt": True}

    def cellsWeAreNotIgnoring(self, txt, wme):
        out, col = [], 0
        p = re.compile(notsep)
        for val in p.finditer(txt):
            word = txt[val.span()[0]:val.span()[1]]
            col = col + 1
            if wme.first:
                wme.use[col] = self.ignored(word)
            if wme.use[col]:
                try:
                    out.append(float(word))
                except ValueError:
                    if word == the.ignore:
                        return False
                    out.append(word)
        return out


    def withOneLine(self, txt, wme):
        txt = txt.replace(padding,"%1").replace(dull,"").replace(comments,"")
        if len(txt) > 0:
            out = self.cellsWeAreNotIgnoring(txt, wme)
            if out:
                wme.fn(out)

    def withEachLine(self, src, wme):
        self.cache = []
        def line1(line):
            self.cache.append(line)
            if not self.incomplete(line):
                self.cache = self.withOneLine("".join(self.cache), wme)
                self.cache = []
                wme.first = False

        if self.files[src[-3:]]:
            file_name = the.data + src
            import os
            if not os.path.exists(file_name):
                print("File {} does not exist in current path\n".format(file_name))
                return
            for line in open(file_name):
                line1(line)
        else:
            for line in src.split("[^\r\n]+"):
                line1(line)


if __name__ == "__main__":
    CSV("auto.csv", print)