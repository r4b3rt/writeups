#!/usr/bin/env python
from Crypto.Cipher import AES
import base64
import binascii
import re
import hashlib

class AESCBC:
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC
        self.bs = 16  # block size
        self.PADDING = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
     
    def encrypt(self, text):
        generator = AES.new(self.key, self.mode,self.key) 
        try:
            crypt = generator.encrypt(self.PADDING(text))
            crypted_str = base64.b64encode(crypt)
            result = crypted_str.decode()
        except Exception:
            result = 'Encrypt Failed!'
        return result
     
    def decrypt(self, text):
        generator = AES.new(self.key, self.mode,self.key) 
        text += (len(text) % 4) * '='
        try:
            decrpyt_bytes = base64.b64decode(text)
            meg = generator.decrypt(decrpyt_bytes)
            result = re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', meg.decode())
        except Exception:
            result = 'Decrypt Failed!'
        return result

def main():
    name = str(input('input uid:'))
    sha1 = hashlib.sha1()
    sha1.update(name.encode('utf8'))
    # key = binascii.a2b_hex('8380cf291d73c51efb5351d7df0268cb89be530e'[:32])
    key = binascii.a2b_hex(sha1.hexdigest()[:32])
    result = 'HappyNewYearFrom52PoJie.Cn'
    cryptor = AESCBC(key)
    plainText = cryptor.encrypt(result)
    print((plainText))

if __name__ == '__main__':
    main()
