
void FUN_001012e0(uint param_1,undefined8 param_2,undefined8 param_3)

{
  long lVar1;
  
  _DT_INIT();
  lVar1 = 0;
  do {
    (*(code *)(&__DT_INIT_ARRAY)[lVar1])((ulong)param_1,param_2,param_3);
    lVar1 = lVar1 + 1;
  } while (lVar1 != 2);
  return;
}

