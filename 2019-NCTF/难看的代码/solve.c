#include<stdio.h>
#include<stdlib.h>
#include<string.h>
unsigned char dword_403020[] =
{
  0x78, 0x56, 0x34, 0x12, 0x0D, 0xF0, 0xAD, 0x0B, 0x14, 0x13,
  0x20, 0x05, 0x21, 0x43, 0x65, 0x87
};
void decrypt (char* a1, unsigned int* k) {
    unsigned int v0=*(unsigned int *)a1, v1=*(unsigned int *)(a1+4), sum=0xC6EF3720, i;  /* set up */
    unsigned int delta=0x9e3779b9;                     /* a key schedule constant */
    unsigned int k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    *(unsigned int *)a1=v0; *(unsigned int *)(a1+4)=v1;
}
int main()
{
    unsigned char a1[] = {0x5E, 0x9F, 0x86, 0x61, 0x8D, 0xF0, 0x9C, 0x0A, 0xCA, 0xC0,
  0x74, 0xAD, 0xB8, 0x16, 0x7F, 0xA5, 0x6D, 0x62, 0x59, 0xB5,
  0xE0, 0x68, 0x7B, 0xD1};
  int i,j;
  for(j=0;j<24;j+=8)
  {
  decrypt(a1+j, &dword_403020);
  }

  for(j=0;j<24;j++)
  {
      a1[j] ^= 0x5Au;
      a1[j] = ((a1[j] >> 3) | (a1[j]<<5))&0xff;
  }
    for ( i = 0; i < 6; i += 4 )
  {
    a1[i] -= 0xC;
    a1[i + 1] -= 0x22;
    a1[i + 2] -= 0x38;
    a1[i + 3] -= 0x4E;
  }
  for(i=0;i<24;i++)
    printf("%c",a1[i]);
    return 0;
}
