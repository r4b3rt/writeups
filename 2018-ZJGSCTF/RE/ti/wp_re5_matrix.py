#coding=utf8
##https://www.cnblogs.com/chamie/p/4870078.html    矩阵乘法
from numpy import *;
mat1=[
[ 0x2B, 0x16, 0x1E, 0x53, 0x35, 0x39, 0x20, 0x29 ],
[ 0x35, 0x63, 0x0A, 0x28, 0x2C, 0x06, 0x32, 0x2A ],
[ 0x55, 0x39, 0x14, 0x5F, 0x20, 0x19, 0x34, 0x21 ],
[ 0x19, 0x0B, 0x5A, 0x09, 0x50, 0x34, 0x6F, 0x5C ],
[ 0x16, 0x1A, 0x68, 0x63, 0x34, 0x4E, 0x16, 0x45 ],
[ 0x4C, 0x53, 0x2F, 0x3F, 0x3F, 0x28, 0x69, 0x51 ],
[ 0x39, 0x44, 0x12, 0x24, 0x0A, 0x4D, 0x55, 0x31 ],
[ 0x49, 0x3B, 0x40, 0x3B, 0x43, 0x28, 0x21, 0x36 ]
]
enc=[
[39430, 34714, 32196, 36639, 34988, 34059, 30813, 33326], 
[36796, 32617, 33253, 34580, 34162, 34694, 27284, 30462], 
[43121, 39454, 38526, 40343, 40267, 39622, 32312, 35938], 
[52554, 37142, 43063, 43360, 41895, 39806, 44188, 43934], 
[51532, 44412, 41672, 48518, 45549, 44436, 41365, 45032], 
[60785, 49721, 52606, 54361, 52991, 52156, 47474, 50031], 
[43050, 35311, 36031, 39633, 34447, 34470, 31270, 31954],
[49152, 43386, 42096, 46024, 45029, 43961, 36733, 42762]
]
#矩阵的逆
#B*A=C
#B=A1*C
A=mat(mat1)
#A的逆矩阵
A1=linalg.inv(A)
C=mat(enc)
B1=A1*C

c=B1.tolist()
s=''
for j in range(8):
	k=c[j]
	for i in range(8):
		kk=int(k[i])+0.5
		if k[i]>kk:
			s=s+chr(int(k[i])+1)
		else:
			s=s+chr(int(k[i]))


def rot13(s):
	flag=''
	le=len(s)
	for ch in s:
		tmp=ord(ch)+13
		if ch.isupper():
			if tmp>90:
				tmp=tmp-26
		elif ch.islower():
			if tmp>122:
				tmp=tmp-26
		else:
			tmp=ord(ch)		
		flag +=chr(tmp)
	return flag

s=rot13(s)
print s

#flag{y0u_are_g0Od_for_Math_this_is_Matrix_5f0256b0f586a7b55dasd}


# #矩阵乘法
# print "矩阵乘法"
# #mat3=multiply(mat(mat1),mat(mat2))

#a=random.randint(0,128,size=[8,8])  
