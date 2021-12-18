import os
load("secret.sage")
def genstr(n):
	return os.urandom(n)

def encrypt(msg, base, key):
	key_1, key_2 = key
	m = bin(int(msg.encode('hex'), 16))[2  :]
	assert len(m) <= 256  
	f1, ii = 0  ,0  
	for cc in m[::-1]:
		f1 += int(cc) * x**ii
		ii +=1   
	assert(key_1<base)
	assert(f1<base)
	assert(key_2<base)
	h = (key_1 * f1 + key_2 ) % base
	tmp = h.exponents()
	enc = ''
	for i in range(256):
		if i in tmp:
			enc += '1'
		else:
			enc += '0'
	enc = hex(int(enc[::-1],2)).lstrip('0x').rstrip('L').zfill(64)
	return enc

#P=PolynomialRing(GF(2),'x')
F.<x> = GF(2)[]
pol = x**255+ x**143+ x**47 + x**3 + 1  

r1 = genstr(30)
r2 = genstr(30)
FF = GF(2**256)

c1 = encrypt(r1, pol, key)
c2 = encrypt(r2, pol, key)
print r1.encode("hex")
print r2.encode("hex")
print c1
print c2
assert(len(flag)==60)
msg = (flag[:30],flag[30:])
print encrypt(msg[0], pol, key)
print encrypt(msg[1], pol, key)

