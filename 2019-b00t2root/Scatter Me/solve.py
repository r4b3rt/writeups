#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

f = open('scatter.txt', 'rb')
cords = f.read().split(';')
f.close()
x, y, z = [], [], []
for i in cords:
    x.append(float(i.split(':')[0]))
    y.append(float(i.split(':')[1]))
    # z.append(float(i.split(':')[2]))
plt.scatter(x, y) # , z)
plt.show()
