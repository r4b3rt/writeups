# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 09:54:25 2019

@author: WxJun
"""
from sage.all import *
import random
#import gmpy2
import binascii
from codecs import encode,decode
from Crypto.Cipher import AES
from functools import reduce
import numpy as np
def s2v(s):
    data = []
    for i in range(len(s)//2):
        data.append(ord(s[i*2])*(2**8)+ord(s[i*2+1]))
    return data
def v2s(v):
    """数字列表(向量)转字符串。
    将向量每个元素视作两字节。
    args:
        v: 向量，如:[123, 13, 456]
    return:
        返回字符串
    """
    b = []
    for i in v:
        b.append(i//(2**8))
        b.append(i%(2**8))
    b = ''.join(map(lambda x:chr(x),b))
    return b
def hadamard(A):
    if not A.is_square():
        raise Exception('must be square!')
    n = A.dimensions()[0]
    muls = reduce(lambda x,y:x*y, map(lambda x:x.norm(), A.rows()))
    return (abs(A.det())/muls)**(1./n)

def mh_make_key(n):
    privKey = [random.randint(1, 4**n)]
    s = privKey[0]
    for i in range(1, n):
        privKey.append(random.randint(s + 1, 4**(n + i)))
        s += privKey[i]
    q = random.randint(privKey[n-1] + 1, 2*privKey[n-1])
    r = random.randint(1, q)
    while gcd(r, q) != 1:
        r = random.randint(1, q)
    pubKey = [ r*w % q for w in privKey ]
    return privKey, q, r, pubKey

def mh_encrypt(plainText, pubKey):
    """使用AES256加密数据，密钥使用pubKey加密"""
    if not plainText:
        return None
    if not isinstance(plainText, bytes):
        plainText = plainText.encode('ascii')
    msg_bit = bin(int(encode(plainText,'hex'), 16))[2:]
    msg_bit = msg_bit.rjust(128, '0')
    if len(msg_bit) != len(pubKey):
        raise Exception('出错啦！')
    cipher = 0
    for i, bit in enumerate(msg_bit):
        cipher += int(bit)*pubKey[i]
    return cipher
def mh_decrypt(cipher, sk, q, r):
    pass
def aes_make_key(key_len=128):
    key = AES.get_random_bytes(key_len//8)
    iv = AES.get_random_bytes(128//8)
    return key, iv
def aes_enc(msg, key=None, iv=None, key_len=128):
    """aes加密，加密密钥在内部随机生成。
    Args:
        msg: 要加密的明文数据。
        key: 指定加密密钥，否则随机生成，默认为None
        key_len: 密钥的长度，key为None时生效。可选128,192,256,默认128
    Return:
        一个元组(cipher, key)表示加密后的密文与加密用的key。
    """
    if key_len not in (128, 192, 256):
        raise Exception('key_len长度错误！')
    if not key:
        key = 00#AES.get_random_bytes(key_len//8)
    if not iv:
        iv = key[:16]
    if not isinstance(msg, bytes):
        msg = msg.encode('utf8')
    msg += b'\x00' * (16 - len(msg)%16)
    aes = AES.new(key, AES.MODE_CBC, iv)
    cipher = aes.encrypt(msg)
    return cipher, key, iv
def aes_dec(cipher, key, iv):
    if cipher and key and iv:
        aes = AES.new(key, AES.MODE_CBC, iv)
        return aes.decrypt(cipher)
def mh_crack(A, S):
    """使用格基规约算法求SVP破解MH密码。
    Args:
        A: 背包密码的公钥，为向量。
        S: 密文，为一个大数。
    Return:
        返回解密后的明文。
    """
    dims = len(A)+1
    B = Matrix(ZZ, dims)
    # fill in the identity matrix
    for i in range(dims-1):
        B[i, i] = 1
        B[i, -1] = A[i]
    B[-1, -1] = -int(S)
    res = B.LLL()
    for i in range(0, dims):
        # print solution
        M = res.row(i).list()
        flag = True
        for m in M:
            if m != 0 and m != 1:
                flag = False
                break
        if flag:
            print(i, M)
            M = ''.join(str(j) for j in M)
            M = M[:-1]
            M = hex(int(M, 2))[2:-1]
            return decode(M, 'hex')

def ggh_make_key(n, gh=0.9, bh=0.2, try_time=1000):
    """生成GGH加密的密钥
    Args:
        n: 安全参数，及矩阵大小，n x n
        gh: 优质基hadamard比率
        bh: 劣质基hadamard比率
        try_time: 尝试次数
    Returns:
        (sk, pk, r)
    """
    def gen_det_one_matrix(n):
        """生成秩为1的矩阵(实际算法正负1都可以)"""
        det_one_matrix = Matrix.identity(n)
        for i in range(n):
            for j in range(i):
                if random.random() > 0.5:
                    det_one_matrix[i,j] = random.randint(-100,100)
        return det_one_matrix
    if False:
        sk = np.random.randint(-100, 100, size=(n,n))

    else:
        for i in range(try_time):
            sk = np.random.randint(-100, 100, size=(n,n))
            sk = Matrix(ZZ, sk)
            print('raw sk H:'+ str(hadamard(sk)))
            sk = sk.LLL()
            h = hadamard(sk)
            print('lll sk H' + str(h))
            if h >= gh:
                break
            if i == try_time - 1:
                return None
        pk = sk
        U = None
        for i in range(try_time):
            U = gen_det_one_matrix(n)
            pk = U*pk
            h = hadamard(pk)
            if h <= bh:
                break
            if i == try_time - 1:
                return None
        r = np.random.randint(-3,3,size=(n,))
        r = Matrix(ZZ, r.tolist())
    return sk, pk, r
def ggh_encrypt(msg, pk, r):
    if isinstance(msg, str):
        msg_len = len(msg)
        v = s2v(msg)
        m = matrix(ZZ,v)
    else:
        m = msg
    pk_len = pk.dimensions()[0]
    print('msg:', str(m))
    e = m*pk + r
    return e
    #msg_len
def ggh_decrypt(cipher, sk, pk):
    v = cipher*(sk.inverse())
    v = matrix_round(v)
    print(v)
    return v*sk*pk.inverse()
def ggh_test():
    V = matrix(ZZ,[
        [81,15,17,60,29],
        [-53,7,49,46,-11],
        [2,84,6,-68,-97],
        [11,-96,92,70,-70],
        [28,-58,98,-89,24]])
    U = matrix(ZZ,[
        [16,111,139,-16,-95],
        [-91,-642,-747,185,471],
        [-103,-677,-1133,492,524],
        [-21,-145,-190,55,111],
        [-10,-86,9,-82,62]])
    print(hadamard(V))
    W = matrix(ZZ,[
        [-7145,19739,-4237,3949,-15400],
        [40384,-113685,25691,-13165,75236],
        [45356,-179080,54894,27526,92497],
        [9317,-29008,7336,-1039,18230],
        [4600,4280,-5798,-16426,7011]
        ])
    W1 = U*V
    print(hadamard(W1))
    print(hadamard(W))
    m = matrix(ZZ,[-78,48,5,66,89])
    r = matrix(ZZ,[-9,-5,1,-2,4])
    e = ggh_encrypt(m,W,r)
    mm = ggh_decrypt(e,V,W)
    mm1 = ggh_decrypt(e,W.LLL(),W)
    raw_input('##')
def matrix_round(A):
    rs, cs = A.dimensions()
    for i in range(rs):
        for j in range(cs):
            A[i,j] = round(A[i,j])
    return A
def main():
    #fun = ForFun()
    #cipher, key = fun.aes_enc('zjgsctf{hahahahahahha}')
    #test_case = b'\xfcG\xe9&fao\xca\xb3:^\xaf\xb4G\xdc\xd8'
    #fun.ggh_make_key(8)
    #a = fun.aes_make_key()

    # md5(B2taMa0_DiDiDi,32) = 932b4f54526f8006387fc1f1298ecd58
    flag = 'ZJGSUCTF{932b4f54526f8006387fc1f1298ecd58}'
    aes_key = b'\x18\x1a\x16\xd5\xcc\xb5wz\x1d\x95\xe6\xfe\xd6\x06\xeb\x93'
    aes_iv = b'\x06|\x84\xb1\x8a\x1c\x1c4V\x8d0\xd5\xbf\x02\x8d\xfc'
    #fun.mh_make_key()
    #with open('aes_key.txt', 'w') as f:
    #    f.write()
    sk, q, r, pk = mh_make_key(128)
    key_cipher = mh_encrypt(aes_key,pk)
    with open('mh_test.txt', 'w') as f:
        f.write('pk:{}\nkey_cipher:{}\n'.format(str(pk),str(key_cipher)))
    msg = mh_crack(pk,key_cipher)
    sk, pk, r = ggh_make_key(8)
    iv_cipher = ggh_encrypt(aes_iv,pk,r)
    msg = ggh_decrypt(iv_cipher, pk.BKZ(), pk)
    print('dec:', msg)
    with open('ggh_test.txt', 'w') as f:
        f.write('pk:{}\niv_cipher:{}\n'.format(str(pk), str(iv_cipher)))
    flag_aes_cipher = aes_enc(flag, aes_key, aes_iv)[0]
    with open('flag_aes_cipher', 'wb') as f:
        f.write(flag_aes_cipher)

    #ggh_test()
#print(makeKey(64)[3])
main()
