#!/usr/bin/env python
f = open('plain_array.txt', 'rb')
t = f.read()
f.close()
data = t.split('\n')[:-1]
print len(data)
# print data
f = open('trial.7z', 'wb')
for i in range(len(data)):
    f.write(chr(int(data[i])))
f.close()
