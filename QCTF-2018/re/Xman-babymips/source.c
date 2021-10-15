//qctf{ReA11y_4_B@89_mlp5_4_XmAn_}
#include <stdio.h>
#include <string.h>
char *check1="Q|j{g";
char *check2= "\x52\xfd\x16\xa4\x89\xbd\x92\x80\x13\x41\x54\xa0\x8d\x45\x18\x81\xde\xfc\x95\xf0\x16\x79\x1a\x15\x5b\x75\x1f";
void check(char *s){
    int i;
    for(i=5;i<strlen(s);i++){
    	if(i%2)
    		s[i]=(s[i]>>2)|((s[i]<<6)&0xff);
    	else
    		s[i]=((s[i]<<2)&0xff)|(s[i]>>6);	
    }
    if(!strncmp(&s[5],check2,27))
   		printf("Right!\n");
   	else
   		printf("Wrong!\n");
}
void main(){
    char s[33];
   	int i;
   	printf("Give me your flag:");
   	scanf("%32s",s);
   	for(i=0;i<32;i++)
   		s[i]^=(32-i);
   	if(!strncmp(s,check1,5))
   		check(s);
   	else
   		printf("Wrong\n");
}