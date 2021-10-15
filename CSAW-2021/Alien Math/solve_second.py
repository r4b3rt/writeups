#!/usr/bin/env python

# arr[idx+1]=(func(arr[idx],arr[idx]+idx)+arr[idx+1]) % 10

def func(a, b):
    return (a * 0x30 + b * 0xb - 4) % 10

target = '3436303439353737'.decode('hex')[::-1] + '3332333535323538'.decode('hex')[::-1] + '353232393232'.decode('hex')[::-1]
print target
print len(target)

cur = 7
arr = [cur] + [0 for _ in range(21)]
for i in range(21):
    func_x = func(cur, cur + i)
    for j in range(10):
        if int(target[i + 1]) == (func_x + j) % 10:
            cur = int(target[i + 1])
            arr[i + 1] = j
            break

print arr
print ''.join([str(c) for c in arr])

