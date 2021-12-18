#!/usr/bin/env python
#https://blog.redrocket.club/2020/02/04/hacktm20-babybear/
import string

class Graph:
    def __init__(self, data):
        self.path = []
        self.data = data[:]
        self.length = 0x2e

    def finished(self):
        return self.length <= 0 or not self.data

    def emit(self, value):
        self.path.append(value)
        self.length -= 1

    def x366(self, x):
        if x:
            self.emit(1)
            return self.x34d
        self.emit(0)
        return self.x3de

    def x34d(self, x):
        if x:
            return self.x457
        return self.x40b

    def x457(self, x):
        if x:
            self.emit(0)
            return self.x3b0
        return self.x37e

    def x40b(self, x):
        if x:
            self.emit(1)
            self.emit(0)
            return self.x3b0
        self.emit(1)
        return self.x37e

    def x3de(self, x):
        if x:
            self.emit(0)
            return self.x379
        return self.x3e9

    def x3e9(self, x):
        if x:
            return self.x37e
        self.emit(0)
        return self.x470

    def x470(self, x):
        if x:
            self.emit(1)
            return self.x482
        return self.x44c

    def x44c(self, x):
        if x:
            self.emit(0)
            return self.x3c4
        return self.x3c7

    def x482(self, x):
        if x:
            self.emit(0)
            return self.x3c4
        return self.x44c

    def x3c4(self, x):
        if x:
            return self.x3c7
        return self.x366

    def x3c7(self, x):
        if x:
            self.emit(1)
            return self.x366
        self.emit(1)
        return self.x11b

    def x11b(self, x):
        if x:
            return self.x366
        self.emit(0)
        return self.x470

    def x39c(self, x):
        if x:
            self.emit(0)
            return self.x3b0
        self.emit(1)
        return self.x482

    def x3b0(self, x):
        if x:
            self.emit(0)
            return self.x3c4
        return self.x366

    def x37e(self, x):
        if x:
            return self.x39c
        self.emit(1)
        return self.x482

    def x379(self, x):
        if x:
            return self.x40b
        return self.x37e

    def traverse(self):
        current = self.x366
        while not self.finished():
            current = current(self.data.pop(0))
        return self.path

def tobin(key):
    res = ''
    for c in key:
        res += '{:08b}'.format(ord(c))[::-1]
    return [1 if c == '1' else 0 for c in res]

def arrstartswith(arr, pre):
    return arr[:len(pre)] == pre

result = [1 if x == '1' else 0 for x in '0010111111001000100111101111111011000100100100']

states = ['']
for _ in range(12):
    newstates = []
    for state in states:
        newstates += [state + x for x in string.letters]
    states = filter(lambda x: arrstartswith(result, Graph(tobin(x)).traverse()), newstates)[:10]

print states
