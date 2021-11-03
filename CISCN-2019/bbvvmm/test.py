#!/usr/bin/env python
import angr
import claripy

p = angr.Project('./test')
flag = claripy.BVS('flag', 5 * 8)
s = p.factory.blank_state(addr=0x400550, stdin=flag)

for c in flag.chop(8):
    s.solver.add(s.solver.And(c<='~', c>=' '))

sm = p.factory.simulation_manager(s)
sm.use_technique(angr.exploration_techniques.Explorer(find=0x4006C1, avoid=0x4006CD))
sm.run()

print(sm.one_found.posix.dumps(0))

