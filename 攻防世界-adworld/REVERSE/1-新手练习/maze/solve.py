#!/usr/bin/env python
'''
  ******
*   *  *
*** * **
**  * **
*  *#  *
** *** *
**     *
********
left - O
down - 0
right - o
up - .
'''
flag = 'nctf{o0oo00O000oooo..OO}'
assert len(flag) == 24
maze = [
    [' ', ' ', '*', '*', '*', '*', '*', '*'],
    ['*', ' ', ' ', ' ', '*', ' ', ' ', '*'],
    ['*', '*', '*', ' ', '*', ' ', '*', '*'],
    ['*', '*', ' ', ' ', '*', ' ', '*', '*'],
    ['*', ' ', ' ', '*', '#', ' ', ' ', '*'],
    ['*', '*', ' ', '*', '*', '*', ' ', '*'],
    ['*', '*', ' ', ' ', ' ', ' ', ' ', '*'],
    ['*', '*', '*', '*', '*', '*', '*', '*']
]
directions = flag[5:-1]
i, j = 0, 0
for d in directions:
    if d == 'O':
        j -= 1
    elif d == '0':
        i += 1
    elif d == 'o':
        j += 1
    elif d == '.':
        i -= 1
    if maze[i][j] == '#' and d == len(directions) - 1:
        print 'success'
        break
    if maze[i][j] == '*':
        print 'failed'
        assert False
print flag
