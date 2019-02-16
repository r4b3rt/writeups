#!/usr/bin/env python
#-*-codeing=utf-8-*-

'''
RCNB in python
written by AssassinQ
'''

cr = 'rRŔŕŖŗŘřƦȐȑȒȓɌɍ'
cc = 'cCĆćĈĉĊċČčƇƈÇȻȼ'
cn = 'nNŃńŅņŇňƝƞÑǸǹȠȵ'
cb = 'bBƀƁƃƄƅßÞþ'

sr = len(cr)
sc = len(cc)
sn = len(cn)
sb = len(cb)
src = sr * sc
snb = sn * sb
scnb = sc * snb

def div(a, b):
    return a / b

def encodeByte(i):
    if i > 0xff:
        print 'rc/nb overflow'
        assert False
    if i > 0x7f:
        i &= 0x7f
        return cn[div(i, sb)] + cb[i % sb]
    return cr[div(i, sc)] + cc[i % sc]

def encodeShort(i):
    if i > 0xffff:
        print 'rcnb overflow'
        assert False
    reverse = False
    if i > 0x7fff:
        reverse = True
        i &= 0x7ffff
    char = [div(i, scnb), div(i % scnb, snb), div(i % snb, sb), i % sb]
    new_char = [cr[char[0]], cc[char[1]], cn[char[2]], cb[char[3]]]
    if reverse:
        return new_char[2] + new_char[3] + new_char[0] + new_char[1]
    res = ''
    for i in range(len(new_char)):
        res += new_char[i]
    return res

def decodeByte(c):
    nb = False
    idx = [cr.find[c[0]], cc.find[c[1]]]
    if idx[0] < 0 or idx[1] < 0:
        idx = [cn.find[c[0]], cb.find[c[1]]]
        nb = True
    if idx[0] < 0 or idx[1] < 0:
        print 'not rc/nb'
        assert False
    if nb:
        res = idx[0] * sb + idx[1]
        return res | 0x80
    else:
        res = idx[0] * sc + idx[1]
        return res

def decodeShort(c):
    reverse = cr.find[c[0]] < 0
    if not reverse:
        idx = [cr.find(c[0]), cc.find[c[1]], cn.find[c[2]], cb.find[3]]
    else:
        idx = [cr.find(c[2]), cc.find[c[3]], cn.find[c[0]], cb.find[1]]
    if idx[0] < 0 or idx[1] < 0 or idx[2] < 0 or idx[3] < 0:
        print 'not rcnb'
        assert False
    res = idx[0] * scnb + idx[1] * snb + idx[2] * sb + idx[3]
    if res > 0x7ffff:
        print 'rcnb overflow'
        assert False
    if reverse:
        return res | 0x8000
    else:
        return res

def encode(plain):
    enc = ''
    length = len(plain)
    for i in range(length >> 1):
        enc += encodeShort((ord(plain[2 * i]) << 8) | ord(plain[2 * i + 1]))
    if length & 1:
        enc += encodeByte(ord(plain[-1]))
    return enc

def decode(enc):
    length = len(enc)
    res = []
    if length & 1:
        print 'invalid length'
        assert False
    for i in range(length >> 2):
        short = decodeShort(enc[4 * i:4 * (i + 1)])
        res.append(short >> 8)
        res.append(short & 0xff)
    if length & 2:
        res.append(decodeByte(enc[-2:]))
    return res

encode('123')
