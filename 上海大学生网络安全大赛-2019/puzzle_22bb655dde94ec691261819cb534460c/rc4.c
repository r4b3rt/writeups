#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 256

void rc4_init(unsigned char *sbox, unsigned char *key, unsigned long len)
{
    int j = 0;
    char t[MAX] = {0};
    unsigned char tmp = 0;
    for(int i = 0; i < MAX; i++)//初始化算法
    {
        sbox[i] = i;
        t[i] = key[i % len];
    }
    for(int i = 0; i < MAX; i++)//伪随机子密码生成算法
    {
        j = (j + sbox[i] + t[i]) % MAX;
        tmp = sbox[i];
        sbox[i] = sbox[j];
        sbox[j] = tmp;
    }
}

unsigned char rc4_crypto(unsigned char *sbox, unsigned char *data, unsigned long len)
{
    int i = 0, j = 0;
    unsigned char tmp = 0;
    unsigned long k = 0;
    for(k = 0; k < len; k++)
    {
        i = (i + 1) % MAX;
        j = (j + sbox[i]) % MAX;
        tmp = sbox[i];
        sbox[i] = sbox[j];
        sbox[j] = tmp;
        int t = (sbox[i] + sbox[j]) % MAX;
        data[k] ^= sbox[t];
    }
}

int main()
{
    unsigned char s[MAX] = {0};
    char key[MAX] = "qweee\x00";
	char data[2 * MAX] = "61495072\x00";
    unsigned long len = strlen(data);
    rc4_init(s, (unsigned char *)key, strlen(key));
    rc4_crypto(s, (unsigned char *)data, len);
	printf("%d\n", len);
    printf("%s\n", data);
	for(int i = 0; i < len; i++) {
		printf("%x", data[i]&0xFF);
	}
	printf("\n");
    return 0;
}
