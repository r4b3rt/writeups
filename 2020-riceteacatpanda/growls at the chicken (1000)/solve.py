#!/usr/bin/env python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
 
ciphertext = '''NQr2MIa1jsaifAVOn3zYeMynNJwd4oBiiem4fJHsA1WjzfyhUp1+seCW0GMijoDHb3w9BMKj7aw6hhtae5/Qw5xOqMioJU3vvEj0BEHO1wInPqlOeTRdZb8BcTsXP+Z/KBA2FjSZcpGHo7rOZ7NtR15y3eY4s/e/tgKUHvPe9MdmDe1kINtyRXgjghJO9e3uMEQmFe2Ai5moVnG7yIVfUd3QG6/Z+K4PSttbJtjWSLFO7zpmYpEOg3XBxsOw/w5scJQqJ7OLGiH22u4+JFXRlD/wPmDzk9uYlLWLcCuxnY0xuMlSfKIFJtVmF0ViO4o4X89ZwsQjjHuYYDaB3el7iA63BzBlsC54Q7Ekv70/GI0UA3R3zJkMaBV12Z6NAE/kAgEJu9ZRcVm6MAIZInLwMU4R1frM0Bks1jeTe72agmxnAIrR8XDeAxzovbvXFwoxNyxiA63fPJGPVoGZq4ecfGvJ23i/Cg+cynB35lc3f+4QifpjCn+MxWkKCzCVEJXdDah19yXKlIxbaR1zm+YHkS0YSUzjr7NJUXHfDCrwAUpXpikfi2f9tgcXEnuhszScE1PCbdt22rRz1pS7MNdRxjCZ5j+8BQNRBLi2BjLGW14X3zd4d6ieoHWH+4fmbqU9dFsUgKN5qL4Gs2LZbbQwkf3+VbIRQK9RaSO9Hj+4/T0='''
 
rsa_key = RSA.importKey(open('privateKey', "rb").read())
cipher = Cipher_PKCS1_v1_5.new(rsa_key)
raw_cipher_data = ciphertext.decode('base64')
plaintext = cipher.decrypt(raw_cipher_data, None)
print plaintext

key = [9, 20, 30, 15, 16, 5, 14, 19, 30, 27, 29, 8, 20, 13, 12, 28]
table = "abcdefghijklmnopqrstuvwxyz[]. "
plaintext = ''
for i in key:
    plaintext += table[i - 1]
print plaintext

