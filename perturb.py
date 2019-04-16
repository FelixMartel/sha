#!/usr/bin/env python3

from shi1 import Shi1

"""
show how a single difference propagates
"""

class Shi(Shi1):
    def __init__(self):
        super().__init__()
        self.s = [0]*5

    def kgen(self, _):
        return 0

    def round_callback(self,s):
        print(" ".join([hex(w)[2:].zfill(8) for w in s]))


if __name__ == "__main__":
    x = bytes.fromhex("01"+"00"*63)
    print(Shi().hash(x).hex())
