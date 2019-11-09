#!/usr/bin/env python
import pytesseract
from PIL import Image
import base64

for i in range(1, 576):
    image = Image.open('../Scattered/' + str(i) + '.jpg')
    crop = image.crop((30, 30, 150, 150))
    crop.load()
    crop.save(str(i), 'png')

output = ''
for i in range(1, 576):
    word = pytesseract.image_to_string(str(i), config='--psm 10')
    if word == '':
        output += 'a'
    elif word == '|':
        output += 'l'
    else:
        output += word[0]
if len(output) % 3 == 1:
    output += '=='
elif len(output) % 3 == 2:
    output += '='
print output

flag = base64.b64decode(output)
print flag
