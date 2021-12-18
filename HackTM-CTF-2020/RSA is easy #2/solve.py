#!/usr/bin/env python
#https://crypto.stackexchange.com/questions/43583/deduce-modulus-n-from-public-exponent-and-encrypted-data
import gmpy2
import string

flag = ''
e = 65537

with open('c', 'rb') as f:
    info = f.readlines()
    c = info[4][1:-2].split(', ')
    c = [int(ch) for ch in c]
    #print c
    print len(c)

def getN():
    for i in c:
        for j in c:
            for x in string.printable:
                for y in string.printable:
                    if i != j and x != y:
                        g = gmpy2.gcd(ord(x) ** e - i, ord(y) ** e - j)
                        if g > 10 ** 10 and g not in ns:
                            return g

#n = getN()
n = 53361144550014053166721365196980912889938802302767543436340298420353476899874610747222379321544658210212273658744624182437888528301817525619324262586755752560722184172889301780332276353612167586294259101340749155939404015704537471927068307582449663907783314406726655255040519664154112497941090624585931831047

for ch in c:
    for b in string.printable:
        if gmpy2.powmod(ord(b), e, n) == ch:
            flag += b
print flag

