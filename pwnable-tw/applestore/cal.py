#!/usr/bin/env python3
from z3 import *

s = Solver()

x = [Int('x%d' % i) for i in range(1, 6)]

for i in range(5):
    s.add(x[i] >= 0)
s.add(x[0] * 199 + x[1] * 299 + x[2] * 499 + x[3] * 399 + x[4] * 199 == 7174)
#s.add(x[0] + x[1] + x[2] + x[3] + x[4] < 26)

if s.check() == sat:
    print(s.model())

