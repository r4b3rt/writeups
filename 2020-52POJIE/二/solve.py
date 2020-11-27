#!/usr/bin/env python
import hashlib

md5 = lambda m: hashlib.md5(m).hexdigest()

string1 = '52pojie'
assert md5(string1) == 'E7EE5F4653E31955CACC7CD68E2A7839'.lower()

string2 = '2019'
assert md5(string2) == 'ea6b2efbdd4255a9f1b3bbc6399b58f4'

string3 = 'game'
assert md5(string3) == 'c8d46d341bea4fd5bff866a65ff8aea9'

flag = string1 + string2 + string3
assert len(flag) == 15
print flag

