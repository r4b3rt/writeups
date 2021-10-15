#include <iostream>
#include <stdio.h>

/* run this program using the console pauser or add your own getch, system("pause") or input loop */

int main(int argc, char** argv) {
  signed int i; // [rsp+1Ch] [rbp-3Ch]
  signed int j; // [rsp+1Ch] [rbp-3Ch]
  unsigned int v4; // [rsp+20h] [rbp-38h]
  unsigned int v5; // [rsp+20h] [rbp-38h]
  unsigned int v6; // [rsp+24h] [rbp-34h]
  unsigned int v7; // [rsp+24h] [rbp-34h]
  unsigned int v8; // [rsp+28h] [rbp-30h]
  unsigned int v9; // [rsp+28h] [rbp-30h]
  unsigned int v10; // [rsp+2Ch] [rbp-2Ch]
  unsigned int v11; // [rsp+30h] [rbp-28h]
  int key[4]; // [rsp+38h] [rbp-20h]
  unsigned int pass[2];
  pass[0] = 0xD2A65C14;
  pass[1] = 0x7709450E;

  v10 = *pass;
  v11 = pass[1];
  key[0] = 0x28371234;
  key[1] = 0x19283543;
  key[2] = 0x19384721;
  key[3] = 0x98372612;
  v4 = *pass;
  v6 = pass[1];
  v8 = 3337565984;
  for ( i = 0; i <= 31; ++i )
  {
    v6 -= (((v4 >> 5) ^ 16 * v4) + v4) ^ (key[(v8 >> 11) & 3] + v8);
    v8 += 0x61C88647;
    v4 -= (((v6 >> 5) ^ 16 * v6) + v6) ^ (key[v8 & 3] + v8);
  }
  *pass = v4;
  pass[1] = v6;
  v5 = v10;
  v7 = v11;
  v9 = 0xe26b8e29;
  for ( j = 0; j <= 8; ++j )
  {
    v7 -= (((v5 >> 5) ^ 16 * v5) + v5) ^ (key[(v9 >> 11) & 3] + v9);
    v9 -= 0x19286521;
    v5 -= (((v7 >> 5) ^ 16 * v7) + v7) ^ (key[v9 & 3] + v9);
  }
  *pass = v5;
  pass[1] = v7;
  printf("%s\n", (char *) pass);
}

