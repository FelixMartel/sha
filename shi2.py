#!/usr/bin/env python3

from shi1 import Shi1
from os import urandom
from math import log

"""
was found after 2^19, other runs yielded nothing after 2^22

1552fd4468f64f3e2a4bff705620474fd210502140241cd8971dc426960402bf5e05025cfe967542bedfc71a069cf6e79fead70c8b5c0ce24f06dc7c9b95255f
hashes to 935ea55064a88fb505d2c0d330e1a679b4c7d555
1552fd4468f64f3e2a4bff725620470fd2105023c0241cd8171dc424160402ff5e05025e7e9675423edfc71a869cf6e79fead70c8b5c0ce24f06dc7e9b95251f
hashes to 935ea55064a88fb505d2c0d330e1a679b4c7d555
"""

class Shi2(Shi1):
    def __init__(self):
        super().__init__()

    def round_callback(self,s):
        pass

    def fgen(self,i):
        # restore IF and MAJ
        return super(Shi1,self).fgen(i)

    def fullcol(self):
        # dif mask from paper
        pert = [0,0,2,0,0,0,2,0,0,0,0,0,0,0,2,0]
        flips = self.preimage(self.correct(self.expand(pert)))
        def xorlike(x, f1,f2,f3):
            _,b,c,d,_ = self.dorounds(x)
            return self.f[0](b,c,d) == self.f[0](b^f1,c^f2,d^f3)^f1^f2^f3

        count = 0
        while True:
            # first find a 15 words xorlike prefix
            count += 1
            x = urandom(60)
            xw = self.btow(x)

            if not xorlike(xw[:4], 2,0,0):
                continue
            if not xorlike(xw[:5], 0,1<<31,0):
                continue
            if not xorlike(xw[:6], 0,0,1<<31):
                continue
            if not xorlike(xw[:8], 2,0,0):
                continue
            if not xorlike(xw[:9], 0,1<<31,0):
                continue
            if not xorlike(xw[:10], 0,0,1<<31):
                continue

            print(f"found prefix in {count} tries")
            count = 0
            while True:
                # brute force the last word
                count += 1
                if len(bin(count)) < len(bin(count+1)):
                    print(f"progress: 2^{int(log(count,2))}")

                w15 = int(urandom(4).hex(),16)
                xwf = xw + [w15]
                a,_,_,_,_ = self.dorounds(xwf)
                if not a&(1<<31):
                    w15 ^= (1<<31) # flip this bit if necessary
                    xwf = xw + [w15]

                expanded = self.expand(xwf)
                cv = self.compress(expanded)
                orig = self.wtob(cv)

                xw2 = [f^e for f,e in zip(flips,xwf)]
                expanded = self.expand(xw2)
                cv = self.compress(expanded)
                new = self.wtob(cv)
                if new == orig:
                    return (self.wtob(xwf), orig),(self.wtob(xw2), new)

if __name__ == "__main__":
    print("Theoretically finds a collision in 2^24")
    (x,o),(xx,v) = Shi2().fullcol()
    print(f"{x.hex()}")
    print(f"hashes to {o.hex()}")
    print(f"{xx.hex()}")
    print(f"hashes to {v.hex()}")
