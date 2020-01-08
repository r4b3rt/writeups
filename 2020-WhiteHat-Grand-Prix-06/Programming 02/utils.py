#!/usr/bin/env python
import socket

class Conn:
    def __init__(self, ip, port):
        conn = socket.socket()
        conn.connect((ip, port))
        self.conn = conn

    def recv(self, n):
        return self.conn.recv(n)

    def recvuntil(self, s):
        length = len(s)
        c = ''
        while True:
            c += self.conn.recv(1)
            if s in c:
                print '[!] Recieved...'
                print c
                return c

    def sendline(self, s):
        print '[!] Sent..'
        print s
        self.conn.send(s + '\n')

def remote(ip, port):
    return Conn(ip, port)

