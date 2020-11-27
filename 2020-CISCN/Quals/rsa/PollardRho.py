#!/usr/bin/env python
from random import randint
import gmpy2
import sys

if len(sys.argv) != 2:
    print 'Usage:', sys.argv[0], '[n in decimal]'
    exit()

def PollardRho_p_1(n):
    a = i = 2
    while True:
        a = gmpy2.powmod(a, i, n)
        d = gmpy2.gcd(a - 1, n)
        if d != 1:
            return d
        i += 1

if __name__ == '__main__':
    n = int(sys.argv[1])
    res = PollardRho_p_1(n)
    print '\033[0;36m[*] Result:\033[0m \033[0;31m%s\033[0m' % (res)

