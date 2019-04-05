#!/usr/bin/env python
with open('flag.txt', 'rb') as f:
    content = f.read().split('.')
    nums = []
    for s in content:
        nums.append(int(s))
    key = int(chr(nums[-1] - 49))
    print key
    nums = nums[:-1]
    flag = ''
    for n in nums:
        flag += chr(n + key)
print flag
