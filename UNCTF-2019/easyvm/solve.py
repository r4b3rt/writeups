#!/usr/bin/env python
import angr

proj = angr.Project('./vm')
simgr = proj.factory.simgr()
simgr.explore(find=lambda s: b'Congratulations!' in s.posix.dumps(1))
print(simgr.found[0].posix.dumps(0))
