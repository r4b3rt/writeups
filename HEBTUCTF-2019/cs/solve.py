#!/usr/bin/env python
import base64

flag1 = base64.b64decode(base64.b64decode('Wm14aFp5VTNRalpBTldWaU5BJTNEJTNE').replace('%3D', '='))
flag2 = '&c0nfu'
flag3 = 's10n'
flag = flag1 + flag2 + flag3 + '}'
flag = flag.replace('%7B', '{')
print flag

