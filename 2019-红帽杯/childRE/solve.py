#!/usr/bin/env python

table = '1234567890-=!@#$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;,ASDFGHJKL:"ZXCVBNM<>?zxcvbnm,./'
s1 = '(_@4620!08!6_0*0442!@186%%0@3=66!!974*3234=&0^3&1@=&0908!6_0*&'
s2 = '55565653255552225565565555243466334653663544426565555525555222'

name = ''
for i in range(62):
    name += chr(table.find(s1[i]) + table.find(s2[i]) * 23)
print name

