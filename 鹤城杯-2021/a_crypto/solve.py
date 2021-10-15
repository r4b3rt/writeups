#!/usr/bin/env python3
import codecs
import base64

dehex = codecs.getdecoder('hex_codec')
rot13 = codecs.getencoder('rot-13')

with open('./timu.txt', 'rb') as f:
    ciphertext = f.read()
print(ciphertext)
ciphertext = rot13(ciphertext.decode())[0]
print(ciphertext)
ciphertext = dehex(ciphertext)[0]
print(ciphertext)
ciphertext = base64.b32decode(ciphertext)
print(ciphertext)
ciphertext = base64.b64decode(ciphertext)
print(ciphertext)
ciphertext = base64.b85decode(ciphertext)
print(ciphertext)

