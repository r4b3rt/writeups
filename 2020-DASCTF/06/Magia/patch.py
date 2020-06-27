flag = 'Nep{mircle_and_maho_is_not_free}'
addr = 0x403000
while addr < 0x403240:
    b = Byte(addr)
    b ^= ord(flag[ord(flag[0]) & 0x1F]) & 0x10
    PatchByte(addr, b)
    addr += 1

