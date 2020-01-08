#!/usr/bin/env python
#https://github.com/pcw109550/write-up/tree/master/2019/ISITDTU/Chaos
from pwn import *
from string import ascii_lowercase, ascii_uppercase, digits

#context.log_level = 'debug'

punctuations = '~`!@#$%^&*()_-+=<,>.?|'

r = remote('15.164.159.194', 8006)
r.recvuntil('cipher key: ')
cipher_key = r.recvuntil('\n')[:-1].strip().split()

def get_enc(msg):
    r.recvuntil('choice: ')
    r.sendline('1')
    r.recvuntil('your message: ')
    r.sendline(msg)
    return r.recvuntil('\n')[:-1].strip()

def generate_list(chset, start=None, end=None):
    mapping = []
    for c in chset:
        mapping.append([r[start:end] for r in get_enc(str(c) * 64).split()])
    mapping = list(map(list, zip(*mapping)))
    for c in mapping:
        warning('Wrong...')
        assert len(set(c)) == len(chset)
    return mapping

def get_key():
    info('Generating lists...')
    alphabet_upper_list = generate_list(ascii_uppercase, 6, 10)
    alphabet_lower_list = generate_list(ascii_lowercase, -10, -6)
    digit_list = generate_list(digits, -4, None)
    punctuation_list = generate_list(punctuations, None, 4)

    info('Get key...')
    key = ''
    for i in range(64):
        query = cipher_key[i]
        l = len(query)
        if l == 16:
            key += digits[digit_list[i].index(query[-4:])]
        elif l == 22:
            if query[6:10] in alphabet_upper_list[i]:
                key += ascii_uppercase[alphabet_upper_list[i].index(query[6:10])]
            elif query[-10:-6] in alphabet_lower_list[i]:
                key += ascii_lowercase[alphabet_lower_list[i].index(query[-10:-6])]
            else:
                warning('Wrong...')
                assert False
        elif l == 28:
            key += punctuations[punctuation_list[i].index(query[:4])]
        else:
            warning('Wrong...')
            assert False
    success('Key: ' + key)
    return key

if __name__ == '__main__':
    key = get_key()
    info('Get Flag:')
    r.recvuntil('choice: ')
    r.sendline('2')
    r.recvuntil('get flag: ')
    r.sendline(key)
    ans = r.recv().strip()
    if 'WRONG KEY' in ans:
        warning('[!] Try again')
    else:
        success(ans) # Hav3_y0u_had_4_h3adach3_4ga1n??_Forgive_me!^^
    r.close()

