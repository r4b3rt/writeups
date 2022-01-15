#!/usr/bin/env python
from Crypto.Cipher import AES
import base64
import libnum

key = bytes('1026'.ljust(16, ' '))
aes = AES.new(key, AES.MODE_ECB)
ciphertext = base64.b64decode('/cM8Nx+iAidmt6RiqX8Vww==')
plaintext = aes.decrypt(ciphertext)
print plaintext

