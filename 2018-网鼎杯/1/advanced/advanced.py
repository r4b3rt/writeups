enc = 'K@LKVHr[DXEsLsYI@\AMYIr\EIZQ'
flag = ''
for i in range(len(enc)):
    if i % 2 == 1:
        flag += chr(ord(enc[i]) ^ 0x2C)
    else:
        flag += chr(ord(enc[i]) ^ 0x2D)
print flag