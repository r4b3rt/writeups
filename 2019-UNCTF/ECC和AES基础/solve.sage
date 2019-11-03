#!/usr/bin/env sage
E = EllipticCurve(GF(15424654874903), [16546484, 4548674875])
print(E)
G = E(6478678675, 5636379357093)
K = E(2854873820564, 9226233541419)
C1 = E(6860981508506, 1381088636252)
C2 = E(1935961385155, 8353060610242)

#print(factor(E.order()))
primes = [2, 353, 691, 31617863]
dlogs = []
for fac in primes:
    t = int(G.order()) / int(fac)
    dlog = discrete_log(t*C2, t*G, operation="+")
    dlogs += [dlog]
r = crt(dlogs, primes)
print(r)
print(r*G == C2)

M = C1 - r*K
print(C1 == M+r*K)
x = M[0]
print(x)

