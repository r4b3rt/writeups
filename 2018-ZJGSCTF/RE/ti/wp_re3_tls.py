
table="QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
enc="\x54\x4f\x69\x5a\x69\x5a\x74\x4f\x72\x59\x61\x54\x6f\x55\x77\x50\x6e\x54\x6f\x42\x73\x4f\x61\x4f\x61\x70\x73\x79\x53\x79"
lenn=len(enc)
print lenn
s=[]
for i in range(lenn):
	if i%2==0:
		s.append(enc[i])
	else:
		k = table.index(enc[i])
		if k>26:
			s.append(chr(k + 38))
		else:
			s.append( chr(k + 96))
print ''.join(s)
#flag{ThisisthreadofwindowshahaIsESE}