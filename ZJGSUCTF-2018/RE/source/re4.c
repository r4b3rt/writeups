#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#pragma comment(linker, "/SECTION:.text,ERWS")
char *table="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
void ck4(char *enc)
{
	char map[]={
 "--------"
 "g +    +"
 "+ + ++ +"
 "+ + #+ +"
 "+ ++++ +"
 "+ ++++ +"
 "+      +"
 "--------"};
	int i=0,j=0,len=22;
	char k[25]; 
	char z[4]={'a','q','w','2'};
	int n=8;	

	for(i=17;i<39;i++)
	{
		k[j++]=enc[i];
	}
	for(i=0;i<len;i++)
	{
		if(k[i]==z[0])
			n=n+8;
		else if(k[i]==z[1])
			n=n-1;
		else if(k[i]==z[2])
			n=n+1;
		else if(k[i]==z[3])
			n=n-8;
		if(map[n]=='#')
		{
			printf("Congratulation!!!!!!\n");
			exit(0);
		}
		if(map[n]!=' ')
		{
			exit(0);
		}
	}

}

void ck3(char *enc)  
{  
    int count;  
    long tmp, buf;  
    char in[4];  
    char src[7];
	char *dst;
    char enc3[]="\x63\x31\x39\x7a\x62\x57\x4e\x66";
    int i, j=0;  
    for(i=11;i<17;i++)
	{
		src[j++]=enc[i];
	}

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

    for(i=0;i<6;i++)
	{
		if(enc3[i]!=dst[i])
		{
			exit(0);
		}
	}

	ck4(enc);
}  

void ck2(char *enc)
{
	int i,j=0;
	char *enc2="\xf2\xee\xef\xf5\xd9\xef";
	for(i=5;i<11;i++)
	{
		if((enc[i]^0x86)!=(enc2[j++]&0xff))
		{					
			exit(0);
		}
	}

	ck3(enc);
}

void ck1(char *enc)
{
	int i;
	char enc1[]="flag{}";
	for(i=0;i<5;i++)
	{
		if(enc[i]!=enc1[i])
		{
			exit(0);
		}
	}
	if(enc[39]!=enc1[i])exit(0);
	ck2(enc);
}
void ck_e(char *enc){}

int main()
{
	char *lp_s = 0;
	char *lp_e = 0;
	int i,len=0;
	char enc[50]={0};
	//flag{this_is_smc_waaaaawwwww22222qqqaaw}
	printf("input flag:\n");
    scanf("%50s",enc);
    if(strlen(enc)!=40)
    {
    	return 0;
    } 
	lp_s = (char *)ck4;  //获取需要加密函数的起始地址
	lp_e = (char *)ck_e;  //获取需要加密函数的结束地址
	len=lp_e-lp_s;
	for(i=0;i<len;i++) //这里对地址进行简单的加密>
	{
		*(lp_s+i) ^=0xbb;
	}
	ck1(enc);
	return 0;
}