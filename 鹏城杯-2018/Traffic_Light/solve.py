#!/usr/bin/env python
import hashlib
res = ''
for i in range(1168):
    name = str(i) + '.png'
    f = open(name, 'rb')
    t = hashlib.md5(f.read()).hexdigest()
    f.close()
    if t == '6175f314321c164c6c39b3eb11acb152':
        # res_l.append('green')
        res += '0'
    elif t == '6d20830240b028d9bf6bdc5c86257204':
        # res_l.append('none')
        res += ''
    elif t == '7a89146e83e226522b93eec505b6e6eb':
        # res_l.append('red')
        res += '1'
    elif t == '7a4035734a8ecd541357674ceda81b3e':
        # res_l.append('yellow')
        res += ''
    else:
        print 'error'
# print len(res)
# print res
tmp = ''
for i in range(len(res) / 8):
    tmp += chr(int(res[8*i:8*i+8],2))
print tmp
    
