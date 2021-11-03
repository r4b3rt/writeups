#!/usr/bin/env python
flag_part2_enc = "29'>823'hhlh"
flag_part2 = "8?-?2??-?b?b"
key = ord('8') ^ ord('2')
flag_part2 = ''
for i in range(len(flag_part2_enc)):
    flag_part2 += chr(ord(flag_part2_enc[i]) ^ key)
print flag_part2

