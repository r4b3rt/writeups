#!/usr/bin/env python
with open('README.md', 'rb') as f:
    ciphertext = f.readlines()[5][:-2]
plaintext = ciphertext.encode('base64')
print plaintext

