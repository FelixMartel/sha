#!/usr/bin/env python3

from functools import reduce

def rot(x,i):
    return (x>>i)|((x&(2**i-1))<<(32-i))

class Sha:
    def __init__(self):
        self.rounds = 80
        self.f = [self.fgen(i) for i in range(self.rounds)]
        self.k = [self.kgen(i) for i in range(self.rounds)]
        self.s = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    def round_callback(self,s):
        pass

    def fgen(self, i):
        if 0 <= i <= 19:
            return lambda x,y,z: (x&y)|(~x&z)
        elif 40 <= i <= 59:
            return lambda x,y,z: (x&y)|(x&z)|(y&z)
        else:
            return lambda x,y,z: x^y^z

    def kgen(self, i):
        if 0 <= i <= 19:
            return 0x5A827999
        elif 20 <= i <= 39:
            return 0x6ED9EBA1
        elif 40 <= i <= 59:
            return 0x8F1BBCDC
        else:
            return 0xCA62C1D6

    def add(self, *args):
        return reduce(lambda x,y: x+y, args)%2**32

    def expand(self, x):
        ex = x[:]
        for i in range(16,self.rounds):
            ex.append(ex[i-3]^ex[i-8]^ex[i-14]^ex[i-16])
            #ex.append(rot(ex[i-3]^ex[i-8]^ex[i-14]^ex[i-16],32-1)) #sha1
        return ex

    def btow(self, x):
        """
        split bytes into 4 byte words
        """
        return [int(x[i:i+4].hex(),16) for i in range(0,len(x),4)]

    def wtob(self, x):
        """
        concatenate 4 byte words
        """
        return bytes.fromhex("".join([hex(w)[2:].zfill(8) for w in x]))

    def hash(self, x):
        """
        full hash of a single block, no padding
        """
        assert len(x) == 64
        expanded = self.expand(self.btow(x))
        cv = self.compress(expanded)
        return self.wtob(cv)

    def compress(self, ws):
        state = self.dorounds(ws)
        return [(iv+s)%2**32 for s,iv in zip(state,self.s)]

    def dorounds(self, ws):
        a,b,c,d,e = self.s
        for i,w in enumerate(ws):
            t = self.add(rot(a,32-5), self.f[i](b,c,d), e, self.k[i], w)
            e = d
            d = c
            c = rot(b,32-30)
            b = a
            a = t
            self.round_callback([a,b,c,d,e])
        return [a,b,c,d,e]

if __name__ == "__main__":
    x = bytes.fromhex("61626380" + "00"*(14*4) + "00000018")
    print(Sha().hash(x).hex())
