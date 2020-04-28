from Crypto.Util.number import *
import gmpy2
from flag import flag


def generate():
    p = getStrongPrime(2048)
    while True:
        f = getRandomNBitInteger(1024)
        g = getStrongPrime(768)
        h = gmpy2.invert(f, p) * g % p
        return (p, f, g, h)


def encrypt(plaintext, p, h):
    m = bytes_to_long(plaintext)
    r = getRandomNBitInteger(1024)
    c = (r * h + m) % p
    return c


p, f, g, h = generate()
c = encrypt(flag, p, h)
with open("cipher.txt", "w") as f:
    f.write("h = " + str(h) + "\n")
    f.write("p = " + str(p) + "\n")
    f.write("c = " + str(c) + "\n")
