#!/usr/bin/env python
f = open('out', 'rb')
t = f.read()
f.close()
enc = []
for i in range(len(t)):
    enc.append(ord(t[i]))
print enc
flag = ''

def convert(c):
    c = ord(c)
    res = c - 10
    if c == 10:
        res = c + 35
    elif 32 <= c <= 34:
        res = c + 10
    elif c == 39:
        res = c + 2
    elif c == 44:
        res = c - 4
    elif c == 46:
        res = c - 7
    elif 58 <= c <= 59:
        res = c - 21
    elif c == 63:
        res = c - 27
    elif c == 95:
        res = c - 49
    else:
        if c <= 47 or c > 57:
            if c <= 64 or c > 90:
                if c > 96 and c <= 122:
                    res = c - 87
            else:
                res = c - 55
        else:
            res = c - 48
    return res

convert_map = {}
for ch in range(256):
    convert_map[convert(chr(ch))] = ch
# print convert_map

f = open('that_girl', 'rb')
that_girl = f.read()
f.close()
# print that_girl

girl = [0 for i in range(256)]
for i in range(len(that_girl)):
    t = convert(that_girl[i])
    girl[t * 4] += 1
# print girl

enc1 = []
enc1.append(((enc[-1] << 5) & 0xff) | (enc[0] >> 3))
for i in range(len(enc) - 1):
    enc1.append(((enc[i] << 5) & 0xff) | (enc[i + 1] >> 3))
print len(enc1)

table = [0x00000016, 0x00000000, 0x00000006, 0x00000002, 0x0000001E, 0x00000018, 0x00000009, 0x00000001, 0x00000015, 0x00000007, 0x00000012, 0x0000000A, 0x00000008, 0x0000000C, 0x00000011, 0x00000017, 0x0000000D, 0x00000004, 0x00000003, 0x0000000E, 0x00000013, 0x0000000B, 0x00000014, 0x00000010, 0x0000000F, 0x00000005, 0x00000019, 0x00000024, 0x0000001B, 0x0000001C, 0x0000001D, 0x00000025, 0x0000001F, 0x00000020, 0x00000021, 0x0000001A, 0x00000022, 0x00000023]
print len(table)

round_map = {}
x = 0
while table[x] != 0:
    round_map[table[x]] = x
    x = table[x]
round_map[0] = 1
print round_map

enc2 = [0 for i in range(len(enc1))]
for origin, encoded in round_map.items():
    enc2[origin] = enc1[encoded]

for i in range(len(enc2)):
    for j in range(len(girl) / 4):
        if enc2[i] == girl[j * 4]:
            flag += chr(convert_map[j])
            break

print 'flag: QCTF{%s}' % flag
