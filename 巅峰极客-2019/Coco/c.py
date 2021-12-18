from Crypto.Util.number import *
from Crypto.Random.random import *
from flag import flag

p = getStrongPrime(1024)
q = getStrongPrime(1024)
k = getStrongPrime(1024)

def gcd(a, b):
    while b: a, b = b, a % b
    return a

def func(a, b, c): # a ^ b % c
    res = 1
    while b != 0:
        if (b & 1) == 1:
            res = (res * a) % c
        b >>= 1
        a = (a * a) % c
    return res

x = func(k, p, q)
while True:
    r = randint(1, 2 ** 512)
    if gcd(r, q - 1) == 1:
        break
key = bytes_to_long("CoCoCoCoCoCoCoCoCoCoCoCoCoCoCoCoCoCoCoCoCoCoCoCo")
c1 = func(k, r, q)
c2 = (key * func(x, r, q)) % q
m = bytes_to_long(flag)
c3 = (m * func(x, r, q)) % q
with open('cipher.txt', 'w') as f:
    f.write("c1 = " + str(c1) + "\n")
    f.write("k = " + str(k) + "\n")
    f.write("c2 = " + str(c2) + "\n")
    f.write("q = " + str(q) + "\n")
    f.write("c3 = " + str(c3) + "\n")
