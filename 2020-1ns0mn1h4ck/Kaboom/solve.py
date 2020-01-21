#!/usr/bin/env python
#https://github.com/Pusty/writeups/tree/master/InsomnihackTeaser2020
s = [ord(c) for c in "63B4E14CBA1B83D7FD77E333".decode("hex")]
l = 0x42
sol = []
for i in s:
    sol.append(chr((i-l)&0xFF))
    l = i
sol.reverse()
print ''.join(sol) # Plz&Thank-Q!
