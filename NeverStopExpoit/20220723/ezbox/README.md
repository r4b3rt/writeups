# 题目考点

- Shellcode编写利用
- Seccomp沙箱绕过

# 解题思路

题目中提供了flag字符串在内存中的地址，并要求输入一串shellcode，并在一个子进程中设置了Seccomp沙箱来执行shellcode。由于设置了`SECCOMP_MODE_STRICT`，且关闭了标准输入输出流，无法直接输出flag的值，可以利用父进程判断子进程是否正常结束的代码，来逐字符爆破flag。

1. 获取flag字符串在内存中的地址；
2. 编写逐字符比较flag的shellcode，构成循环对flag进行爆破。

# 预估难度

中

