#!/usr/bin/env python
import gmpy2

# https://tover.xyz/p/Fibonacci-series/

e = 1292991588783542706506728336494377723983115217051171962646571511384590134899
c = 229797522574801936576076488492034448896863980731763047709941641260180597290800402814069755381965565755866855389082787759443816945304000719176334587540293777658369250939545994974691382505993209963323032684771922094686136104097942892330051349688373437571196103392801691879287264056022383484359551333197

K = 3

def mul(a, b):
    c = [[0 for i in range(3)] for j in range(3)]
    for i in range(K):
        for j in range(K):
            for k in range(K):
                c[i][j] += a[i][k] * b[k][j]
    return c

def pow(a, p):
    if p == 1:
        return a
    if p % 2:
        return mul(a, pow(a, p - 1))
    x = pow(a, p / 2)
    return mul(x, x)

def fib3(n):
    f1 = [1, 1, 1]
    t = [
        [0, 1, 0], 
        [0, 0, 1],
        [1, 1, 1]
    ]
    if n == 1:
        return 1
    t = pow(t, n - 1)
    r = 0
    for i in range(K):
        r += t[0][i] * f1[i]
    return r

# https://stackoverflow.com/a/40117659/12584325
def huge_fib():
    # Initialize a matrix [[1,1],[1,0]]
    v1, v2, v3 = 1, 1, 0
    # Perform fast exponentiation of the matrix (quickly raise it to the nth power)
    for rec in bin(n)[3:]:
        calc = (v2*v2) % m
        v1, v2, v3 = (v1*v1+calc) % m, ((v1+v3)*v2) % m, (calc+v3*v3) % m
        if rec == '1':
            v1, v2, v3 = (v1+v2) % m, v1, v2
    return v2

def huge_fib3():
    pass



