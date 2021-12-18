import gmpy2
from fractions import Fraction
from secret import flag,e
from libnum import *
from os import urandom
k = 1024
p = gmpy2.next_prime(int(urandom(k / 8).encode('hex'),16))
q = gmpy2.next_prime(int(urandom(k / 8).encode('hex'),16))
n = p*q
assert(e<1000)
print n
print Fraction(int(p+1),int(p)) +Fraction(int(q+1),int(q))
print pow(123,e,n)

msg = s2n(flag)

assert(msg<n)
print pow(msg,e,n)
