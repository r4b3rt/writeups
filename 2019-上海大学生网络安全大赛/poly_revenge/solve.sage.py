

# This file was *autogenerated* from the file ./solve.sage
from sage.all_cmdline import *   # import sage library

_sage_const_3 = Integer(3); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_0x1e63622141285872093eda8da6c7a94ad7c50e695fdc6ed9bd8adaf4c6c40b14 = Integer(0x1e63622141285872093eda8da6c7a94ad7c50e695fdc6ed9bd8adaf4c6c40b14); _sage_const_0x8eeb27d8c2776920bd4672bbcee6d1ebf357c81419e2c3e2073a1e241dbd = Integer(0x8eeb27d8c2776920bd4672bbcee6d1ebf357c81419e2c3e2073a1e241dbd); _sage_const_47 = Integer(47); _sage_const_0x237b20405cf83f261749fba5507ed14cb566e3722a93308c7752297d92a8338c = Integer(0x237b20405cf83f261749fba5507ed14cb566e3722a93308c7752297d92a8338c); _sage_const_255 = Integer(255); _sage_const_256 = Integer(256); _sage_const_64 = Integer(64); _sage_const_0x1f8fe9b5e32500c3d306924938d1f443b3718ec410c380944503311ff932f528 = Integer(0x1f8fe9b5e32500c3d306924938d1f443b3718ec410c380944503311ff932f528); _sage_const_0x8e4188999c007557e481d4dfcf51a8bb92a752ebac7015967f1133387c7c = Integer(0x8e4188999c007557e481d4dfcf51a8bb92a752ebac7015967f1133387c7c); _sage_const_143 = Integer(143); _sage_const_0x1a99ff13954d42e6a21af67aa58e2df8b7bec68f499edf992c95b25326ed768c = Integer(0x1a99ff13954d42e6a21af67aa58e2df8b7bec68f499edf992c95b25326ed768c)#!/usr/bin/env sage

P=PolynomialRing(GF(_sage_const_2 ),'x')
F = GF(_sage_const_2 )['x']; (x,) = F._first_ngens(1)
base = x**_sage_const_255 + x**_sage_const_143 + x**_sage_const_47  + x**_sage_const_3  + _sage_const_1 
FF = GF(_sage_const_2 **_sage_const_256 )

r1 = _sage_const_0x8eeb27d8c2776920bd4672bbcee6d1ebf357c81419e2c3e2073a1e241dbd 
r2 = _sage_const_0x8e4188999c007557e481d4dfcf51a8bb92a752ebac7015967f1133387c7c 
c1 = _sage_const_0x237b20405cf83f261749fba5507ed14cb566e3722a93308c7752297d92a8338c 
c2 = _sage_const_0x1f8fe9b5e32500c3d306924938d1f443b3718ec410c380944503311ff932f528 

def getPoly(c):
	b = bin(c)[_sage_const_2 :].zfill(_sage_const_256 )[::-_sage_const_1 ]
	p = _sage_const_0 
	for i in range(_sage_const_256 ):
		if b[i] == '1':
			p += x**i
	return p

h1 = getPoly(c1)
h2 = getPoly(c2)

f1 = getPoly(r1)
f2 = getPoly(r2)

key_1 = (h1-h2)*inverse_mod((f1-f2),base)%base
key_2 = (h1-f1*key_1)%base
print 'key_1:', key_1
print 'key_2:', key_2

ciphertext1 = _sage_const_0x1a99ff13954d42e6a21af67aa58e2df8b7bec68f499edf992c95b25326ed768c 
ciphertext2 = _sage_const_0x1e63622141285872093eda8da6c7a94ad7c50e695fdc6ed9bd8adaf4c6c40b14 

ch1 = getPoly(ciphertext1)
ch2 = getPoly(ciphertext2)
plaintext1 = (ch1-key_2)*inverse_mod(key_1,base)%base
plaintext2 = (ch2-key_2)*inverse_mod(key_1,base)%base

def getNum(p):
	tmp = p.exponents()
	b = ''
	for i in range(_sage_const_256 ):
		if i in tmp:
			b += '1'
		else:
			b += '0'
	return hex(int(b[::-_sage_const_1 ], _sage_const_2 )).lstrip('0x').rstrip('L').zfill(_sage_const_64 )

flag1 = getNum(plaintext1).decode('hex')
flag2 = getNum(plaintext2).decode('hex')
flag = flag1 + flag2
print flag


