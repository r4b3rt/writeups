#!/usr/bin/env python3
import base64
from PIL import Image
import libnum

img = Image.open('Oni.png')
im = img.load()
X, Y = img.size

out = ''
for y in range(Y):
    b = ''
    for x in range(8):
        if im[x, y] == (0,0,0,255):
            b += '1'
        else:
            b += '0'
    out += chr(int(b, 2))
print(out)

x = base64.b32decode(''.join([chr(ord(e) + 8) for e in out])).replace(b'\xe2\x96\xa2', b'Z')
print(x)

y = [int(base64.b85decode(x[i:i + 5]), 16) // 666 if b'F' in x[i:i + 5] else 0 for i in range(0, len(x), 5)]
print(y)

z = int(''.join(map(str, y)))
print(libnum.n2s(z)[::-1])
