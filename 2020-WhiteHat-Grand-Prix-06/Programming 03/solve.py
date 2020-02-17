#!/usr/bin/env python
#https://github.com/p4-team/ctf/blob/master/2020-01-04-whitehat/programming03/solver.py
from pwn import *

context.log_level = 'debug'

def solver(str1, str2):
	finalstr = str1 + '==' + str2
	result = True
	tab = [[0,1] if x in finalstr else [0] for x in ['A','B','C','D','E','F','G','H','I']]
	for A in tab[0]:
		for B in tab[1]:
			for C in tab[2]:
				for D in tab[3]:
					for E in tab[4]:
						for F in tab[5]:
							for G in tab[6]:
								for H in tab[7]:
									for I in tab[8]:
										result &= eval(finalstr.replace('*','&').replace('+','|').replace('A', str(A)).replace('B',str(B)).replace('C',str(C)).replace('D',str(D)).replace('E', str(E)).replace('F', str(F)).replace('G',str(G)).replace('H',str(H)).replace('I',str(I)))
										if result is False:
											return result
	return result

r = remote('52.78.36.66', 82)

while True:
    data = r.recv()
    if 'flag' in data:
        break
    i1 = data.index('E1')
    i2 = data.index('E2')
    str1 = data[i1 + 4:i2 - 1]
    str2 = data[i2 + 4:len(data) - 3]
    print str1
    print str2
    if solver(str1, str2):
        r.sendline('YES')
    else:
        r.sendline('NO')

print data
r.close()

