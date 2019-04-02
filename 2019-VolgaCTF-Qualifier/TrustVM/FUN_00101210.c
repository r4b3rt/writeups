
void * FUN_00101210(char *param_1,ulong *param_2)

{
  FILE *__stream;
  size_t __n;
  void *__ptr;
  size_t sVar1;
  ulong __size;
  long lVar2;
  
  __stream = fopen(param_1,"rb");
  if (__stream != (FILE *)0x0) {
    fseek(__stream,0,2);
    __n = ftell(__stream);
    __size = __n + 0x3f & 0xffffffffffffffc0;
    if (param_2 != (ulong *)0x0) {
      *param_2 = __size;
    }
    rewind(__stream);
    __ptr = malloc(__size);
    if (0 < (long)__n) {
      lVar2 = 0;
      do {
        sVar1 = fread(__ptr,1,__n,__stream);
        lVar2 = lVar2 + sVar1;
      } while (lVar2 < (long)__n);
    }
    fclose(__stream);
    return __ptr;
  }
  __printf_chk(1,"Can\'t open file %s\n",param_1);
                    /* WARNING: Subroutine does not return */
  exit(1);
}

