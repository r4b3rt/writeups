import hashlib
import sympy as sy
x = sy.Symbol('x')
f = (1-sy.E**sy.tan(x))/(sy.asin(x/2))
ans = str(sy.limit(f, x, 0, dir='+'))
flag = 'LCTF{' + hashlib.md5(ans).hexdigest() + '}'
print flag