#!/usr/bin/env python
import angr
import claripy

p = angr.Project('task_xman1')
flag_chars = [claripy.BVS('flag_%d' % i, 8) for i in range(28)] # flag's length is 28, every char is 8 bit
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')]) # end with '\n'

st = p.factory.full_init_state(
        args=['./xman_task1'], # arguments
        add_options=angr.options.unicorn,
        stdin=flag, # flag as input
)

for k in flag_chars:
    st.solver.add(k != 0) # char is not 0
    st.solver.add(k != 10) # char is not '\n'

sm = p.factory.simulation_manager(st)
sm.run()

out = b''
for pp in sm.deadended:
    out = pp.posix.dumps(1)
    if b'flag{' in out:
        out = next(filter(lambda s: b'flag{' in s, out.split()))
        break
print('flag:', out)
