#!/usr/bin/env python

with open('./tcp_stream_eq_2.out', 'rb') as f:
    data = f.read()
    flag = ''
    for c in data:
        if c == '.' or c == 'd':
            continue
        flag += c
    print flag

