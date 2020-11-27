#!/usr/bin/env sage

N = 100
F = GF(2)

with open('./output.txt', 'rb') as f:
    c = f.read()

origState = c[:200][::-1]
scdState = c[100:200][::-1]

#mask = matrix([vector(F, 1) for i in range(N)])
mask = var('mask')
print mask

for i in range(N):
    state = origState[i:100+i]
    state = matrix([int(c) for c in state])
    print state
    target = matrix([int(scdState[i])])
    print target
    solve(state*mask==target, mask)

