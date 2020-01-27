#!/usr/bin/env python
with open('jef1056.github.io/archive/game.arcd0', 'rb') as f:
    binary = f.read()
flag = binary[0x271E:0x2738].replace('\n', '')
print flag

