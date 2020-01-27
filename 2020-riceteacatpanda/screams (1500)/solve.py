#!/usr/bin/env python
import soundfile
import cv2
import numpy

h = soundfile.SoundFile('aaaaaaaaaaaaaaaaaa.wav', 'r')
sf = h.read()
h.close()

l = 500
pic = numpy.zeros((l, l, 3), dtype=numpy.uint8)
for i in range(l):
    for j in range(l):
        count = i * l + j
        result = str(sf[count][1])
        if result.startswith('-'):
            result = result[1:]
        result = result[4:13]
        #print str(count), result
        r = int(result[0:3].zfill(3))
        g = int(result[3:6].zfill(3))
        b = int(result[6:9].zfill(3))
        pic[i][j][0] = r
        pic[i][j][1] = g
        pic[i][j][2] = b
cv2.imwrite('res.jpg', pic)

