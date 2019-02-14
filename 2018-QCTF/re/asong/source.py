#!/usr/bin/env python
s = [22, 0, 6, 2, 30, 24, 9, 1, 21, 7, 18, 10, 8, 12, 17, 23, 13, 4, 3, 14, 19, 11, 20, 16, 15, 5, 25, 36, 27, 28, 29, 37, 31, 32, 33, 26, 34, 35]
 
dic = {"a":104,"b":30,"c":15,"d":29,"e":169,"f":19,"g":38,"h":67,"i":60,"j":0,"k":20,"l":39,"m":28,"n":118,"o":165,"p":26,"q":0,"r":61,"s":51,"t":133,"u":45,"v":7,"w":34,"x":0,"y":62,"z":0,"_":245}
 
flag = r'QCTF{that_girl_saying_no_for_your_vindicate}'
 
def encypt(flag):
	f = flag[5:-1]
	e0 = []
	for i in f:
		e0.append(dic[i])
	i = 0
	temp = e0[0]
	while s[i] != 0:
		e0[i] = e0[s[i]]
		i = s[i]
	e0[i] = temp
	temp = (e0[0]>>5) & 0x7
	enc = ""
	for i in range(len(e0)-1):
		enc += chr(((e0[i] << 3) & 0xff) | ((e0[i+1] >> 5) & 0x7))
	enc += chr(((e0[len(e0)-1] << 3) & 0xff) | temp)
	return enc
 
 
def decypt(enc):
	# enc = open("out").read()
 
	d0 = []
	temp = ord(enc[len(enc)-1]) & 0x7
	for i in range(len(enc)):
		d0.append((temp << 5) | (ord(enc[i]) >> 3))
		temp = ord(enc[i]) & 0x7
 
	i = 37
	temp = d0[37]
	while s.index(i) != 37:
		d0[i] = d0[s.index(i)]
		i = s.index(i)
	d0[i] = temp
	flag = []
	for i in d0:
		flag.append(list(dic.keys())[list(dic.values()).index(i)])
	return "QCTF{%s}" % ''.join(flag)
 
print decypt(encypt(flag))
