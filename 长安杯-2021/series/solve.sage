#!/usr/bin/env sage
from Crypto.Util.number import *
from gmpy2 import next_prime

def fastPow(M, x, n=None):
    if x==0:
        return identity_matrix(len(M.columns()))
    if n!=None:
        res = fastPow(M, x//2, n)
    else:
        res = fastPow(M, x//2)
    if x%2 == 1:
        if n!=None:
            return res*res*M % n
        else:
            return res*res*M
    else:
        if n!=None:
            return res*res % n
        else:
            return res*res

e = 1292991588783542706506728336494377723983115217051171962646571511384590134899
c = 229797522574801936576076488492034448896863980731763047709941641260180597290800402814069755381965565755866855389082787759443816945304000719176334587540293777658369250939545994974691382505993209963323032684771922094686136104097942892330051349688373437571196103392801691879287264056022383484359551333197
# yafu!
ep = 33285073849485750791903437807279991921
eq = 38845988283830087557982578789883120419
assert ep*eq == e
phi = int((ep^2-1)*(eq^2-1))
phi2 = int(euler_phi(ep+1)*euler_phi(ep-1)*euler_phi(eq+1)*euler_phi(eq-1))  # euler_phi(phi)

one = matrix(ZZ, [1, 1, 1]).transpose()
Fme = matrix(IntegerModRing(e), [[1, 1, 1], [1, 0, 0], [0, 1, 0]])

def Fe(n, i=0):
  return int((Fme^n*Fme^(i-3)*one)[0][0])%e

def Fe2(n, i=0):
  n = int(n)
  return int((Fme^pow(n, n, phi)*Fme^(i-3)*one)[0][0])%e

def Fe3(m, n, i=0):
  m = int(m)
  n = int(n)
  return int((Fme^pow(m, pow(n, n, phi2), phi)*Fme^(i-3)*one)[0][0])%e

s1 = reduce(lambda a, b: a*b, [Fe2(e, i) for i in range(1, 5)])
s2 = Fe3(2021, e)^4
s = s1+s2
p = next_prime(s)
print('c = %s' % c)
print('p = %s' % p)

d = e.inverse_mod(p-1)
m = pow(c, d, p)
print(long_to_bytes(int(m)))
