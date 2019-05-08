from PIL import Image
import os
filename="./Traffic_Light.gif"
img=Image.open(filename)
now=0
try:
    while 1:
        img.seek(now)
        img.save(str(now)+".png")
        now+=1
except:
    pass