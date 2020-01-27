#!/usr/bin/env python
with open('analytics.js', 'rb') as f:
    ciphertext = f.read()[:-1]
ciphertext = ''.join([chr(ord(c) ^ 104) for c in ciphertext])
print ciphertext

blah = 'U3RyaW5nLnJhd2BycIFsmVVEMVV9lTBXTlV9V219VDCAfU5tlX11MDJ9M1WfYC5zcGxpdGBgLm1hcChpPT4oW2EsYixjXT0n'.decode('base64')[11:-27].encode('base64')
print blah

