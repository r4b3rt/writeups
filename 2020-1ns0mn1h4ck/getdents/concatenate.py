#!/usr/bin/env python
with open('memory.zip', 'wb') as f:
    for i in range(10):
        with open(str(i) + '.dat', 'rb') as d:
            f.write(d.read())
