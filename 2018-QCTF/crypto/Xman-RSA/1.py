l1 = {
    'a': 'd',
    'b': 'm',
    'd': 'e',
    'e': 'n',
    'f': 'w',
    'g': 'f',
    'h': 'o',
    'i': 'x',
    'j': 'g',
    'k': 'p',
    'l': 'y',
    'm': 'h',
    'p': 'i',
    'q': 'r',
    'r': 'a',
    't': 's',
    'u': 'b',
    'v': 'k',
    'w': 't',
    'x': 'c',
    'y': 'l',
    'z': 'u'
}
f = open('encryption.encrypted', 'r')
ans = f.read()
# print ans
res = ""
for ch in ans:
    flag = 0
    for key, value in l1.items():
        if ch == key:
            res += value
            flag = 1
            break
        else:
            continue
    if flag == 1:
        continue
    else:
        res += ch
print res
raw_input()
f = open('encrypt.py', 'wb')
f.write(res)
f.close()
