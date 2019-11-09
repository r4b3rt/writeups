import base64
#----------------------------
enc1='flag{'
#----------------------------
enc2='\xf2\xee\xef\xf5\xd9\xef'
s=[]
s.append(enc1)
for x in enc2:
    s.append(chr(ord(x)^0x86))
#----------------------------
enc3='\x63\x31\x39\x7a\x62\x57\x4e\x66'
data=base64.b64decode(enc3)
s.append(data)
#-----------------------------
s.append('waaaaawwwww22222qqqaaw}')
print ''.join(s)
#flag{this_is_smc_waaaaawwwww22222qqqaaw}