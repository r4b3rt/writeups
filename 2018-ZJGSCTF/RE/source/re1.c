#include<stdio.h>
void ck1(char *enc,int len)
{
	int i=0;
	for(i=0;i<len;i++)
	{
		enc[i]=(enc[i]^0x30)+1;
	}
}
int main()
{
	//flag{Welcome_t0_re_this_is_only_asm}
    char enc[37]="\x55\x5b\x50\x56\x4a\x66\x54\x5b\x52\x5e\x5c\x54\x6e\x43\x1f\x6e\x41\x54\x6e\x43\x57\x58\x42\x6e\x58\x42\x6e\x5e\x5d\x5b\x48\x6e\x50\x42\x5c\x4c";
	ck1(enc,36);
	printf("%s\n",enc);
	return 0;
}