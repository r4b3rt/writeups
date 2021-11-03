#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 8

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
    unsigned char s[MAX] = {7, 6, 2, 5, 1, 0, 3, 4};
	char enc[40] = "kfggtb}thiu[jtXU@2Xeu{uu|\x00";
	unsigned long len = strlen(enc);
	printf("%d\n", len);
    rc4_crypto(s, (unsigned char *)enc, len);
    printf("%s\n", enc);
    return 0;
}
