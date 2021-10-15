#!/usr/bin/env python3

encoded = '1010000011111000101010101000001010100100110110001111111010001000100000101000111011000100101111011001100011011000101011001100100010011001110110001001000010001100101111001110010011001100'

def up_back(x):
    r=''
    for i in range(0,len(x),8):
        c=chr(int(x[i:i+8],2)>>1)
        r+=c
    return r

def down_back(x):
    x = ''.join(['1' if x[i] == '0' else '0' for i in range(len(x))])
    return x

def right_back(x,d):
    x = x[-d:] + x[0:-d]
    return x

def left_back(x,d):
    x = x[::-1]
    x = right_back(x,len(x)-d)
    return x

d = 24
x = left_back(encoded,d)
x = down_back(x)
x = right_back(x,d)
x = up_back(x)

print(x)

