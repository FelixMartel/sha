#!/usr/bin/env python3

from sha import Sha,rot
from functools import reduce

class Shi1(Sha):
    def __init__(self):
        super().__init__()

    def fgen(self, _):
        return lambda x,y,z: x^y^z

    def add(self, *args):
        return reduce(lambda x,y: x^y, args)

    def localcol(self,x):
        flips = [1,1<<5,1,2<<30,1<<30,1<<30]
        flips += [0]*(80-len(flips))
        expanded = self.expand(self.btow(x))

        cv = self.compress(expanded)
        orig = self.wtob(cv)

        expanded = [f^e for f,e in zip(flips,expanded)]
        cv = self.compress(expanded)
        new = self.wtob(cv)
        return orig, new

    def findflips(self):
        """
        find a perturbation vector that has a preimage
        """
        for p in self.findperturb():
            flips = self.preimage(self.correct(self.expand(p)))
            if flips is not None:
                return flips

    def fullcol(self,x):
        # magic flips found with findflips
        flips = [0, 0, 0, 0, 0, 1, 32, 1, 1073741825, 1073741856, 1073741824, 1073741857, 1073741857, 1, 1, 32]

        xw = self.btow(x)
        expanded = self.expand(xw)
        cv = self.compress(expanded)
        orig = self.wtob(cv)

        xx = [f^e for f,e in zip(flips,xw)]
        expanded = self.expand(xx)
        cv = self.compress(expanded)
        new = self.wtob(cv)
        return (x,orig),(self.wtob(xx), new)

    def findperturb(self):
        """
        find correctable perturbation vectors
        """
        def isvalid(x):
            xx = self.expand(x)
            return all([not i for i in xx[-5:]])

        for i in range(1,2**16):
            p = [int(i) for i in bin(i)[2:].zfill(16)]
            if isvalid(p):
                yield p

    def correct(self,pert):
        """
        add correction bits to perturbation
        """
        m0 = [0]*5 + pert
        m1 = [rot(m0[i-1],32-5) for i in range(5,len(m0))]
        m2 = [m0[i-2] for i in range(5,len(m0))]
        m3 = [rot(m0[i-3],32-30) for i in range(5,len(m0))]
        m4 = [rot(m0[i-4],32-30) for i in range(5,len(m0))]
        m5 = [rot(m0[i-5],32-30) for i in range(5,len(m0))]
        return [pert[i]^m1[i]^m2[i]^m3[i]^m4[i]^m5[i] for i in range(len(pert))]

    def preimage(self,ms):
        """
        brute force a preimage given 80 words from the expanded domain
        """
        pre = [0]*16
        for b in range(32):
            for i in range(2**16):
                p = [int(i) for i in bin(i)[2:].zfill(16)]
                ep = self.expand(p)
                if ep == [(m>>b)&1 for m in ms]:
                    pre = [p|(n<<b) for p,n in zip(pre,p)]
                    break
            else:
                return None
        return pre

if __name__ == "__main__":
    x = bytes.fromhex("02"*64)
    (x,o),(xx,v) = Shi1().fullcol(x)
    print(f"{x.hex()}")
    print(f"hashes to {o.hex()}")
    print(f"{xx.hex()}")
    print(f"hashes to {v.hex()}")
