#!/usr/bin/env python
with open('cipher.txt', 'rb') as f:
    c = f.read()
    dic = {
        'c':'t', 'C':'T', 
        's':'h', 'S':'H', 
        'j':'e', 'J':'E', 
        'm':'f', 'M':'F', 
        'e':'l', 'E':'L', 
        'x':'a', 'X':'A', 
        'p':'g', 'P':'G', 
        'v':'i', 'V':'I', 
        'z':'s', 'Z':'S', 
        'g':'d', 'G':'D', 
        'w':'r', 'W':'R', 
        'k':'n', 'K':'N', 
        'd':'c', 'D':'C', 
        'q':'p', 'Q':'P', 
        'n':'o', 'N':'O', 
        'h':'m', 'H':'M'
    }
    res = ''
    for i in range(len(c)):
        flag = 0
        for key, val in dic.items():
            if c[i] == key:
                res += val
                flag = 1
        if flag == 1:
            continue
        else:
            res += c[i]
    print res
