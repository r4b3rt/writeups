#!/usr/bin/env python
#https://yof3ng.github.io/2019/10/21/flodbg-junkcode/
ciphertext = 'S@yRtfTl0+ag-L_3M}{'
plaintext = ciphertext

def func3(data, idx, a, b, c):
    return data[:idx + a] + data[idx + a + (c - b):idx + c] + data[idx + a:idx + a + (c - b)] + data[idx + c:]

plaintext = func3(plaintext, 16, 0, 2, 3)
print plaintext
plaintext = func3(plaintext, 11, 1, 3, 8)
print plaintext
plaintext = func3(plaintext, 10, 0, 2, 9)
print plaintext
plaintext = func3(plaintext, 16, 0, 2, 3)
print plaintext
plaintext = func3(plaintext, 0, 0, 7, 0x13)
print plaintext
plaintext = func3(plaintext, 8, 3, 6, 0xB)
print plaintext
plaintext = func3(plaintext, 15, 1, 3, 4)
print plaintext
plaintext = func3(plaintext, 3, 3, 5, 0x10)
print plaintext
plaintext = func3(plaintext, 0, 0, 2, 0x13)
print plaintext
plaintext = func3(plaintext, 5, 1, 5, 0xE)
print plaintext
plaintext = func3(plaintext, 11, 3, 6, 8)
print plaintext
plaintext = func3(plaintext, 0, 6, 9, 0xF)
print plaintext
plaintext = func3(plaintext, 9, 3, 5, 0xA)
print plaintext
plaintext = func3(plaintext, 2, 4, 6, 0x11)
print plaintext
plaintext = func3(plaintext, 5, 2, 7, 0xE)
print plaintext

