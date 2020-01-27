#!/usr/bin/env python
with open('motivation!!!!!.txt', 'rb') as f1, open('motivation.png', 'wb') as f2:
    data = f1.read()[::-1]
    f2.write(data)
