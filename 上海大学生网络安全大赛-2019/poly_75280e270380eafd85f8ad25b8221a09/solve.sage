#!/usr/bin/env sage

P = PolynomialRing(GF(2), 'x')
F.<x> = GF(2)[]
base = x**255 + x**143 + x**47 + x**3 + 1
FF = GF(2**256)

r1 = 0xbd94909c0e247c276ef6816797dd2b176337a430269f4f9df7ea14923a1a
r2 = 0xc1fef44fd4d870d00622e1f40779a2a83a64ab693c54780960b043d4d2ea
c1 = 0x0000bd94909c0e247c276ef6816797dd2b176337a430269f4f9df7ea14923a1a
c2 = 0x0000c1fef44fd4d870d00622e1f40779a2a83a64ab693c54780960b043d4d2ea

def getPoly(c):
	b = bin(c)[2:].zfill(256)[::-1]
	p = 0
	for i in range(256):
		if b[i] == '1':
			p += x**i
	return p

h1 = getPoly(c1)
h2 = getPoly(c2)
print h1
print h2

f1 = getPoly(r1)
f2 = getPoly(r2)
print f1
print f2

key_1 = (h1-h2)*inverse_mod((f1-f2),base)%base
key_2 = (h1-f1*key_1)%base
print key_1
print key_2

