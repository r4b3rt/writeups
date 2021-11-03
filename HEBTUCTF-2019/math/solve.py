#!/usr/bin/env python
import hashlib

a = -80538738812075974
b = 80435758145817515
c = 12602123297335631

flag = 'HEBTUCTF{' + hashlib.md5(str(a) + str(b) + str(c)).hexdigest() + '}'
print flag

