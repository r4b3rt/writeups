#!/usr/bin/env python

key = 'Resery'.lower()
key = [c for c in key]
for i in range(len(key)):
    key[i] = chr(0x100 - 37 - ord(key[i]))
key = ''.join(key)
print key

data = [0xFFFFFFFFFFFFFF80, 0x0000000000000059, 0x0000000000000023, 0x0000000000000035, 0x0000000000000022, 0x0000000000000073, 0xFFFFFFFFFFFFFF8D, 0x000000000000001A, 0x0000000000000051, 0x000000000000005D, 0x0000000000000030, 0xFFFFFFFFFFFFFFE8, 0x0000000000000057, 0x0000000000000026, 0xFFFFFFFFFFFFFFF6, 0x0000000000000007, 0xFFFFFFFFFFFFFFC6, 0xFFFFFFFFFFFFFF92, 0x000000000000005E, 0xFFFFFFFFFFFFFFDC, 0xFFFFFFFFFFFFFF83, 0x000000000000001F, 0x0000000000000076, 0xFFFFFFFFFFFFFF92, 0x0000000000000025, 0x000000000000000F, 0x0000000000000065, 0xFFFFFFFFFFFFFFFB, 0x000000000000002E, 0x000000000000004D, 0x000000000000006B, 0x0000000000000045, 0x0000000000000003, 0xFFFFFFFFFFFFFF87, 0xFFFFFFFFFFFFFFE9, 0xFFFFFFFFFFFFFF9F, 0x0000000000000022]
data = [chr(c & 0xff) for c in data]
print data
data = ''.join(data)

def rc4(text, key):
    result = ''
    key_len = len(key)
    box = list(range(256))
    j = 0
    for i in range(256):
        j = (j + box[i] + ord(key[i%key_len]))%256
        box[i],box[j] = box[j],box[i]
    i = j = 0
    for element in text:
        i = (i+1)%256
        j = (j+box[i])%256
        box[i],box[j] = box[j],box[i]
        k = chr(ord(element) ^ box[(box[i]+box[j])%256])
        result += k
    return result

flag = rc4(data, key)
print flag

