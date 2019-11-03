#!/usr/bin/env python
import gmpy2
import libnum

c1 = 62501276588435548378091741866858001847904773180843384150570636252430662080263
c2 = 72510845991687063707663748783701000040760576923237697638580153046559809128516

def getM(c):
    e = 2
    n = 0xc2636ae5c3d8e43ffb97ab09028f1aac6c0bf6cd3d70ebca281bffe97fbe30dd
    p = 275127860351348928173285174381581152299
    q = 319576316814478949870590164193048041239
    u = gmpy2.powmod(c, (p + 1) / 4, p)
    v = gmpy2.powmod(c, (q + 1) / 4, q)
    s = gmpy2.invert(p, q)
    t = gmpy2.invert(q, p)
    x = (t * q * u + s * p * v) % n
    y = (t * q * u - s * p * v) % n

    print libnum.n2s(x % n)
    print libnum.n2s((-x) % n)
    print libnum.n2s(y % n)
    print libnum.n2s((-y) % n)

getM(c1)
getM(c2)

