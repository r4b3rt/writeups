#!/usr/bin/env python
#https://philzimmermann.com/EN/essays/SnakeOil.html
quipqiup = ''
flag = ''

with open('c', 'rb') as f:
    info = f.readlines()
    c = info[4][1:-2].split(', ')
    c = [int(ch) for ch in c]
    #print c
    print len(c)

freq = {}
for ch in c:
    if ch not in freq:
        freq[ch] = 1
    else:
        freq[ch] += 1
#print freq

mapping = {}
for i in range(len(freq.keys())):
    mapping[freq.keys()[i]] = chr(ord('A') + i)
for ch in c:
    quipqiup += mapping[ch]
#print quipqiup

dic = {
    'V': 'W',
    'U': 'H',
    '_': 'E',
    '\\': ' ',
    'J': 'I',
    'Y': 'A',
    'W': 'S',
    'C': 'O',
    'E': 'Y',
    'K': 'U',
    'P': 'R',
    'X': 'L',
    'Q': 'C',
    'G': 'P',
    'L': 'T',
    'S': 'G',
    'A': 'F',
    'B': '.',
    '^': 'D',
    'O': ',',
    'T': 'M',
    'F': 'V',
    'I': 'B',
    '[': 'Q',
    'M': '7',
    ']': '0',
    'D': 'X',
    'R': 'K',
    'H': '\''
}
for ch in quipqiup:
    if ch in dic:
        flag += dic[ch]
    else:
        flag += ch
flag = flag.lower()
print flag

