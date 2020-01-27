#!/usr/bin/env python
import re
pat = re.compile(r'rtcp\{.{1,20}_.{1,20}\}')
with open('worbz.txt', 'rb') as f:
    print pat.findall(f.read())[0]

