#!/usr/bin/env python
from Crypto.Cipher import AES

with open('flag_aes_cipher', 'rb') as f:
    ciphertext = f.read()
print len(ciphertext)

with open('iv_cipher.txt', 'rb') as f:
    iv_cipher_txt = f.readlines()
    iv_pk = iv_cipher_txt[0][4:-2].split(', ')
    iv_pk = [int(n.replace('L', '')) for n in iv_pk]
    # print iv_pk
    iv_key_cipher = int(iv_cipher_txt[1][11:-1])
    # print iv_key_cipher

