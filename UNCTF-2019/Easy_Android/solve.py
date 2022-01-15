#!/usr/bin/env python
import hashlib
import libnum

app_name = 'themix' # 0x7f0b0027 (2131427367) = string.app_name: themix
str2 = 'flag{this_is_a_fake_flag_ahhhhh}'
flag = ''

a = "2061e19de42da6e0de934592a2de3ca0"
b = "a81813dabd92cefdc6bbf28ea522d2d1"
c = "4b98921c9b772ed5971c9eca38b08c9f"
d = "81773872cbbd24dd8df2b980a2b47340"
e = "73b131aa8e4847d27a1c20608199814e"
f = "bbd7c4e20e99f0a3bf21c148fe22f21d"
g = "bf268d46ef91eea2634c34db64c91ef2"
h = "0862deb943decbddb87dbf0eec3a06cc"
check = [a, b, c, d, e, f, g, h]

h = lambda m: hashlib.md5(m).hexdigest()

s = '0123456789abcdef'
flag = ''
for i in range(8):
    for c1 in s:
        for c2 in s:
            for c3 in s:
                for c4 in s:
                    guess = c1 + c2 + c3 + c4
                    m = libnum.n2s(libnum.s2n(guess) ^ libnum.s2n(str2[4*i:4*i+4]))
                    if h(m) == check[i]:
                        flag += guess
print 'Result:', flag

