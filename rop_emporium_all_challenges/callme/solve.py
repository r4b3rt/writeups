#!/usr/bin/env python
with open('key1.dat', 'rb') as f:
	k1 = f.read()
with open('key2.dat', 'rb') as f:
	k2 = f.read()
with open('encrypted_flag.txt', 'rb') as f:
	ciphertext = f.read()
plaintext = ''
for i in range(16):
	plaintext += chr(ord(ciphertext[i]) ^ ord(k1[i]))
for i in range(16):
	plaintext += chr(ord(ciphertext[i + 16]) ^ ord(k2[i]))
print plaintext
