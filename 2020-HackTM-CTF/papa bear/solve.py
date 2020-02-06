#!/usr/bin/env python3
#https://blog.redrocket.club/2020/02/04/hacktm20-papabear/
import subprocess
import string

soll = """
dWWW=- dWWMWWWWWMWMb dMMWWWWWWWWWb -=MMMb
dWMWP dWWWMWWWMMWMMMWWWWWMMMMMMWMMMWWWMMMb qMWb
WMWWb dMWWMMMMMMWWWWMMWWWMWWWWWWMMWWWWMWMWMMMWWWWb dMMM
qMMWMWMMMWMMWWWMWMMMMMMMMWMMMMWWWMMWWMWMWMMWWMWWWWMWWMMWMMWP
QWWWWWWWMMWWWWWWWMMWWWWMMWP QWWWMWMMMMWWWWWMMWWMWWWWWWMP
QWMWWWMMWWMWMWWWWMWWP QWWMWWMMMWMWMWWWWMMMP
QMWWMMMP QMMMMMMP
"""

def normalize(data):
    return ''.join(filter(lambda c: c if c in ['W', 'M'] else '', data)).replace('W', '1').replace('M', '0')

soll = normalize(soll)

states = ['HackTM{F4th3r bEaR s@y$: Smb']
while states:
    newstates = []
    for state in states:
        for c in string.digits + string.ascii_letters + string.whitespace + r"""!"#%&'()*+,-./:;<=>?@[\]^_`{|}~""":
            ist = subprocess.getoutput("./papa_bear '{}'".format((state + c).replace("'", "'\\''")))
            ist = ''.join(ist.splitlines()[7:])
            ist = normalize(ist)
            ist = ist[:ist.rfind('1') + 1]
            if soll.startswith(ist):
                newstates.append(state + c)
    states = newstates
    print(states)
