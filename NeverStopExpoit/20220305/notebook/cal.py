#!/usr/bin/env python
from z3 import *

s = Solver()

arr = [BitVec('x%d' % i, 8) for i in range(16)]

s.add(arr[0] != 0)
s.add(67 == (arr[15] + 55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (55 * (arr[2] + 55 * (arr[1] + 55 * arr[0])) + arr[3]) + arr[4]) + arr[5]) + arr[6]) + arr[7]) + arr[8]) + arr[9]) + arr[10]) + arr[11]) + arr[12]) + arr[13]) + arr[14])) % 256)

if s.check() == sat:
    print s.model()

