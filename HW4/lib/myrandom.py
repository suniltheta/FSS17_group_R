import random
import math

class Myrandom:
    def __init__(self):
        self.seed0 = 10013
        self._seed = self.seed0
        self.multipler = 16807.0
        self.modulus = 2147483647.0
        self.randomtable = None

    def park_miller_randomizer(self):
        self._seed = (self.multipler * self._seed) % self.modulus
        return self._seed / self.modulus

    def rseed(self, n):
        if n:
            self._seed = n
        else:
            self._seed = self.seed0
        self.randomtable = None

    def system(self):
        self.rseed(random.random() * self.modulus)

    def another(self):
        if self.randomtable == None:
            self.randomtable = {}
            for i in range(1, 97):
                self.randomtable[i] = self.park_miller_randomizer()
        x = self.park_miller_randomizer()
        i = 1 + math.floor(97 * x)
        x, self.randomtable[i] = self.randomtable[i], x
        return x

    def r(self):
        return self.another()

    def seed(self, n):
        return self.rseed(n)

