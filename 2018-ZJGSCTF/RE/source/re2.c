#include<stdio.h>
#include<string.h>
#include<malloc.h>
#include<stdlib.h>
char *table="ABCDEFGHIJSTUVWKLMNOPQRXYZabcdqrstuvwxefghijklmnopyz0123456789+/";
char *secret="\x20\xc3\x1a\xae\x97\x3c\x7a\x41\xde\xf6\x78\x15\xcb\x4b\x4c\xdc\x26\x55\x8b\x55\xe5\xe9\x55\x75\x40\x3d\x82\x13\xa5\x60\x13\x3b\xf5\xd8\x19\x0e\x47\xcf\x5f\x5e\xde\x9d\x14\xbd";

typedef unsigned longULONG;
/*初始化函数*/
void rc4_init(unsigned char*s, unsigned char*key, unsigned long Len)
{
    int i = 0, j = 0;
    char k[256] = { 0 };
    unsigned char tmp = 0;
    for (i = 0; i<256; i++)
    {
        s[i] = i;
        k[i] = key[i%Len];
    }
    for (i = 0; i<256; i++)
    {
        j = (j + s[i] + k[i]) % 256;
        tmp = s[i];
        s[i] = s[j];//交换s[i]和s[j]
        s[j] = tmp;
    }
}
 
/*加解密*/
void rc4_crypt(unsigned char*s, unsigned char*Data, unsigned long Len)
{
    int i = 0, j = 0, t = 0;
    unsigned long k = 0;
    unsigned char tmp;
    for (k = 0; k<Len; k++)
    {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        tmp = s[i];
        s[i] = s[j];//交换s[x]和s[y]
        s[j] = tmp;
        t = (s[i] + s[j]) % 256;
        Data[k] ^= s[t];
    }
}


char *base64_encode(const char *src)  
{  
    int count;  
    long tmp, buf;  
    char in[4];  
    char *dst;
    int i, j;  
  
    count = strlen(src) / 3 + (strlen(src) % 3 ? 1 : 0);  
    dst = (char*)malloc((count * 4 + 1));  
    memset(dst, 0, count * 4 + 1);  
      
  
    for(j = 0; j < count; j++)  
    {  
        memset(in, 0, sizeof(in));  
        strncpy(in, src + j * 3, 3);  
  
        buf = 0;  
        for(i = 0; i < strlen(in); i++)  
        {  
            tmp = (long)in[i];  
            tmp <<= (16 - i * 8);  
            buf |= tmp;  
        }  
  
        for(i = 0; i < 4; i++)  
        {  
            if(strlen(in) + 1 > i)  
            {  
                tmp = buf >> (18 - 6 * i);  
                tmp &= 0x3f;  
                dst[j * 4 + i] = table[tmp];  
            }  
            else  
            {  
                dst[j * 4 + i] = '=';  
            }  
        }  
  
    }   
	
	return dst;
}  
void ck(char *enc)
{
	int i;
	for(i=0;i<44;i++)
	{
		//printf("\\x%x",enc[i]&0xff);
		if(enc[i]!=secret[i])
		{
			exit(0);
		}
	}
	printf("Congratulation!!!!!!\n");

}

int main()
{
    unsigned char s[256] = { 0 }, s2[256] = { 0 };//S-box
    char key[256] = { "flag{this_is_not_the_flag_hahaha}" };
    char pData[50];
    unsigned long len;
    char *enc1;
	int i;
    //flag{y0u_know_rc4_and_base64_ha$}
    printf("input flag:\n");
    scanf("%50s",pData); 
    __asm{
		push eax
		xor eax,eax
		jz	betamao
		add esp,30
	    betamao:
		pop eax
	}
    len = strlen(pData);
    if(len!=33)
    {
        return 0;
    } 
    enc1=base64_encode(pData);  

    rc4_init(s, (unsigned char*)key, strlen(key));//已经完成了初始化
    rc4_crypt(s, (unsigned char*)enc1, strlen(enc1));//加密

    ck(enc1);
    return 0;
}