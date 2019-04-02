
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_00100900(int param_1,undefined8 *param_2)

{
  char *pcVar1;
  undefined auVar2 [16];
  undefined auVar3 [16];
  undefined auVar4 [16];
  undefined auVar5 [16];
  undefined auVar6 [16];
  undefined auVar7 [16];
  undefined auVar8 [16];
  undefined auVar9 [16];
  byte bVar10;
  byte bVar11;
  ushort uVar12;
  ulong uVar13;
  char cVar14;
  undefined4 *puVar15;
  undefined *puVar16;
  int iVar17;
  undefined8 *puVar18;
  ushort *__ptr;
  void *__ptr_00;
  FILE *__s;
  undefined8 uVar19;
  byte *pbVar20;
  undefined8 *puVar21;
  byte bVar22;
  long lVar23;
  uint uVar24;
  uint uVar25;
  long lVar26;
  ushort *puVar27;
  long in_FS_OFFSET;
  size_t local_560;
  undefined4 local_558;
  undefined4 uStack1364;
  undefined4 uStack1360;
  undefined4 uStack1356;
  undefined4 local_548;
  undefined4 uStack1348;
  undefined4 uStack1344;
  undefined4 uStack1340;
  undefined4 local_538;
  undefined4 uStack1332;
  undefined4 uStack1328;
  undefined4 uStack1324;
  undefined4 local_528;
  undefined4 uStack1316;
  undefined4 uStack1312;
  undefined4 uStack1308;
  undefined8 local_158 [2];
  char local_148 [264];
  long local_40;
  
  local_40 = *(long *)(in_FS_OFFSET + 0x28);
  if (param_1 != 3) {
    __printf_chk(1,"Usage:\n\t%s progname filetoprocess\n",*param_2);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  lVar23 = 0x82;
  puVar21 = (undefined8 *)&local_558;
  while (puVar18 = (undefined8 *)&local_558, lVar23 != 0) {
    lVar23 = lVar23 + -1;
    *puVar21 = 0;
    puVar21 = puVar21 + 1;
  }
  do {
    puVar21 = puVar18 + 8;
    *(undefined4 *)puVar18 = 0;
    *(undefined4 *)((long)puVar18 + 4) = 0;
    *(undefined4 *)(puVar18 + 1) = 0;
    *(undefined4 *)((long)puVar18 + 0xc) = 0;
    *(undefined4 *)(puVar18 + 2) = 0;
    *(undefined4 *)((long)puVar18 + 0x14) = 0;
    *(undefined4 *)(puVar18 + 3) = 0;
    *(undefined4 *)((long)puVar18 + 0x1c) = 0;
    *(undefined4 *)(puVar18 + 4) = 0;
    *(undefined4 *)((long)puVar18 + 0x24) = 0;
    *(undefined4 *)(puVar18 + 5) = 0;
    *(undefined4 *)((long)puVar18 + 0x2c) = 0;
    *(undefined4 *)(puVar18 + 6) = 0;
    *(undefined4 *)((long)puVar18 + 0x34) = 0;
    *(undefined4 *)(puVar18 + 7) = 0;
    *(undefined4 *)((long)puVar18 + 0x3c) = 0;
    puVar18 = puVar21;
  } while (puVar21 != local_158);
  lVar23 = 0x82;
  puVar21 = (undefined8 *)&local_558;
  puVar18 = &DAT_00302040;
  while (lVar23 != 0) {
    lVar23 = lVar23 + -1;
    *puVar18 = *puVar21;
    puVar21 = puVar21 + 1;
    puVar18 = puVar18 + 1;
  }
  __ptr = (ushort *)FUN_00101210((char *)param_2[1],(ulong *)0x0);
  __ptr_00 = FUN_00101210((char *)param_2[2],&local_560);
  DAT_003023c0 = SUB81(__ptr_00,0);
  DAT_003023c1 = (undefined)((ulong)__ptr_00 >> 8);
  DAT_003023c2 = (undefined)((ulong)__ptr_00 >> 0x10);
  DAT_003023c3 = (undefined)((ulong)__ptr_00 >> 0x18);
  _DAT_003023f8 = 0;
  _DAT_00302438 = 0;
  DAT_003023c4 = (undefined)((ulong)__ptr_00 >> 0x20);
  DAT_003023c5 = (undefined)((ulong)__ptr_00 >> 0x28);
  DAT_003023c6 = (undefined)((ulong)__ptr_00 >> 0x30);
  DAT_003023c7 = (undefined)((ulong)__ptr_00 >> 0x38);
  _DAT_003023c8 = 0;
  DAT_003023cc = 0;
  DAT_003023d0 = 0;
  DAT_003023d4 = 0;
  DAT_00302401 = (undefined)(local_560 >> 8);
  DAT_00302400 = (undefined)local_560;
  DAT_00302402 = (undefined)(local_560 >> 0x10);
  DAT_00302403 = (undefined)(local_560 >> 0x18);
  DAT_00302404 = (undefined)(local_560 >> 0x20);
  DAT_00302405 = (undefined)(local_560 >> 0x28);
  DAT_003023e0 = 0;
  DAT_003023e4 = 0;
  DAT_00302407 = (undefined)(local_560 >> 0x38);
  DAT_003023f0 = 0;
  DAT_003023f4 = 0;
  DAT_00302410 = 0;
  DAT_00302414 = 0;
  DAT_00302420 = 0;
  DAT_00302424 = 0;
  DAT_00302430 = 0;
  DAT_00302434 = 0;
  DAT_00302406 = (undefined)(local_560 >> 0x30);
  puVar27 = __ptr;
  _DAT_003023d8 = _DAT_003023c8;
  DAT_003023dc = DAT_003023cc;
  _DAT_003023e8 = _DAT_003023c8;
  DAT_003023ec = DAT_003023cc;
  _DAT_00302408 = _DAT_003023c8;
  DAT_0030240c = DAT_003023cc;
  _DAT_00302418 = _DAT_003023c8;
  DAT_0030241c = DAT_003023cc;
  _DAT_00302428 = _DAT_003023c8;
  DAT_0030242c = DAT_003023cc;
  _DAT_00302448 = __ptr;
LAB_00100ad0:
  uVar12 = *puVar27;
  DAT_00302440 = puVar27 + 1;
  local_558 = 0;
  uStack1364 = 0;
  uStack1360 = 0;
  uStack1356 = 0;
  uVar13 = (ulong)(uVar12 >> 0xc);
  uVar24 = (int)(uint)uVar12 >> 4 & 0xf;
  uVar25 = (int)(uint)uVar12 >> 8 & 0xf;
  local_548 = 0;
  uStack1348 = 0;
  uStack1344 = 0;
  uStack1340 = 0;
  local_538 = 0;
  uStack1332 = 0;
  uStack1328 = 0;
  uStack1324 = 0;
  local_528 = 0;
  uStack1316 = 0;
  uStack1312 = 0;
  uStack1308 = 0;
  switch((uint)uVar12 & 0xf) {
  case 0:
    lVar23 = 0;
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302040 + (long)(int)uVar25 * 8);
    uVar25 = 0;
    do {
      uVar25 = uVar25 + (uint)*(byte *)((long)&local_558 + lVar23) +
                        (uint)*(byte *)((long)&DAT_00302040 + lVar23 + uVar13 * 0x40);
      *(undefined *)((long)&local_558 + lVar23) = (char)uVar25;
      uVar25 = uVar25 >> 8;
      lVar23 = lVar23 + 1;
    } while (lVar23 != 0x40);
    puVar16 = SUB168(auVar2,0);
    lVar23 = (long)(int)uVar24;
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)puVar16;
    *(int *)(&DAT_00302040 + lVar23 * 8) = SUB164(auVar2,0);
    *(undefined4 *)((long)&DAT_00302040 + lVar23 * 0x40 + 4) = SUB164(auVar2 >> 0x20,0);
    (&DAT_00302048)[lVar23 * 0x10] = SUB164(auVar2 >> 0x40,0);
    (&DAT_0030204c)[lVar23 * 0x10] = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(puVar16 + 0x10);
    (&DAT_00302050)[lVar23 * 0x10] = SUB164(auVar2,0);
    (&DAT_00302054)[lVar23 * 0x10] = SUB164(auVar2 >> 0x20,0);
    (&DAT_00302058)[lVar23 * 0x10] = SUB164(auVar2 >> 0x40,0);
    (&DAT_0030205c)[lVar23 * 0x10] = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(puVar16 + 0x20);
    (&DAT_00302060)[lVar23 * 0x10] = SUB164(auVar2,0);
    (&DAT_00302064)[lVar23 * 0x10] = SUB164(auVar2 >> 0x20,0);
    (&DAT_00302068)[lVar23 * 0x10] = SUB164(auVar2 >> 0x40,0);
    (&DAT_0030206c)[lVar23 * 0x10] = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(puVar16 + 0x30);
    (&DAT_00302070)[lVar23 * 0x10] = SUB164(auVar2,0);
    (&DAT_00302074)[lVar23 * 0x10] = SUB164(auVar2 >> 0x20,0);
    (&DAT_00302078)[lVar23 * 0x10] = SUB164(auVar2 >> 0x40,0);
    (&DAT_0030207c)[lVar23 * 0x10] = SUB164(auVar2 >> 0x60,0);
    puVar27 = DAT_00302440;
    goto LAB_00100ad0;
  case 1:
    lVar23 = 0;
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302040 + (long)(int)uVar24 * 8);
    uVar24 = 0;
    do {
      uVar24 = uVar24 + (uint)*(byte *)((long)&local_558 + lVar23) +
                        (uint)*(byte *)((long)&DAT_00302040 + lVar23 + (long)(int)uVar25 * 0x40);
      *(undefined *)((long)&local_558 + lVar23) = (char)uVar24;
      uVar24 = uVar24 >> 8;
      lVar23 = lVar23 + 1;
    } while (lVar23 != 0x40);
    puVar15 = SUB168(auVar2,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302040 + uVar13 * 8);
    *puVar15 = SUB164(auVar2,0);
    puVar15[1] = SUB164(auVar2 >> 0x20,0);
    puVar15[2] = SUB164(auVar2 >> 0x40,0);
    puVar15[3] = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302050 + uVar13 * 0x10);
    puVar15[4] = SUB164(auVar2,0);
    puVar15[5] = SUB164(auVar2 >> 0x20,0);
    puVar15[6] = SUB164(auVar2 >> 0x40,0);
    puVar15[7] = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302060 + uVar13 * 0x10);
    puVar15[8] = SUB164(auVar2,0);
    puVar15[9] = SUB164(auVar2 >> 0x20,0);
    puVar15[10] = SUB164(auVar2 >> 0x40,0);
    puVar15[0xb] = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302070 + uVar13 * 0x10);
    puVar15[0xc] = SUB164(auVar2,0);
    puVar15[0xd] = SUB164(auVar2 >> 0x20,0);
    puVar15[0xe] = SUB164(auVar2 >> 0x40,0);
    puVar15[0xf] = SUB164(auVar2 >> 0x60,0);
    puVar27 = DAT_00302440;
    goto LAB_00100ad0;
  case 2:
    lVar23 = (long)(int)uVar24;
    puVar21 = &DAT_00302040 + lVar23 * 8;
    do {
      puVar27 = DAT_00302440;
      if (*(char *)puVar21 !=
          *(char *)(puVar21 + lVar23 * 0x1ffffffffffffff8 + (long)(int)uVar25 * 8))
      goto LAB_00100ad0;
      puVar21 = (undefined8 *)((long)puVar21 + 1);
    } while ((undefined8 *)(&DAT_00302080 + lVar23 * 0x10) != puVar21);
LAB_00100e58:
    lVar23 = uVar13 * 0x40;
    puVar27 = (ushort *)
              (((ulong)*(byte *)((long)&DAT_00302040 + lVar23 + 7) << 0x38 |
               (ulong)*(byte *)((long)&DAT_00302040 + lVar23 + 5) << 0x28 |
               (ulong)*(byte *)((long)&DAT_00302040 + lVar23 + 3) << 0x18 |
               (ulong)*(byte *)((long)&DAT_00302040 + lVar23 + 1) << 8 |
               (ulong)*(byte *)((long)&DAT_00302040 + lVar23 + 2) << 0x10 |
               (ulong)*(byte *)(&DAT_00302040 + uVar13 * 8) |
               (ulong)*(byte *)((long)&DAT_00302040 + lVar23 + 4) << 0x20 |
               (ulong)*(byte *)((long)&DAT_00302040 + lVar23 + 6) << 0x30) + (long)_DAT_00302448);
    goto LAB_00100ad0;
  case 3:
    lVar23 = (long)(int)uVar24 * 0x40;
    pbVar20 = (byte *)((long)&DAT_0030207c + lVar23 + 3);
    do {
      bVar10 = pbVar20[(long)(int)uVar25 * 0x40 + (long)(int)uVar24 * -0x40];
      if (*pbVar20 < bVar10) goto LAB_00100e58;
      puVar27 = DAT_00302440;
    } while ((*pbVar20 < bVar10 || *pbVar20 == bVar10) &&
            (pbVar20 = pbVar20 + -1, puVar27 = DAT_00302440, &DAT_0030203f + lVar23 != pbVar20));
    goto LAB_00100ad0;
  case 5:
    lVar26 = (long)(int)uVar25;
    lVar23 = 0;
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302040 + lVar26 * 8);
    local_558 = SUB164(auVar2,0);
    uStack1364 = SUB164(auVar2 >> 0x20,0);
    uStack1360 = SUB164(auVar2 >> 0x40,0);
    uStack1356 = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302050 + lVar26 * 0x10);
    local_548 = SUB164(auVar2,0);
    uStack1348 = SUB164(auVar2 >> 0x20,0);
    uStack1344 = SUB164(auVar2 >> 0x40,0);
    uStack1340 = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302060 + lVar26 * 0x10);
    local_538 = SUB164(auVar2,0);
    uStack1332 = SUB164(auVar2 >> 0x20,0);
    uStack1328 = SUB164(auVar2 >> 0x40,0);
    uStack1324 = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302070 + lVar26 * 0x10);
    uVar25 = 0;
    local_528 = SUB164(auVar2,0);
    uStack1316 = SUB164(auVar2 >> 0x20,0);
    uStack1312 = SUB164(auVar2 >> 0x40,0);
    uStack1308 = SUB164(auVar2 >> 0x60,0);
    do {
      uVar25 = uVar25 + (uint)*(byte *)((long)&local_558 + lVar23) +
                        (uint)*(byte *)((long)&DAT_00302040 + lVar23 + uVar13 * 0x40);
      *(undefined *)((long)&local_558 + lVar23) = (char)uVar25;
      uVar25 = uVar25 >> 8;
      lVar23 = lVar23 + 1;
    } while (lVar23 != 0x40);
    break;
  case 6:
    lVar26 = (long)(int)uVar25;
    lVar23 = 0;
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302040 + lVar26 * 8);
    local_558 = SUB164(auVar2,0);
    uStack1364 = SUB164(auVar2 >> 0x20,0);
    uStack1360 = SUB164(auVar2 >> 0x40,0);
    uStack1356 = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302050 + lVar26 * 0x10);
    local_548 = SUB164(auVar2,0);
    uStack1348 = SUB164(auVar2 >> 0x20,0);
    uStack1344 = SUB164(auVar2 >> 0x40,0);
    uStack1340 = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302060 + lVar26 * 0x10);
    local_538 = SUB164(auVar2,0);
    uStack1332 = SUB164(auVar2 >> 0x20,0);
    uStack1328 = SUB164(auVar2 >> 0x40,0);
    uStack1324 = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302070 + lVar26 * 0x10);
    uVar19 = 0;
    local_528 = SUB164(auVar2,0);
    uStack1316 = SUB164(auVar2 >> 0x20,0);
    uStack1312 = SUB164(auVar2 >> 0x40,0);
    uStack1308 = SUB164(auVar2 >> 0x60,0);
    while( true ) {
      while( true ) {
        bVar10 = *(byte *)((long)&local_558 + lVar23);
        iVar17 = (int)uVar19 + (uint)*(byte *)((long)&DAT_00302040 + lVar23 + uVar13 * 0x40);
        cVar14 = (char)iVar17;
        if ((ushort)iVar17 <= (ushort)bVar10) break;
        *(char *)((long)&local_558 + lVar23) = bVar10 - cVar14;
        lVar23 = lVar23 + 1;
        if (lVar23 == 0x40) goto LAB_00100c78;
        uVar19 = 1;
      }
      *(char *)((long)&local_558 + lVar23) = bVar10 - cVar14;
      lVar23 = lVar23 + 1;
      if (lVar23 == 0x40) break;
      uVar19 = 0;
    }
    break;
  case 7:
    lVar26 = (long)(int)uVar25;
    lVar23 = (long)(int)uVar24;
                    /* WARNING: Load size is inaccurate */
    auVar2 = *(undefined *)(&DAT_00302040 + lVar26 * 8);
                    /* WARNING: Load size is inaccurate */
    auVar3 = *(undefined *)(&DAT_00302040 + uVar13 * 8);
                    /* WARNING: Load size is inaccurate */
    auVar4 = *(undefined *)(&DAT_00302050 + lVar26 * 0x10);
                    /* WARNING: Load size is inaccurate */
    auVar5 = *(undefined *)(&DAT_00302060 + lVar26 * 0x10);
                    /* WARNING: Load size is inaccurate */
    auVar6 = *(undefined *)(&DAT_00302050 + uVar13 * 0x10);
                    /* WARNING: Load size is inaccurate */
    auVar7 = *(undefined *)(&DAT_00302070 + lVar26 * 0x10);
                    /* WARNING: Load size is inaccurate */
    auVar8 = *(undefined *)(&DAT_00302060 + uVar13 * 0x10);
                    /* WARNING: Load size is inaccurate */
    auVar9 = *(undefined *)(&DAT_00302070 + uVar13 * 0x10);
    *(int *)(&DAT_00302040 + lVar23 * 8) = SUB164(auVar2 ^ auVar3,0);
    *(undefined4 *)((long)&DAT_00302040 + lVar23 * 0x40 + 4) = SUB164((auVar2 ^ auVar3) >> 0x20,0);
    (&DAT_00302048)[lVar23 * 0x10] = SUB164(auVar3 >> 0x40,0);
    (&DAT_0030204c)[lVar23 * 0x10] = SUB164(auVar3 >> 0x60,0);
    (&DAT_00302050)[lVar23 * 0x10] = SUB164(auVar4 ^ auVar6,0);
    (&DAT_00302054)[lVar23 * 0x10] = SUB164((auVar4 ^ auVar6) >> 0x20,0);
    (&DAT_00302058)[lVar23 * 0x10] = SUB164(auVar6 >> 0x40,0);
    (&DAT_0030205c)[lVar23 * 0x10] = SUB164(auVar6 >> 0x60,0);
    (&DAT_00302060)[lVar23 * 0x10] = SUB164(auVar5 ^ auVar8,0);
    (&DAT_00302064)[lVar23 * 0x10] = SUB164((auVar5 ^ auVar8) >> 0x20,0);
    (&DAT_00302068)[lVar23 * 0x10] = SUB164(auVar8 >> 0x40,0);
    (&DAT_0030206c)[lVar23 * 0x10] = SUB164(auVar8 >> 0x60,0);
    (&DAT_00302070)[lVar23 * 0x10] = SUB164(auVar7 ^ auVar9,0);
    (&DAT_00302074)[lVar23 * 0x10] = SUB164((auVar7 ^ auVar9) >> 0x20,0);
    (&DAT_00302078)[lVar23 * 0x10] = SUB164(auVar9 >> 0x40,0);
    (&DAT_0030207c)[lVar23 * 0x10] = SUB164(auVar9 >> 0x60,0);
    puVar27 = DAT_00302440;
    goto LAB_00100ad0;
  case 8:
    lVar23 = 0;
    bVar10 = *(byte *)((long)&DAT_00302040 + uVar13 * 0x40 + 1);
    bVar11 = *(byte *)(&DAT_00302040 + uVar13 * 8);
    bVar22 = bVar11 & 7;
    do {
      iVar17 = (int)lVar23;
      pcVar1 = (char *)((long)(&DAT_00302040 + (long)(int)uVar25 * 8) + lVar23);
      lVar23 = lVar23 + 1;
      *(byte *)((long)&local_558 +
               (ulong)(((int)(((uint)bVar10 & 1) << 8 | (uint)bVar11) >> 3) + iVar17 & 0x3f)) =
           (byte)(((uint)*(byte *)((long)(&DAT_00302040 + (long)(int)uVar25 * 8) +
                                  (ulong)(iVar17 + 0x3fU & 0x3f)) << bVar22) >> 8) |
           *pcVar1 << bVar22;
    } while (lVar23 != 0x40);
    break;
  case 10:
    goto switchD_00100b19_caseD_a;
  case 0xf:
    __sprintf_chk(local_148,1,0x100,"%s.enc",param_2[2]);
    __s = fopen(local_148,"wb");
    if (__s != (FILE *)0x0) {
      fwrite(__ptr_00,1,local_560,__s);
      fclose(__s);
      free(__ptr_00);
      free(__ptr);
      if (local_40 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return 0;
    }
    __printf_chk(1,"Error when trying to create %s\n",local_148);
  default:
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
LAB_00100c78:
  lVar23 = (long)(int)uVar24;
  *(undefined4 *)(&DAT_00302040 + lVar23 * 8) = local_558;
  *(undefined4 *)((long)&DAT_00302040 + lVar23 * 0x40 + 4) = uStack1364;
  (&DAT_00302048)[lVar23 * 0x10] = uStack1360;
  (&DAT_0030204c)[lVar23 * 0x10] = uStack1356;
  (&DAT_00302050)[lVar23 * 0x10] = local_548;
  (&DAT_00302054)[lVar23 * 0x10] = uStack1348;
  (&DAT_00302058)[lVar23 * 0x10] = uStack1344;
  (&DAT_0030205c)[lVar23 * 0x10] = uStack1340;
  (&DAT_00302060)[lVar23 * 0x10] = local_538;
  (&DAT_00302064)[lVar23 * 0x10] = uStack1332;
  (&DAT_00302068)[lVar23 * 0x10] = uStack1328;
  (&DAT_0030206c)[lVar23 * 0x10] = uStack1324;
  (&DAT_00302070)[lVar23 * 0x10] = local_528;
  (&DAT_00302074)[lVar23 * 0x10] = uStack1316;
  (&DAT_00302078)[lVar23 * 0x10] = uStack1312;
  (&DAT_0030207c)[lVar23 * 0x10] = uStack1308;
  puVar27 = DAT_00302440;
  goto LAB_00100ad0;
switchD_00100b19_caseD_a:
  lVar23 = (long)(int)uVar24;
                    /* WARNING: Load size is inaccurate */
  auVar2 = *(undefined *)DAT_00302440;
  *(int *)(&DAT_00302040 + lVar23 * 8) = SUB164(auVar2,0);
  *(undefined4 *)((long)&DAT_00302040 + lVar23 * 0x40 + 4) = SUB164(auVar2 >> 0x20,0);
  (&DAT_00302048)[lVar23 * 0x10] = SUB164(auVar2 >> 0x40,0);
  (&DAT_0030204c)[lVar23 * 0x10] = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
  auVar2 = *(undefined *)(puVar27 + 9);
  (&DAT_00302050)[lVar23 * 0x10] = SUB164(auVar2,0);
  (&DAT_00302054)[lVar23 * 0x10] = SUB164(auVar2 >> 0x20,0);
  (&DAT_00302058)[lVar23 * 0x10] = SUB164(auVar2 >> 0x40,0);
  (&DAT_0030205c)[lVar23 * 0x10] = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
  auVar2 = *(undefined *)(puVar27 + 0x11);
  (&DAT_00302060)[lVar23 * 0x10] = SUB164(auVar2,0);
  (&DAT_00302064)[lVar23 * 0x10] = SUB164(auVar2 >> 0x20,0);
  (&DAT_00302068)[lVar23 * 0x10] = SUB164(auVar2 >> 0x40,0);
  (&DAT_0030206c)[lVar23 * 0x10] = SUB164(auVar2 >> 0x60,0);
                    /* WARNING: Load size is inaccurate */
  auVar2 = *(undefined *)(puVar27 + 0x19);
  (&DAT_00302070)[lVar23 * 0x10] = SUB164(auVar2,0);
  (&DAT_00302074)[lVar23 * 0x10] = SUB164(auVar2 >> 0x20,0);
  (&DAT_00302078)[lVar23 * 0x10] = SUB164(auVar2 >> 0x40,0);
  (&DAT_0030207c)[lVar23 * 0x10] = SUB164(auVar2 >> 0x60,0);
  puVar27 = DAT_00302440 + 0x20;
  goto LAB_00100ad0;
}

