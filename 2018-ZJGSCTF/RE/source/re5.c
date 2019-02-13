#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
char data[50];
int b[8][8]={
{ 0x2B, 0x16, 0x1E, 0x53, 0x35, 0x39, 0x20, 0x29 },
{ 0x35, 0x63, 0x0A, 0x28, 0x2C, 0x06, 0x32, 0x2A },
{ 0x55, 0x39, 0x14, 0x5F, 0x20, 0x19, 0x34, 0x21 },
{ 0x19, 0x0B, 0x5A, 0x09, 0x50, 0x34, 0x6F, 0x5C },
{ 0x16, 0x1A, 0x68, 0x63, 0x34, 0x4E, 0x16, 0x45 },
{ 0x4C, 0x53, 0x2F, 0x3F, 0x3F, 0x28, 0x69, 0x51 },
{ 0x39, 0x44, 0x12, 0x24, 0x0A, 0x4D, 0x55, 0x31 },
{ 0x49, 0x3B, 0x40, 0x3B, 0x43, 0x28, 0x21, 0x36 }
};
int enc_flag[8][8]={
{39430, 34714, 32196, 36639, 34988, 34059, 30813, 33326,}, 
{36796, 32617, 33253, 34580, 34162, 34694, 27284, 30462,}, 
{43121, 39454, 38526, 40343, 40267, 39622, 32312, 35938,}, 
{52554, 37142, 43063, 43360, 41895, 39806, 44188, 43934,}, 
{51532, 44412, 41672, 48518, 45549, 44436, 41365, 45032,}, 
{60785, 49721, 52606, 54361, 52991, 52156, 47474, 50031,}, 
{43050, 35311, 36031, 39633, 34447, 34470, 31270, 31954,},
{49152, 43386, 42096, 46024, 45029, 43961, 36733, 42762,}
};
void ck1(char *enc,int len)
{
    int i;
    unsigned char tmp;
    for(i=0;i<len;i++)
    {
    	tmp=enc[i]+13;
    	if(enc[i] >= 97 && enc[i] <= 122)
    	{   
        	if (tmp > 122)
        	{
        		tmp = tmp - 26;
        	}
   		}else if(enc[i] >= 65 && enc[i] <= 90){
   			if(tmp > 90)
        	{
            	tmp = tmp- 26;
        	}
   		}else
		{
			tmp=enc[i];
		}
   		enc[i] = tmp;
    }
}

void ck2(int enc2[][8],char *enc1)
{
	int i=0,j=0,k=0;
	for(j=0;j<8;j++)
	{
		for(i=0;i<8;i++)
		{
			enc2[j][i]=(int)enc1[k++];
		}
	}

}
void ck3(int b[][8], int c[][8], int a[][8], int nx, int ny, int nk)
{
	int i, j, k;
	for (j = 0; j<ny; j++)
	{
		for (i = 0; i<nx; i++)
		{
			a[j][i] = 0;
		}
	}

	for (j = 0; j<ny; j++)
	{
		for (i = 0; i<nx; i++)
		{
			for (k = 0; k<nk; k++)
			{
				a[j][i] += b[j][k] * c[k][i];
			}
		}
	}
}

int ck4(int a[][8])
{
	int i, j, k;
	for (j = 0; j<8; j++)
	{
		for (i = 0; i<8; i++)
		{
			if(a[j][i]!=enc_flag[j][i])
			{
				return 0;
			}
		}
	}
	return 1;
}
int main()
{
    	int n;
    	int fd[2];
	int len=0;
	char flag[70];
	int enc[8][8];
	int a[8][8];
    	char buff[128] = {0};

 	pid_t pid;
	printf("input flag:\n");
	//#flag{y0u_are_g0Od_for_Math_this_is_Matrix_5f0256b0f586a7b55dasd}
        scanf("%70s",flag);
	len=strlen(flag);
	if(len!=64)
	{
		return 0;
	}

 	if(pipe(fd)<0)
 	{
 		exit(1);
 	}
    	if((pid=fork())<0)
    	{
        	exit(1);
    	}
    	if( pid>0 )
    	{
        	close(fd[0]);	
		ck1(flag,len);
        	write(fd[1],flag,len);
        	wait(NULL);
    	}
    	else
    	{
        	close(fd[1]);
        	len=read(fd[0],flag,len);
		ck2(enc,flag);
		ck3(b,enc,a,8,8,8);
		if(ck4(a))
		{
			printf("Congratulate!!!");
		}
    	}
    	return 0;
}
