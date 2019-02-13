fake_flag = 'hebtuctf[thesE-is-wrong-flag-haha!]'
flag = ''
middle_flag = [25, 25, 25, 25, 25, 25, 25, 25, 32, 26, 93, 36, 10, 75, -94, 65, 90, 119, 2, 64, 4, 67, 63, 36, 24, 89, 6, 3, 108, 89, 10, 82, 105, 126, 25]
pre_middle_flag = [32, 32, 32, 32, 32, 32, 32, 32, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32]
# [32, 32, 32, 32, 32, 32, 32, 32, 32, 25, 40, 28, 17, 32, 114, 41, 3, 70, 40, 67, 28, 49, 9, 29, 18, 51, 21, 40, 66, 55, 9, 40, 19, 69, 32]
for i in range(len(middle_flag) - 1):
    if pre_middle_flag[33 - i] == 0:
        pre_middle_flag[33 - i] = (middle_flag[33 - i] ^ pre_middle_flag[34 - i]) - 25
for i in range(len(middle_flag)):
    ch = (pre_middle_flag[i] ^ ord(fake_flag[i])) % 256
    flag += chr(ch)
print flag