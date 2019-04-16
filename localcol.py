#!/usr/bin/env python3

from shi1 import Shi1

"""
show the correction of a single perturbation
"""

class Shi(Shi1):
    def __init__(self):
        super().__init__()
        self.s = [0]*5

    def round_callback(self,s):
        print(" ".join([hex(w)[2:].zfill(8) for w in s]))

    def kgen(self, _):
        return 0

    def view(self,x):
        flips = [1,1<<5,1,1<<30,1<<30,1<<30]
        flips += [0]*(80-len(flips))
        expanded = self.expand(self.btow(x))
        expanded = [f^e for f,e in zip(flips,expanded)]
        cv = self.compress(expanded)
        return self.wtob(cv)

if __name__ == "__main__":
    x = bytes.fromhex("00"*64)
    print(Shi().view(x).hex())
