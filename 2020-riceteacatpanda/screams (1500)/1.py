import cv2
import soundfile
import random
import numpy

h = soundfile.SoundFile("oh-gawd-plsno.wav", 'r')
sf = h.read()
h.close()

pic = cv2.imread("pls-no.jpg")
i = pic.shape[0]
j = 0
k = numpy.zeros((i*i, 2), dtype=numpy.float64)

for n in range(0, i):
    for o in range(0, i):
        r = str(pic[n][o][0])
        g = str(pic[n][o][1])
        b = str(pic[n][o][2])
        while len(r) < 3:
            r = "0" + r
            while len(g) < 3:
                g = "0" + g
                while len(b) < 3:
                    b = "0" + b
        result = r + g + b
        s = random.randint(0, 1)
        if s == 0:
            k[j] = (sf[j][0]*2, float('0.00' + result))
        if s == 1:
            k[j] = (sf[j][0]*2, float('-0.00' + result))
        j += 1

soundfile.write('out.wav', k, 44100, 'FLOAT')
