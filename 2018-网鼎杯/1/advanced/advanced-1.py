stringA = r'K@LKVHr[DXEsLsYI@\AMYIr\EIZQ'
listA = []
for i in stringA:
    listA.append(ord(i))
for i in range(1, 500):
    encryptStr = str(i) * 3
    for i in range(len(stringA)):
        listA[i] = listA[i] ^ ord(encryptStr[i % len(encryptStr)]) ^ len(stringA)
flag = ''.join(chr(i) for i in listA)
print(flag)