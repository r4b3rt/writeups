#coding=utf8
from Crypto.Cipher import ARC4
import  base64
import string
print 'ARC4------------------------------------'
key='flag{this_is_not_the_flag_hahaha}'
msg='123456789'
ob1=ARC4.new(key)
enc=ob1.encrypt(msg)
print enc
enc="\x20\xc3\x1a\xae\x97\x3c\x7a\x41\xde\xf6\x78\x15\xcb\x4b\x4c\xdc\x26\x55\x8b\x55\xe5\xe9\x55\x75\x40\x3d\x82\x13\xa5\x60\x13\x3b\xf5\xd8\x19\x0e\x47\xcf\x5f\x5e\xde\x9d\x14\xbd"
ob2=ARC4.new(key)
enc1=ob2.decrypt(enc)
print enc1
#ZeptZ3l5UHQra25nd19yYzMrYR5wX2Jtc2P2VF9gYNM9
#ZeptZ3l5UHQra25nd19yYzMrYR5wX2Jtc2P2VF9gYNM9
print 'base64--------------------------------------'
s=''
Base64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
table=    "ABCDEFGHIJSTUVWKLMNOPQRXYZabcdqrstuvwxefghijklmnopyz0123456789+/"
for ch in enc1:
	if ch in Base64:
		s  = s + Base64[string.find(table,str(ch))]
	elif ch == '=':
		s = s + '=' 
print base64.b64decode(s)
#flag{y0u_know_rc4_and_base64_ha$}
