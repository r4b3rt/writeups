#!/usr/bin/env python
#https://darth.fandom.com/wiki/Orders#Order_15
dic = {
    'T': 'R', 't': 'r',
    'O': 'T', 'o': 't',
    'V': 'C', 'v': 'c',
    'M': 'P', 'm': 'p',
    'S': 'A', 's': 'a',
    'X': 'J', 'x': 'j',
    'H': 'U', 'h': 'u',
    'Q': 'L', 'q': 'l',
    'B': 'Y', 'b': 'y',
    'A': 'O', 'a': 'o',
    'L': 'N', 'l': 'n',
    'Z': 'M', 'z': 'm',
    'W': 'E', 'w': 'e',
    'K': 'H', 'k': 'h',
    'C': 'I', 'c': 'i',
    'F': 'W', 'f': 'w',
    'I': 'D', 'i': 'd',
    'G': 'V', 'g': 'v',
    'Y': 'S', 'y': 's',
    'D': 'B', 'd': 'b',
    'N': 'G', 'n': 'g',
    'R': 'Q', 'r': 'q',
    'P': 'K', 'p': 'k',
    'J': 'X', 'j': 'x',
    'E': 'F', 'e': 'f'
}

with open('README.md', 'rb') as f:
    ciphertext = f.read()

plaintext = ''
for c in ciphertext:
    if c in dic.keys():
        plaintext += dic[c]
    else:
        plaintext += c
print plaintext

