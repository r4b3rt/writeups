#!/usr/bin/env python
code = [33, 0, 129, 39, 1, 1, 36, 1, 1, 35, 2, 0, 34, 3, 2, 33, 4, 8, 40, 3, 4, 39, 2, 3, 40, 3, 4, 39, 2, 3, 40, 3, 4, 39, 2, 3, 39, 3, 3, 35, 4, 3, 36, 3, 2, 39, 2, 4, 36, 0, 2, 33, 1, 1, 37, 0, 1, 34, 1, 0, 33, 2, 129, 38, 1, 2, 33, 2, 9, 38, 1, 2, 33, 2, 9, 45, 2, 1, 33, 0, 129, 34, 1, 0, 33, 2, 9, 37, 1, 2, 35, 3, 0, 35, 4, 1, 38, 3, 4, 33, 4, 126, 45, 4, 3, 33, 3, 1, 37, 0, 3, 37, 1, 3, 38, 2, 3, 33, 4, 90, 45, 4, 2, 47, 0, 0, 48, 0, 0]
data = [0x61646238, 0x36353465, 0x6361352d, 0x31312d38, 0x612d3965, 0x2d316331, 0x39653838, 0x30386566, 0x66616566, 0x57635565, 0x06530401, 0x1f494949, 0x5157071f, 0x575f4357, 0x57435e57, 0x4357020a, 0x575e035e, 0x0f590000, 0x6e6f7277, 0x20202067, 0x00202020, 0x72726f63, 0x20746365, 0x20202020, 0x6c660020, 0x69206761, 0x6c662073, 0x597b6761, 0x5072756f, 0x68637461, 0x2020207d, 0x20202020, 0x20202020, 0x20202020, 0x20202020, 0x20202020, 0x20202020, 0xffffff00, 0xffffffff]
code = code + data
pc = 0
buf = [0, 0, 0, 0, 0]

while pc < len(code):
    ins = code[pc]
    op1 = code[pc + 1]
    op2 = code[pc + 2]
    pc += 3
    if ins == 0x21:
        print 'buf[%d] = %d' % (op1, op2)
        buf[op1] = op2
    elif ins == 0x22:
        print 'buf[%d] = buf[%d]' % (op1, op2)
        buf[op1] = buf[op2]
    elif ins == 0x23:
        if buf[op2] >= (0x204 + 0x6F) / 4:
            comment = 'Read patch'
        elif buf[op2] >= 0x204 / 4:
            comment = 'Read code, offset:', str(buf[op2])
        else:
            comment = str(buf[op2])
        print 'buf[%d] = code[buf[%d]] # %s' % (op1, op2, comment)
        buf[op1] = code[buf[op2]]
    elif ins == 0x24:
        if buf[op1] >= (0x204 + 0x6F) / 4:
            comment = 'Write patch'
        elif buf[op1] >= 0x204 / 4:
            comment = 'Write code, offset:', str(buf[op1])
        else:
            comment = str(buf[op1])
        print 'code[buf[%d]] = buf[%d] # %s' % (op1, op2, comment)
        code[buf[op1]] = buf[op2]
    elif ins == 0x25:
        print 'buf[%d] += buf[%d]' % (op1, op2)
        buf[op1] += buf[op2]
    elif ins == 0x26:
        print 'buf[%d] -= buf[%d]' % (op1, op2)
        buf[op1] -= buf[op2]
    elif ins == 0x27:
        print 'buf[%d] ^= buf[%d]' % (op1, op2)
        buf[op1] ^= buf[op2]
    elif ins == 0x28:
        print 'buf[%d] <<= (buf[%d] & 0xFF)' % (op1, op2)
        buf[op1] <<= (buf[op2] & 0xFF)
    elif ins == 0x29:
        print 'buf[%d] >>= (buf[%d] & 0xFF)' % (op1, op2)
        buf[op1] >>= (buf[op2] & 0xFF)
    elif ins == 0x2A:
        print 'buf[%d] &= buf[%d]' % (op1, op2)
        buf[op1] &= buf[op2]
    elif ins == 0x2B:
        print 'pc = buf[%d] # jmp %d' % (op1, buf[op1])
        pc = buf[op1]
    elif ins == 0x2C:
        print 'if buf[%d] == 0:' % (op2)
        print '\tpc = buf[%d] # jmp %d' % (op1, buf[op1])
        if buf[op2] == 0:
            pc = buf[op1]
    elif ins == 0x2D:
        print 'if buf[%d] != 0:' % (op2)
        print '\tpc = buf[%d] # jmp %d' % (op1, buf[op1])
        if op2 == 3: # if do not jmp
            continue
        if buf[op2] != 0:
            pc = buf[op1]
    elif ins == 0x2E:
        print 'exit(0)'
        exit(0)
    elif ins == 0x2F:
        print 'print \'right\''
    elif ins == 0x30:
        print 'print \'wrong\''
    else:
        break
print code
print buf

