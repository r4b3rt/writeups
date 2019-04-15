#!/usr/bin/env python
table = 'c61b68366edeb7bdce3c6820314b7498'
# enc = [0x0000001E, 0x00000018, 0x00000019, 0x00000020, 0x00000028, 0x00000024, 0x0000001C, 0x00000011, 0x00000022, 0x00000027, 0x00000010, 0x00000021, 0x00000013, 0x0000001A, 0x00000005, 0x00000003, 0x0000001D, 0x0000001B, 0x0000001F, 0x00000004, 0x00000008, 0x0000000F, 0x00000025, 0x0000002A, 0x0000000E, 0x00000029, 0x00000002, 0x00000017, 0x00000015, 0x00000000, 0x0000000A, 0x00000014, 0x00000007, 0x0000000B, 0x00000001, 0x0000000D, 0x00000006, 0x00000026, 0x00000012, 0x00000023, 0x0000000C, 0x00000016, 0x00000009]
fake = 'SharifCTF{????????????????????????????????}'
fake_list = []
for i in range(len(fake)):
	fake_list.append(fake[i])
for i in range(len(table)):
	if i & 1:
		sign = 1
	else:
		sign = -1
	fake_list[i + 10] = chr(ord(table[i]) + sign)
flag = ''
for i in range(len(fake_list)):
	flag += fake_list[i]
print flag
