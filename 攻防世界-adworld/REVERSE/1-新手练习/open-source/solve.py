#!/usr/bin/env python
first = 0xcafe
second = 0
for i in range(1000):
    if i % 5 == 3 or i % 17 != 8:
        continue
    else:
        second = i
        break
third = 'h4cky0u'
res = first * 31337 + (second % 17) * 11 + len(third) - 1615810207
print hex(res)

