source_filename = "test"
target datalayout = "e-p:32:32:32-f80:32:32"

@a1 = internal unnamed_addr global i32 0
@sp = internal unnamed_addr global i32 0
@fp = internal unnamed_addr global i32 0
@global_var_412520.14 = local_unnamed_addr global i32 0
@global_var_412538.15 = local_unnamed_addr global i32 0
@global_var_402237.16 = constant [65 x i8] c"/EXHYI6sc9RJPZyeqWi2QbNdh5uDL1MonwfS8VKxUrvF03lAGt7OgBk+zjC4Tmpa\00"
@global_var_470000.17 = global i32 0
@global_var_472e64.18 = global i32 0
@global_var_412570.19 = global i32 0
@global_var_412540.20 = local_unnamed_addr global i32 0
@global_var_412524.21 = local_unnamed_addr global i32 0
@rfc3548_Base_64_Encoding_with_URL_and_Filename_Safe_Alphabet_at_4021f8 = constant [62 x i8] c"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
@global_var_412480.22 = local_unnamed_addr global [62 x i8]* @rfc3548_Base_64_Encoding_with_URL_and_Filename_Safe_Alphabet_at_4021f8
@global_var_412a70.23 = global i32 0
@global_var_412544.24 = local_unnamed_addr global i32 0
@global_var_412528.25 = local_unnamed_addr global i32 0
@global_var_412970.26 = global i32 0
@global_var_412530.27 = local_unnamed_addr global i32 0
@global_var_41254c.28 = local_unnamed_addr global i32 0
@global_var_412e70.29 = global i32 0
@global_var_4022b4.30 = constant i32 66
@global_var_41252c.31 = local_unnamed_addr global i32 0
@global_var_412548.32 = local_unnamed_addr global i32 0
@global_var_402278.33 = constant [28 x i8] c"========================:\0A \00"
@global_var_462e66.35 = global i32 0
@global_var_402294.36 = constant [3 x i8] c"%s\00"
@global_var_402297.37 = constant [14 x i8] c"good job boy\0A\00"
@global_var_4022a5.38 = constant [14 x i8] c"try it again\0A\00"

define i32 @function_4007a0(i32 %arg1) local_unnamed_addr {
dec_label_pc_4007a0:
  %a0.global-to-local = alloca i32, align 4
  %a1.global-to-local = alloca i32, align 4
  %a2.global-to-local = alloca i32, align 4
  %a3.global-to-local = alloca i32, align 4
  %at.global-to-local = alloca i32, align 4
  %t0.global-to-local = alloca i32, align 4
  %t1.global-to-local = alloca i32, align 4
  %v0.global-to-local = alloca i32, align 4
  %v1.global-to-local = alloca i32, align 4
  store i32 %arg1, i32* %a0.global-to-local, align 4
  %stack_var_-80 = alloca i32, align 4
  %v2_4007a0 = ptrtoint i32* %stack_var_-80 to i32
  %v3_4007b4 = load i32, i32* @global_var_412520.14, align 4
  %v3_4007bc = load i32, i32* @global_var_412538.15, align 4
  %v1_4007c0 = add i32 %v3_4007b4, -1
  %v2_4007c4 = mul i32 %v1_4007c0, %v3_4007b4
  %v1_4007c8 = urem i32 %v2_4007c4, 2
  %v1_4007cc = icmp eq i32 %v1_4007c8, 0
  %v2_4007cc = zext i1 %v1_4007cc to i32
  %v1_4007d0 = icmp slt i32 %v3_4007bc, 10
  %v2_4007d0 = zext i1 %v1_4007d0 to i32
  store i32 %v2_4007d0, i32* %a1.global-to-local, align 4
  store i32 9, i32* %a2.global-to-local, align 4
  %v2_4007d8 = icmp sgt i32 %v3_4007bc, 9
  %v3_4007d8 = zext i1 %v2_4007d8 to i32
  store i32 %v3_4007d8, i32* %v0.global-to-local, align 4
  %v2_4007dc = xor i32 %v2_4007cc, %v2_4007d0
  store i32 %v2_4007dc, i32* %v1.global-to-local, align 4
  %v2_4007e0 = or i32 %v1_4007c8, %v3_4007d8
  %v1_4007e4 = xor i32 %v2_4007e0, 1
  store i32 %v1_4007e4, i32* %at.global-to-local, align 4
  %v0_4007ec = load i32, i32* %a0.global-to-local, align 4
  %v1_4007f0 = icmp eq i32 %v2_4007dc, 0
  br i1 %v1_4007f0, label %dec_label_pc_400800, label %dec_label_pc_400818

dec_label_pc_400800:                              ; preds = %dec_label_pc_4007a0
  store i32 %v1_4007e4, i32* %at.global-to-local, align 4
  store i32 %v1_4007e4, i32* %v0.global-to-local, align 4
  %v1_400808 = icmp eq i32 %v1_4007e4, 0
  br i1 %v1_400808, label %dec_label_pc_400de4, label %dec_label_pc_400818

dec_label_pc_400818:                              ; preds = %dec_label_pc_400800, %dec_label_pc_4007a0, %dec_label_pc_400de4
  %v0_400818 = phi i32 [ %v2_4007a0, %dec_label_pc_400800 ], [ %v2_4007a0, %dec_label_pc_4007a0 ], [ %v0_400818.pre, %dec_label_pc_400de4 ]
  store i32 %v0_400818, i32* %at.global-to-local, align 4
  %v1_40081c = add i32 %v0_400818, -8
  store i32 %v1_40081c, i32* %v0.global-to-local, align 4
  %v1_400828 = add i32 %v0_400818, -16
  store i32 %v1_400828, i32* %v1.global-to-local, align 4
  store i32 %v1_400828, i32* %a0.global-to-local, align 4
  %v1_400834 = add i32 %v0_400818, -24
  store i32 %v1_400834, i32* %a1.global-to-local, align 4
  %v1_400840 = add i32 %v0_400818, -32
  store i32 %v1_400840, i32* %a2.global-to-local, align 4
  %v1_40084c = add i32 %v0_400818, -40
  store i32 %v1_40084c, i32* %a3.global-to-local, align 4
  store i32 %v1_40084c, i32* %t0.global-to-local, align 4
  %v1_400858 = add i32 %v0_400818, -48
  store i32 %v1_400858, i32* %t1.global-to-local, align 4
  %v3_400864 = inttoptr i32 %v1_40081c to i32*
  store i32 %v0_4007ec, i32* %v3_400864, align 4
  %v1_400870 = load i32, i32* %t0.global-to-local, align 4
  %v2_400870 = add i32 %v1_400870, -8
  %v3_400870 = inttoptr i32 %v2_400870 to i32*
  store i32 ptrtoint ([65 x i8]* @global_var_402237.16 to i32), i32* %v3_400870, align 4
  %v0_400874 = load i32, i32* %at.global-to-local, align 4
  %v1_400874 = add i32 %v0_400874, -8
  %v2_400874 = inttoptr i32 %v1_400874 to i32*
  %v3_400874 = load i32, i32* %v2_400874, align 4
  store i32 %v3_400874, i32* %at.global-to-local, align 4
  %v0_40087c = load i32, i32* %a0.global-to-local, align 4
  %v1_400880 = inttoptr i32 %v3_400874 to i8*
  store i32 %v3_400874, i32* %a0.global-to-local, align 4
  %v0_400884 = load i32, i32* %t1.global-to-local, align 4
  %v0_400888 = load i32, i32* %v0.global-to-local, align 4
  %v0_40088c = load i32, i32* %v1.global-to-local, align 4
  %v0_400890 = load i32, i32* %a1.global-to-local, align 4
  %v0_400894 = load i32, i32* %a2.global-to-local, align 4
  %v0_400898 = load i32, i32* %a3.global-to-local, align 4
  %v3_4008a0 = call i32 @strlen(i8* %v1_400880)
  store i32 %v3_4008a0, i32* %v0.global-to-local, align 4
  store i32 %v0_40087c, i32* %at.global-to-local, align 4
  %v2_4008ac = add i32 %v0_40087c, -8
  %v3_4008ac = inttoptr i32 %v2_4008ac to i32*
  store i32 %v3_4008a0, i32* %v3_4008ac, align 4
  %v0_4008b0 = load i32, i32* %at.global-to-local, align 4
  %v1_4008b0 = add i32 %v0_4008b0, -8
  %v2_4008b0 = inttoptr i32 %v1_4008b0 to i32*
  %v3_4008b0 = load i32, i32* %v2_4008b0, align 4
  %v2_4008bc = sext i32 %v3_4008b0 to i64
  %v4_4008bc = mul nsw i64 %v2_4008bc, 1431655766
  %v6_4008bc = udiv i64 %v4_4008bc, 4294967296
  %v7_4008bc = trunc i64 %v6_4008bc to i32
  %v1_4008c41 = lshr i64 %v4_4008bc, 63
  %v1_4008c4 = trunc i64 %v1_4008c41 to i32
  %v2_4008c8 = add i32 %v7_4008bc, %v1_4008c4
  %v2_4008d0 = mul i32 %v2_4008c8, 3
  %v1_4008d8 = icmp eq i32 %v3_4008b0, %v2_4008d0
  %v2_4008d8 = zext i1 %v1_4008d8 to i32
  store i32 %v2_4008d8, i32* %v0.global-to-local, align 4
  %v3_4008e0 = load i32, i32* @global_var_412520.14, align 4
  %v3_4008e8 = load i32, i32* @global_var_412538.15, align 4
  %v1_4008ec = add i32 %v3_4008e0, -1
  %v2_4008f0 = mul i32 %v1_4008ec, %v3_4008e0
  %v1_4008f4 = urem i32 %v2_4008f0, 2
  %v2_4008fc = icmp sgt i32 %v3_4008e8, 9
  %v3_4008fc = zext i1 %v2_4008fc to i32
  store i32 %v3_4008fc, i32* %a0.global-to-local, align 4
  %v2_400900 = xor i32 %v3_4008fc, %v1_4008f4
  store i32 %v2_400900, i32* %a1.global-to-local, align 4
  %v2_400904 = or i32 %v1_4008f4, %v3_4008fc
  %v1_400908 = xor i32 %v2_400904, 1
  store i32 %v1_400908, i32* %v1.global-to-local, align 4
  %v1_400914 = icmp eq i32 %v2_400900, 0
  br i1 %v1_400914, label %dec_label_pc_400924, label %dec_label_pc_40093c

dec_label_pc_400924:                              ; preds = %dec_label_pc_400818
  store i32 %v1_400908, i32* %at.global-to-local, align 4
  store i32 %v1_400908, i32* %v0.global-to-local, align 4
  %v1_40092c = icmp eq i32 %v1_400908, 0
  br i1 %v1_40092c, label %dec_label_pc_400924.dec_label_pc_400de4_crit_edge, label %dec_label_pc_40093c

dec_label_pc_400924.dec_label_pc_400de4_crit_edge: ; preds = %dec_label_pc_400924
  %v0_400de4.pre = load i32, i32* @sp, align 4
  br label %dec_label_pc_400de4

dec_label_pc_40093c:                              ; preds = %dec_label_pc_400924, %dec_label_pc_400818
  store i32 %v2_4008d8, i32* %v0.global-to-local, align 4
  %v1_400944 = icmp eq i1 %v1_4008d8, false
  store i32 %v0_400890, i32* %at.global-to-local, align 4
  %v1_40098c = inttoptr i32 %v0_400890 to i32*
  %v2_40098c = load i32, i32* %v1_40098c, align 4
  %v2_400998 = sext i32 %v2_40098c to i64
  %v4_400998 = mul nsw i64 %v2_400998, 1431655766
  %v6_400998 = udiv i64 %v4_400998, 4294967296
  %v7_400998 = trunc i64 %v6_400998 to i32
  store i32 %v7_400998, i32* %v0.global-to-local, align 4
  %v1_4009a07 = lshr i64 %v4_400998, 63
  %v1_4009a0 = trunc i64 %v1_4009a07 to i32
  store i32 %v1_4009a0, i32* %v1.global-to-local, align 4
  %v2_4009a4 = add i32 %v7_400998, %v1_4009a0
  %v1_4009a8 = mul i32 %v2_4009a4, 4
  br i1 %v1_400944, label %dec_label_pc_400988, label %dec_label_pc_400954

dec_label_pc_400954:                              ; preds = %dec_label_pc_40093c
  store i32 %v1_4009a8, i32* %v0.global-to-local, align 4
  store i32 %v0_40088c, i32* %v1.global-to-local, align 4
  %v2_40097c = inttoptr i32 %v0_40088c to i32*
  store i32 %v1_4009a8, i32* %v2_40097c, align 4
  br label %dec_label_pc_4009c0

dec_label_pc_400988:                              ; preds = %dec_label_pc_40093c
  %v1_4009ac = add i32 %v1_4009a8, 4
  store i32 %v1_4009ac, i32* %v0.global-to-local, align 4
  store i32 %v0_40088c, i32* %v1.global-to-local, align 4
  %v2_4009b4 = inttoptr i32 %v0_40088c to i32*
  store i32 %v1_4009ac, i32* %v2_4009b4, align 4
  br label %dec_label_pc_4009c0

dec_label_pc_4009c0:                              ; preds = %dec_label_pc_400988, %dec_label_pc_400954
  %v3_4009c4 = load i32, i32* @global_var_412520.14, align 4
  %v3_4009cc = load i32, i32* @global_var_412538.15, align 4
  %v1_4009d0 = add i32 %v3_4009c4, -1
  %v2_4009d4 = mul i32 %v1_4009d0, %v3_4009c4
  %v1_4009d8 = urem i32 %v2_4009d4, 2
  %v1_4009dc = icmp eq i32 %v1_4009d8, 0
  %v2_4009dc = zext i1 %v1_4009dc to i32
  %v1_4009e0 = icmp slt i32 %v3_4009cc, 10
  %v2_4009e0 = zext i1 %v1_4009e0 to i32
  store i32 %v2_4009e0, i32* %a0.global-to-local, align 4
  store i32 9, i32* %a1.global-to-local, align 4
  %v2_4009e8 = icmp sgt i32 %v3_4009cc, 9
  %v3_4009e8 = zext i1 %v2_4009e8 to i32
  store i32 %v3_4009e8, i32* %v0.global-to-local, align 4
  %v2_4009ec = xor i32 %v2_4009dc, %v2_4009e0
  store i32 %v2_4009ec, i32* %v1.global-to-local, align 4
  %v2_4009f0 = or i32 %v1_4009d8, %v3_4009e8
  %v1_4009f4 = xor i32 %v2_4009f0, 1
  store i32 %v1_4009f4, i32* %at.global-to-local, align 4
  %v1_4009fc = icmp eq i32 %v2_4009ec, 0
  br i1 %v1_4009fc, label %dec_label_pc_400a0c, label %dec_label_pc_400a24

dec_label_pc_400a0c:                              ; preds = %dec_label_pc_4009c0
  store i32 %v1_4009f4, i32* %at.global-to-local, align 4
  store i32 %v1_4009f4, i32* %v0.global-to-local, align 4
  %v1_400a14 = icmp eq i32 %v1_4009f4, 0
  br i1 %v1_400a14, label %dec_label_pc_400a0c.dec_label_pc_400e68_crit_edge, label %dec_label_pc_400a24

dec_label_pc_400a0c.dec_label_pc_400e68_crit_edge: ; preds = %dec_label_pc_400a0c
  %.pre = inttoptr i32 %v0_400894 to i32*
  %.pre18 = inttoptr i32 %v0_400898 to i32*
  br label %dec_label_pc_400e68

dec_label_pc_400a24:                              ; preds = %dec_label_pc_400a0c, %dec_label_pc_4009c0, %dec_label_pc_400e68
  store i32 %v0_400894, i32* %at.global-to-local, align 4
  %v1_400a28 = inttoptr i32 %v0_400894 to i32*
  store i32 0, i32* %v1_400a28, align 4
  store i32 %v0_400898, i32* %v0.global-to-local, align 4
  %v1_400a30 = inttoptr i32 %v0_400898 to i32*
  store i32 0, i32* %v1_400a30, align 4
  %v3_400a38 = load i32, i32* @global_var_412520.14, align 4
  %v3_400a40 = load i32, i32* @global_var_412538.15, align 4
  %v1_400a44 = add i32 %v3_400a38, -1
  %v2_400a48 = mul i32 %v1_400a44, %v3_400a38
  %v1_400a4c = urem i32 %v2_400a48, 2
  %v1_400a50 = icmp eq i32 %v1_400a4c, 0
  %v2_400a50 = zext i1 %v1_400a50 to i32
  %v1_400a54 = icmp slt i32 %v3_400a40, 10
  %v2_400a54 = zext i1 %v1_400a54 to i32
  store i32 %v2_400a54, i32* %a0.global-to-local, align 4
  %v2_400a58 = and i32 %v2_400a50, %v2_400a54
  store i32 %v2_400a58, i32* %a1.global-to-local, align 4
  %v2_400a5c = xor i32 %v2_400a50, %v2_400a54
  store i32 %v2_400a5c, i32* %v1.global-to-local, align 4
  %v1_400a64 = icmp eq i32 %v2_400a58, 0
  br i1 %v1_400a64, label %dec_label_pc_400a74, label %dec_label_pc_400a94.preheader

dec_label_pc_400a74:                              ; preds = %dec_label_pc_400a24
  store i32 %v2_400a5c, i32* %at.global-to-local, align 4
  store i32 %v2_400a5c, i32* %v0.global-to-local, align 4
  %v1_400a7c = icmp eq i32 %v2_400a5c, 0
  br i1 %v1_400a7c, label %dec_label_pc_400e68, label %dec_label_pc_400a94.preheader

dec_label_pc_400a94.preheader:                    ; preds = %dec_label_pc_400a74, %dec_label_pc_400a24
  store i32 %v0_400894, i32* %at.global-to-local, align 4
  %v2_400a989 = load i32, i32* %v1_400a28, align 4
  store i32 %v2_400a989, i32* %v0.global-to-local, align 4
  store i32 %v0_40088c, i32* %v1.global-to-local, align 4
  %v1_400aa0 = inttoptr i32 %v0_40088c to i32*
  %v2_400aa010 = load i32, i32* %v1_400aa0, align 4
  %v1_400aa411 = add i32 %v2_400aa010, -2
  store i32 %v1_400aa411, i32* %a0.global-to-local, align 4
  %v2_400aa812 = icmp slt i32 %v2_400a989, %v1_400aa411
  %v3_400aa813 = zext i1 %v2_400aa812 to i32
  store i32 %v3_400aa813, i32* %v0.global-to-local, align 4
  %v1_400aac14 = icmp eq i1 %v2_400aa812, false
  br i1 %v1_400aac14, label %dec_label_pc_400c60, label %dec_label_pc_400abc.lr.ph

dec_label_pc_400abc.lr.ph:                        ; preds = %dec_label_pc_400a94.preheader
  %v1_400ac0 = inttoptr i32 %v0_400884 to i32*
  %v1_400ac8 = inttoptr i32 %v0_400888 to i32*
  br label %dec_label_pc_400abc

dec_label_pc_400abc:                              ; preds = %dec_label_pc_400abc.lr.ph, %dec_label_pc_400abc
  store i32 %v0_400884, i32* %at.global-to-local, align 4
  %v2_400ac0 = load i32, i32* %v1_400ac0, align 4
  store i32 %v2_400ac0, i32* %v0.global-to-local, align 4
  store i32 %v0_400888, i32* %v1.global-to-local, align 4
  %v2_400ac8 = load i32, i32* %v1_400ac8, align 4
  store i32 %v2_400ac8, i32* %a0.global-to-local, align 4
  store i32 %v0_400898, i32* %a1.global-to-local, align 4
  %v2_400ad0 = load i32, i32* %v1_400a30, align 4
  store i32 %v2_400ad0, i32* %a2.global-to-local, align 4
  %v2_400ad4 = add i32 %v2_400ad0, %v2_400ac8
  store i32 %v2_400ad4, i32* %a0.global-to-local, align 4
  %v1_400ad8 = inttoptr i32 %v2_400ad4 to i8*
  %v2_400ad8 = load i8, i8* %v1_400ad8, align 1
  %tmp44 = sdiv i8 %v2_400ad8, 4
  %v1_400adc = sext i8 %tmp44 to i32
  store i32 %v1_400adc, i32* %a0.global-to-local, align 4
  %v2_400ae0 = add i32 %v1_400adc, %v2_400ac0
  store i32 %v2_400ae0, i32* %v0.global-to-local, align 4
  %v1_400ae4 = inttoptr i32 %v2_400ae0 to i8*
  %v2_400ae4 = load i8, i8* %v1_400ae4, align 1
  %v3_400ae4 = zext i8 %v2_400ae4 to i32
  store i32 %v3_400ae4, i32* %v0.global-to-local, align 4
  store i32 %v0_400894, i32* %a0.global-to-local, align 4
  %v2_400aec = load i32, i32* %v1_400a28, align 4
  store i32 ptrtoint (i32* @global_var_472e64.18 to i32), i32* %a3.global-to-local, align 4
  %v2_400af8 = add i32 %v2_400aec, ptrtoint (i32* @global_var_472e64.18 to i32)
  store i32 %v2_400af8, i32* %a2.global-to-local, align 4
  %v3_400afc = inttoptr i32 %v2_400af8 to i8*
  store i8 %v2_400ae4, i8* %v3_400afc, align 1
  %v0_400b00 = load i32, i32* %a0.global-to-local, align 4
  %v1_400b00 = inttoptr i32 %v0_400b00 to i32*
  %v2_400b00 = load i32, i32* %v1_400b00, align 4
  %v0_400b04 = load i32, i32* %a3.global-to-local, align 4
  %v2_400b04 = add i32 %v0_400b04, %v2_400b00
  store i32 %v2_400b04, i32* %v0.global-to-local, align 4
  %v0_400b08 = load i32, i32* %at.global-to-local, align 4
  %v1_400b08 = inttoptr i32 %v0_400b08 to i32*
  %v2_400b08 = load i32, i32* %v1_400b08, align 4
  store i32 %v2_400b08, i32* %a2.global-to-local, align 4
  %v0_400b0c = load i32, i32* %v1.global-to-local, align 4
  %v1_400b0c = inttoptr i32 %v0_400b0c to i32*
  %v2_400b0c = load i32, i32* %v1_400b0c, align 4
  store i32 %v2_400b0c, i32* %t0.global-to-local, align 4
  %v0_400b10 = load i32, i32* %a1.global-to-local, align 4
  %v1_400b10 = inttoptr i32 %v0_400b10 to i32*
  %v2_400b10 = load i32, i32* %v1_400b10, align 4
  store i32 %v2_400b10, i32* %t1.global-to-local, align 4
  %v2_400b14 = add i32 %v2_400b10, %v2_400b0c
  store i32 %v2_400b14, i32* %t0.global-to-local, align 4
  %v1_400b18 = inttoptr i32 %v2_400b14 to i8*
  %v2_400b18 = load i8, i8* %v1_400b18, align 1
  %v3_400b18 = sext i8 %v2_400b18 to i32
  %v2_400b28 = and i32 %v3_400b18, -268435453
  %v1_400b2c = mul i32 %v2_400b28, 16
  store i32 %v1_400b2c, i32* %t1.global-to-local, align 4
  %v1_400b30 = add i32 %v2_400b14, 1
  %v2_400b30 = inttoptr i32 %v1_400b30 to i8*
  %v3_400b30 = load i8, i8* %v2_400b30, align 1
  %tmp45 = sdiv i8 %v3_400b30, 16
  %v1_400b34 = sext i8 %tmp45 to i32
  %v2_400b40 = or i32 %v1_400b34, %v1_400b2c
  store i32 %v2_400b40, i32* %t0.global-to-local, align 4
  %v2_400b44 = add i32 %v2_400b40, %v2_400b08
  store i32 %v2_400b44, i32* %a2.global-to-local, align 4
  %v1_400b48 = inttoptr i32 %v2_400b44 to i8*
  %v2_400b48 = load i8, i8* %v1_400b48, align 1
  %v3_400b48 = zext i8 %v2_400b48 to i32
  store i32 %v3_400b48, i32* %a2.global-to-local, align 4
  %v3_400b4c = add i32 %v2_400b04, 1
  %v4_400b4c = inttoptr i32 %v3_400b4c to i8*
  store i8 %v2_400b48, i8* %v4_400b4c, align 1
  %v0_400b50 = load i32, i32* %a0.global-to-local, align 4
  %v1_400b50 = inttoptr i32 %v0_400b50 to i32*
  %v2_400b50 = load i32, i32* %v1_400b50, align 4
  %v0_400b54 = load i32, i32* %a3.global-to-local, align 4
  %v2_400b54 = add i32 %v0_400b54, %v2_400b50
  store i32 %v2_400b54, i32* %v0.global-to-local, align 4
  %v0_400b58 = load i32, i32* %at.global-to-local, align 4
  %v1_400b58 = inttoptr i32 %v0_400b58 to i32*
  %v2_400b58 = load i32, i32* %v1_400b58, align 4
  store i32 %v2_400b58, i32* %a2.global-to-local, align 4
  %v0_400b5c = load i32, i32* %v1.global-to-local, align 4
  %v1_400b5c = inttoptr i32 %v0_400b5c to i32*
  %v2_400b5c = load i32, i32* %v1_400b5c, align 4
  store i32 %v2_400b5c, i32* %t0.global-to-local, align 4
  %v0_400b60 = load i32, i32* %a1.global-to-local, align 4
  %v1_400b60 = inttoptr i32 %v0_400b60 to i32*
  %v2_400b60 = load i32, i32* %v1_400b60, align 4
  %v2_400b64 = add i32 %v2_400b60, %v2_400b5c
  %v1_400b68 = sub i32 -1, %v2_400b60
  store i32 %v1_400b68, i32* %t1.global-to-local, align 4
  %v2_400b6c = sub i32 %v2_400b5c, %v1_400b68
  store i32 %v2_400b6c, i32* %t0.global-to-local, align 4
  %v1_400b70 = inttoptr i32 %v2_400b6c to i8*
  %v2_400b70 = load i8, i8* %v1_400b70, align 1
  %v3_400b70 = sext i8 %v2_400b70 to i32
  %v2_400b7c = xor i32 %v3_400b70, 1073741808
  store i32 %v2_400b7c, i32* %t1.global-to-local, align 4
  %v2_400b80 = and i32 %v2_400b7c, %v3_400b70
  %v1_400b84 = mul i32 %v2_400b80, 4
  store i32 %v1_400b84, i32* %t0.global-to-local, align 4
  %v1_400b88 = add i32 %v2_400b64, 2
  %v2_400b88 = inttoptr i32 %v1_400b88 to i8*
  %v3_400b88 = load i8, i8* %v2_400b88, align 1
  %tmp46 = sdiv i8 %v3_400b88, 64
  %v1_400b8c = sext i8 %tmp46 to i32
  %v1_400b90 = sub i32 -1, %v1_400b84
  %v2_400ba0 = and i32 %v1_400b90, -1335064306
  %v2_400bac = and i32 %v1_400b84, 1335064304
  %v2_400bbc = or i32 %v2_400bac, %v2_400ba0
  %v2_400bc0 = xor i32 %v1_400b8c, -1335064306
  %v2_400bc4 = xor i32 %v2_400bc0, %v2_400bbc
  %v3_400bc8 = and i32 %v1_400b8c, %v1_400b84
  store i32 %v3_400bc8, i32* %t1.global-to-local, align 4
  %v2_400bcc = or i32 %v2_400bc4, %v3_400bc8
  store i32 %v2_400bcc, i32* %t0.global-to-local, align 4
  %v2_400bd0 = add i32 %v2_400bcc, %v2_400b58
  store i32 %v2_400bd0, i32* %a2.global-to-local, align 4
  %v1_400bd4 = inttoptr i32 %v2_400bd0 to i8*
  %v2_400bd4 = load i8, i8* %v1_400bd4, align 1
  %v3_400bd4 = zext i8 %v2_400bd4 to i32
  store i32 %v3_400bd4, i32* %a2.global-to-local, align 4
  %v3_400bd8 = add i32 %v2_400b54, 2
  %v4_400bd8 = inttoptr i32 %v3_400bd8 to i8*
  store i8 %v2_400bd4, i8* %v4_400bd8, align 1
  %v0_400bdc = load i32, i32* %a0.global-to-local, align 4
  %v1_400bdc = inttoptr i32 %v0_400bdc to i32*
  %v2_400bdc = load i32, i32* %v1_400bdc, align 4
  %v0_400be0 = load i32, i32* %a3.global-to-local, align 4
  %v2_400be0 = add i32 %v0_400be0, %v2_400bdc
  store i32 %v2_400be0, i32* %v0.global-to-local, align 4
  %v0_400be4 = load i32, i32* %at.global-to-local, align 4
  %v1_400be4 = inttoptr i32 %v0_400be4 to i32*
  %v2_400be4 = load i32, i32* %v1_400be4, align 4
  store i32 %v2_400be4, i32* %a2.global-to-local, align 4
  %v0_400be8 = load i32, i32* %v1.global-to-local, align 4
  %v1_400be8 = inttoptr i32 %v0_400be8 to i32*
  %v2_400be8 = load i32, i32* %v1_400be8, align 4
  store i32 %v2_400be8, i32* %a3.global-to-local, align 4
  %v0_400bec = load i32, i32* %a1.global-to-local, align 4
  %v1_400bec = inttoptr i32 %v0_400bec to i32*
  %v2_400bec = load i32, i32* %v1_400bec, align 4
  store i32 -2, i32* %t1.global-to-local, align 4
  %v2_400bf4 = sub i32 -2, %v2_400bec
  store i32 %v2_400bf4, i32* %t0.global-to-local, align 4
  %v2_400bf8 = sub i32 %v2_400be8, %v2_400bf4
  store i32 %v2_400bf8, i32* %a3.global-to-local, align 4
  %v1_400bfc = inttoptr i32 %v2_400bf8 to i8*
  %v2_400bfc = load i8, i8* %v1_400bfc, align 1
  %v3_400bfc = sext i8 %v2_400bfc to i32
  %v2_400c04 = xor i32 %v3_400bfc, -64
  store i32 %v2_400c04, i32* %t0.global-to-local, align 4
  %v2_400c08 = and i32 %v2_400c04, %v3_400bfc
  store i32 %v2_400c08, i32* %a3.global-to-local, align 4
  %v2_400c0c = add i32 %v2_400c08, %v2_400be4
  store i32 %v2_400c0c, i32* %a2.global-to-local, align 4
  %v1_400c10 = inttoptr i32 %v2_400c0c to i8*
  %v2_400c10 = load i8, i8* %v1_400c10, align 1
  %v3_400c10 = zext i8 %v2_400c10 to i32
  store i32 %v3_400c10, i32* %a2.global-to-local, align 4
  %v3_400c14 = add i32 %v2_400be0, 3
  %v4_400c14 = inttoptr i32 %v3_400c14 to i8*
  store i8 %v2_400c10, i8* %v4_400c14, align 1
  store i32 %v0_400898, i32* %at.global-to-local, align 4
  %v2_400c24 = load i32, i32* %v1_400a30, align 4
  store i32 0, i32* %v1.global-to-local, align 4
  store i32 3, i32* %a0.global-to-local, align 4
  %v2_400c34 = add i32 %v2_400c24, 3
  store i32 %v2_400c34, i32* %v1_400a30, align 4
  store i32 %v0_400894, i32* %v0.global-to-local, align 4
  %v2_400c40 = load i32, i32* %v1_400a28, align 4
  store i32 4, i32* %a1.global-to-local, align 4
  %v2_400c4c = add i32 %v2_400c40, 4
  store i32 %v2_400c4c, i32* %a0.global-to-local, align 4
  store i32 %v2_400c4c, i32* %v1_400a28, align 4
  store i32 %v0_400894, i32* %at.global-to-local, align 4
  %v2_400a98 = load i32, i32* %v1_400a28, align 4
  store i32 %v2_400a98, i32* %v0.global-to-local, align 4
  store i32 %v0_40088c, i32* %v1.global-to-local, align 4
  %v2_400aa0 = load i32, i32* %v1_400aa0, align 4
  %v1_400aa4 = add i32 %v2_400aa0, -2
  store i32 %v1_400aa4, i32* %a0.global-to-local, align 4
  %v2_400aa8 = icmp slt i32 %v2_400a98, %v1_400aa4
  %v3_400aa8 = zext i1 %v2_400aa8 to i32
  store i32 %v3_400aa8, i32* %v0.global-to-local, align 4
  %v1_400aac = icmp eq i1 %v2_400aa8, false
  br i1 %v1_400aac, label %dec_label_pc_400c60, label %dec_label_pc_400abc

dec_label_pc_400c60:                              ; preds = %dec_label_pc_400abc, %dec_label_pc_400a94.preheader
  store i32 %v0_400890, i32* %at.global-to-local, align 4
  %v2_400c64 = load i32, i32* %v1_40098c, align 4
  %v2_400c70 = sext i32 %v2_400c64 to i64
  %v4_400c70 = mul nsw i64 %v2_400c70, 1431655766
  %v6_400c70 = udiv i64 %v4_400c70, 4294967296
  %v7_400c70 = trunc i64 %v6_400c70 to i32
  %v1_400c785 = lshr i64 %v4_400c70, 63
  %v1_400c78 = trunc i64 %v1_400c785 to i32
  %v2_400c7c = add i32 %v7_400c70, %v1_400c78
  %v1_400c80 = mul i32 %v2_400c7c, 2
  store i32 %v1_400c80, i32* %a0.global-to-local, align 4
  %tmp43 = mul i32 %v2_400c7c, -3
  %v2_400c88 = add i32 %tmp43, %v2_400c64
  store i32 %v2_400c88, i32* %v0.global-to-local, align 4
  store i32 1, i32* %v1.global-to-local, align 4
  %v2_400c94 = icmp eq i32 %v2_400c88, 1
  br i1 %v2_400c94, label %dec_label_pc_400cbc, label %dec_label_pc_400ca4

dec_label_pc_400ca4:                              ; preds = %dec_label_pc_400c60
  store i32 2, i32* %at.global-to-local, align 4
  store i32 %v2_400c88, i32* %v0.global-to-local, align 4
  %v2_400cac = icmp eq i32 %v2_400c88, 2
  br i1 %v2_400cac, label %dec_label_pc_400cec, label %dec_label_pc_400dcc

dec_label_pc_400cbc:                              ; preds = %dec_label_pc_400c60
  store i32 %v0_400894, i32* %at.global-to-local, align 4
  %v2_400cc0 = load i32, i32* %v1_400a28, align 4
  store i32 ptrtoint (i32* @global_var_472e64.18 to i32), i32* %v1.global-to-local, align 4
  %v2_400ccc = add i32 %v2_400cc0, ptrtoint (i32* @global_var_472e64.18 to i32)
  store i32 %v2_400ccc, i32* %v0.global-to-local, align 4
  store i32 61, i32* %a0.global-to-local, align 4
  %v3_400cd4 = add i32 %v2_400cc0, add (i32 ptrtoint (i32* @global_var_472e64.18 to i32), i32 -2)
  %v4_400cd4 = inttoptr i32 %v3_400cd4 to i8*
  store i8 61, i8* %v4_400cd4, align 1
  %v0_400cd8 = load i32, i32* %at.global-to-local, align 4
  %v1_400cd8 = inttoptr i32 %v0_400cd8 to i32*
  %v2_400cd8 = load i32, i32* %v1_400cd8, align 4
  %v0_400cdc = load i32, i32* %v1.global-to-local, align 4
  %v2_400cdc = add i32 %v0_400cdc, %v2_400cd8
  store i32 %v2_400cdc, i32* %v0.global-to-local, align 4
  %v0_400ce0 = load i32, i32* %a0.global-to-local, align 4
  %v1_400ce0 = trunc i32 %v0_400ce0 to i8
  %v3_400ce0 = add i32 %v2_400cdc, -1
  %v4_400ce0 = inttoptr i32 %v3_400ce0 to i8*
  store i8 %v1_400ce0, i8* %v4_400ce0, align 1
  %v0_400de0.pre = load i32, i32* %v0.global-to-local, align 4
  br label %dec_label_pc_400dcc

dec_label_pc_400cec:                              ; preds = %dec_label_pc_400ca4
  %v3_400cf0 = load i32, i32* @global_var_412520.14, align 4
  %v3_400cf8 = load i32, i32* @global_var_412538.15, align 4
  %v1_400cfc = add i32 %v3_400cf0, -1
  %v2_400d00 = mul i32 %v1_400cfc, %v3_400cf0
  %v1_400d04 = urem i32 %v2_400d00, 2
  %v1_400d08 = icmp eq i32 %v1_400d04, 0
  %v2_400d08 = zext i1 %v1_400d08 to i32
  %v1_400d0c = icmp slt i32 %v3_400cf8, 10
  %v2_400d0c = zext i1 %v1_400d0c to i32
  store i32 %v2_400d0c, i32* %v0.global-to-local, align 4
  %v2_400d10 = and i32 %v2_400d08, %v2_400d0c
  store i32 %v2_400d10, i32* %v1.global-to-local, align 4
  %v2_400d14 = xor i32 %v2_400d08, %v2_400d0c
  store i32 %v2_400d14, i32* %at.global-to-local, align 4
  %v1_400d1c = icmp eq i32 %v2_400d10, 0
  br i1 %v1_400d1c, label %dec_label_pc_400d2c, label %dec_label_pc_400d44

dec_label_pc_400d2c:                              ; preds = %dec_label_pc_400cec
  store i32 %v2_400d14, i32* %at.global-to-local, align 4
  store i32 %v2_400d14, i32* %v0.global-to-local, align 4
  %v1_400d34 = icmp eq i32 %v2_400d14, 0
  br i1 %v1_400d34, label %dec_label_pc_400e80, label %dec_label_pc_400d44

dec_label_pc_400d44:                              ; preds = %dec_label_pc_400d2c, %dec_label_pc_400cec, %dec_label_pc_400e80
  store i32 %v0_400894, i32* %at.global-to-local, align 4
  %v2_400d48 = load i32, i32* %v1_400a28, align 4
  %v3_400d5c = add i32 %v2_400d48, add (i32 ptrtoint (i32* @global_var_472e64.18 to i32), i32 -1)
  %v4_400d5c = inttoptr i32 %v3_400d5c to i8*
  store i8 61, i8* %v4_400d5c, align 1
  %v3_400d64 = load i32, i32* @global_var_412520.14, align 4
  %v3_400d6c = load i32, i32* @global_var_412538.15, align 4
  %v1_400d70 = add i32 %v3_400d64, -1
  %v2_400d74 = mul i32 %v1_400d70, %v3_400d64
  %v1_400d78 = urem i32 %v2_400d74, 2
  %v1_400d7c = icmp eq i32 %v1_400d78, 0
  %v2_400d7c = zext i1 %v1_400d7c to i32
  %v1_400d80 = icmp slt i32 %v3_400d6c, 10
  %v2_400d80 = zext i1 %v1_400d80 to i32
  store i32 %v2_400d80, i32* %a1.global-to-local, align 4
  store i32 9, i32* %a2.global-to-local, align 4
  %v2_400d88 = icmp sgt i32 %v3_400d6c, 9
  %v3_400d88 = zext i1 %v2_400d88 to i32
  store i32 %v3_400d88, i32* %v1.global-to-local, align 4
  %v2_400d8c = xor i32 %v2_400d7c, %v2_400d80
  store i32 %v2_400d8c, i32* %a0.global-to-local, align 4
  %v2_400d90 = or i32 %v1_400d78, %v3_400d88
  %v1_400d94 = xor i32 %v2_400d90, 1
  store i32 %v1_400d94, i32* %v0.global-to-local, align 4
  %v1_400d9c = icmp eq i32 %v2_400d8c, 0
  br i1 %v1_400d9c, label %dec_label_pc_400dac, label %dec_label_pc_400dcc

dec_label_pc_400dac:                              ; preds = %dec_label_pc_400d44
  store i32 %v1_400d94, i32* %at.global-to-local, align 4
  store i32 %v1_400d94, i32* %v0.global-to-local, align 4
  %v1_400db4 = icmp eq i32 %v1_400d94, 0
  br i1 %v1_400db4, label %dec_label_pc_400e80, label %dec_label_pc_400dcc

dec_label_pc_400dcc:                              ; preds = %dec_label_pc_400d44, %dec_label_pc_400dac, %dec_label_pc_400ca4, %dec_label_pc_400cbc
  %v0_400de0 = phi i32 [ %v1_400d94, %dec_label_pc_400d44 ], [ %v1_400d94, %dec_label_pc_400dac ], [ %v2_400c88, %dec_label_pc_400ca4 ], [ %v0_400de0.pre, %dec_label_pc_400cbc ]
  ret i32 %v0_400de0

dec_label_pc_400de4:                              ; preds = %dec_label_pc_400924.dec_label_pc_400de4_crit_edge, %dec_label_pc_400800
  %v0_400de4 = phi i32 [ %v0_400de4.pre, %dec_label_pc_400924.dec_label_pc_400de4_crit_edge ], [ %v2_4007a0, %dec_label_pc_400800 ]
  store i32 %v0_400de4, i32* %at.global-to-local, align 4
  %v1_400de8 = add i32 %v0_400de4, -8
  %v1_400df4 = add i32 %v0_400de4, -16
  store i32 %v1_400df4, i32* %v0.global-to-local, align 4
  %v1_400e18 = add i32 %v0_400de4, -40
  store i32 %v1_400e18, i32* %v1.global-to-local, align 4
  store i32 %v0_4007ec, i32* %a0.global-to-local, align 4
  %v3_400e30 = inttoptr i32 %v1_400de8 to i32*
  store i32 %v0_4007ec, i32* %v3_400e30, align 4
  store i32 ptrtoint ([65 x i8]* @global_var_402237.16 to i32), i32* %a1.global-to-local, align 4
  %v1_400e3c = load i32, i32* %v1.global-to-local, align 4
  %v2_400e3c = add i32 %v1_400e3c, -8
  %v3_400e3c = inttoptr i32 %v2_400e3c to i32*
  store i32 ptrtoint ([65 x i8]* @global_var_402237.16 to i32), i32* %v3_400e3c, align 4
  %v0_400e40 = load i32, i32* %at.global-to-local, align 4
  %v1_400e40 = add i32 %v0_400e40, -8
  %v2_400e40 = inttoptr i32 %v1_400e40 to i32*
  %v3_400e40 = load i32, i32* %v2_400e40, align 4
  %v4_400e40 = inttoptr i32 %v3_400e40 to i8*
  store i32 %v3_400e40, i32* %a0.global-to-local, align 4
  %v0_400e48 = load i32, i32* %v0.global-to-local, align 4
  store i32 %v0_400e48, i32* %stack_var_-80, align 4
  %v3_400e50 = call i32 @strlen(i8* %v4_400e40)
  store i32 %v3_400e50, i32* %v0.global-to-local, align 4
  %v2_400e58 = load i32, i32* %stack_var_-80, align 4
  store i32 %v2_400e58, i32* %at.global-to-local, align 4
  %v2_400e5c = add i32 %v2_400e58, -8
  %v3_400e5c = inttoptr i32 %v2_400e5c to i32*
  store i32 %v3_400e50, i32* %v3_400e5c, align 4
  %v0_400818.pre = load i32, i32* @sp, align 4
  br label %dec_label_pc_400818

dec_label_pc_400e68:                              ; preds = %dec_label_pc_400a0c.dec_label_pc_400e68_crit_edge, %dec_label_pc_400a74
  %v1_400e74.pre-phi = phi i32* [ %.pre18, %dec_label_pc_400a0c.dec_label_pc_400e68_crit_edge ], [ %v1_400a30, %dec_label_pc_400a74 ]
  %v1_400e6c.pre-phi = phi i32* [ %.pre, %dec_label_pc_400a0c.dec_label_pc_400e68_crit_edge ], [ %v1_400a28, %dec_label_pc_400a74 ]
  store i32 %v0_400894, i32* %at.global-to-local, align 4
  store i32 0, i32* %v1_400e6c.pre-phi, align 4
  store i32 %v0_400898, i32* %v0.global-to-local, align 4
  store i32 0, i32* %v1_400e74.pre-phi, align 4
  br label %dec_label_pc_400a24

dec_label_pc_400e80:                              ; preds = %dec_label_pc_400dac, %dec_label_pc_400d2c
  store i32 %v0_400894, i32* %at.global-to-local, align 4
  %v2_400e84 = load i32, i32* %v1_400a28, align 4
  %v2_400e90 = add i32 %v2_400e84, ptrtoint (i32* @global_var_472e64.18 to i32)
  store i32 %v2_400e90, i32* %v0.global-to-local, align 4
  store i32 61, i32* %v1.global-to-local, align 4
  %v3_400e98 = add i32 %v2_400e84, add (i32 ptrtoint (i32* @global_var_472e64.18 to i32), i32 -1)
  %v4_400e98 = inttoptr i32 %v3_400e98 to i8*
  store i8 61, i8* %v4_400e98, align 1
  br label %dec_label_pc_400d44
}

define i32 @function_400ea4(i1 %arg1, i32 %arg2) local_unnamed_addr {
dec_label_pc_400ea4:
  br label %dec_label_pc_400ed4

dec_label_pc_400ed4:                              ; preds = %dec_label_pc_400ea4, %dec_label_pc_400ed4
  %storemerge1 = phi i32 [ 0, %dec_label_pc_400ea4 ], [ %v1_400ef8, %dec_label_pc_400ed4 ]
  %v1_400ed8 = mul i32 %storemerge1, 4
  %v2_400ee4 = add i32 %v1_400ed8, ptrtoint (i32* @global_var_412570.19 to i32)
  %v2_400ee8 = inttoptr i32 %v2_400ee4 to i32*
  store i32 %storemerge1, i32* %v2_400ee8, align 4
  %v1_400ef8 = add i32 %storemerge1, 1
  %v1_400ec0 = icmp slt i32 %v1_400ef8, 256
  %v1_400ec4 = icmp eq i1 %v1_400ec0, false
  br i1 %v1_400ec4, label %dec_label_pc_400f08, label %dec_label_pc_400ed4

dec_label_pc_400f08:                              ; preds = %dec_label_pc_400ed4
  %v3_400f0c = load i32, i32* @global_var_412540.20, align 4
  %v3_400f14 = load i32, i32* @global_var_412524.21, align 4
  %v1_400f18 = add i32 %v3_400f0c, -1
  %v2_400f1c = mul i32 %v1_400f18, %v3_400f0c
  %v1_400f20 = urem i32 %v2_400f1c, 2
  %v1_400f24 = icmp eq i32 %v1_400f20, 0
  %v1_400f28 = icmp slt i32 %v3_400f14, 10
  %v2_400f30 = icmp sgt i32 %v3_400f14, 9
  %v3_400f30 = zext i1 %v2_400f30 to i32
  %v2_400f38 = or i32 %v1_400f20, %v3_400f30
  %v1_400f3c = xor i32 %v2_400f38, 1
  %v1_400f44 = icmp eq i1 %v1_400f24, %v1_400f28
  br i1 %v1_400f44, label %dec_label_pc_400f54, label %dec_label_pc_400fd0.critedge

dec_label_pc_400f54:                              ; preds = %dec_label_pc_400f08
  %v1_400f5c = icmp eq i32 %v1_400f3c, 0
  br i1 %v1_400f5c, label %dec_label_pc_400fe4, label %dec_label_pc_400fd0.critedge12

dec_label_pc_400fd0.critedge:                     ; preds = %dec_label_pc_400f08
  br label %dec_label_pc_400fd0

dec_label_pc_400fd0.critedge12:                   ; preds = %dec_label_pc_400f54
  br label %dec_label_pc_400fd0

dec_label_pc_400fd0:                              ; preds = %dec_label_pc_400fd0.critedge12, %dec_label_pc_400fd0.critedge
  %v0_400fe0 = phi i32 [ %v3_400f30, %dec_label_pc_400fd0.critedge ], [ %v1_400f3c, %dec_label_pc_400fd0.critedge12 ]
  ret i32 %v0_400fe0

dec_label_pc_400fe4:                              ; preds = %dec_label_pc_400f54, %dec_label_pc_400fe4
  br label %dec_label_pc_400fe4
}

define i32 @function_400fec() local_unnamed_addr {
dec_label_pc_400fec:
  br label %dec_label_pc_40101c

dec_label_pc_40101c:                              ; preds = %dec_label_pc_400fec, %dec_label_pc_40101c
  %storemerge4 = phi i32 [ 0, %dec_label_pc_400fec ], [ %v1_401064, %dec_label_pc_40101c ]
  %v2_401024 = sub nuw nsw i32 63, %storemerge4
  %v3_401030 = load i32, i32* bitcast ([62 x i8]** @global_var_412480.22 to i32*), align 4
  %v2_401038 = add i32 %v3_401030, %v2_401024
  %v1_40103c = inttoptr i32 %v2_401038 to i8*
  %v2_40103c = load i8, i8* %v1_40103c, align 1
  %v3_40103c = sext i8 %v2_40103c to i32
  %v1_40104c = mul i32 %storemerge4, 4
  %v2_401050 = add i32 %v1_40104c, ptrtoint (i32* @global_var_412a70.23 to i32)
  %v2_401054 = inttoptr i32 %v2_401050 to i32*
  store i32 %v3_40103c, i32* %v2_401054, align 4
  %v1_401064 = add nuw nsw i32 %storemerge4, 1
  %v1_401008 = icmp slt i32 %v1_401064, 64
  %v1_40100c = icmp eq i1 %v1_401008, false
  br i1 %v1_40100c, label %dec_label_pc_401080, label %dec_label_pc_40101c

dec_label_pc_401080:                              ; preds = %dec_label_pc_40101c, %dec_label_pc_401160
  %storemerge2.off0 = phi i32 [ %v1_4011c0, %dec_label_pc_401160 ], [ 0, %dec_label_pc_40101c ]
  %v3_401084 = load i32, i32* @global_var_412544.24, align 4
  %v3_40108c = load i32, i32* @global_var_412528.25, align 4
  %v1_401090 = add i32 %v3_401084, -1
  %v2_401094 = mul i32 %v1_401090, %v3_401084
  %v1_401098 = urem i32 %v2_401094, 2
  %v1_40109c = icmp eq i32 %v1_401098, 0
  %v2_40109c = zext i1 %v1_40109c to i32
  %v1_4010a0 = icmp slt i32 %v3_40108c, 10
  %v2_4010a0 = zext i1 %v1_4010a0 to i32
  %v2_4010a4 = and i32 %v2_40109c, %v2_4010a0
  %v2_4010a8 = xor i32 %v2_40109c, %v2_4010a0
  %v1_4010b0 = icmp eq i32 %v2_4010a4, 0
  br i1 %v1_4010b0, label %dec_label_pc_4010c0, label %dec_label_pc_4010d8

dec_label_pc_4010c0:                              ; preds = %dec_label_pc_401080
  %v1_4010c8 = icmp eq i32 %v2_4010a8, 0
  br i1 %v1_4010c8, label %dec_label_pc_4014ac, label %dec_label_pc_4010d8

dec_label_pc_4010d8:                              ; preds = %dec_label_pc_4010c0, %dec_label_pc_401080, %dec_label_pc_4014ac
  %v1_4010dc = icmp slt i32 %storemerge2.off0, 256
  %v1_401120 = icmp eq i32 %v2_4010a8, 0
  br i1 %v1_401120, label %dec_label_pc_401130, label %dec_label_pc_401148

dec_label_pc_401130:                              ; preds = %dec_label_pc_4010d8
  %v2_401108 = icmp sgt i32 %v3_40108c, 9
  %v3_401108 = zext i1 %v2_401108 to i32
  %v2_401110 = or i32 %v1_401098, %v3_401108
  %v1_401138 = icmp eq i32 %v2_401110, 1
  br i1 %v1_401138, label %dec_label_pc_4014ac, label %dec_label_pc_401148

dec_label_pc_401148:                              ; preds = %dec_label_pc_401130, %dec_label_pc_4010d8
  %v1_401150 = icmp eq i1 %v1_4010dc, false
  br i1 %v1_401150, label %dec_label_pc_4011dc, label %dec_label_pc_401160

dec_label_pc_401160:                              ; preds = %dec_label_pc_401148
  %v2_40116c = sext i32 %storemerge2.off0 to i64
  %v4_40116c = mul nsw i64 %v2_40116c, -2113396605
  %v6_40116c = udiv i64 %v4_40116c, 4294967296
  %v7_40116c = trunc i64 %v6_40116c to i32
  %v2_401174 = add i32 %v7_40116c, %storemerge2.off0
  %tmp46 = icmp slt i32 %v2_401174, 0
  %v1_401178 = zext i1 %tmp46 to i32
  %v1_40117c = sdiv i32 %v2_401174, 32
  %v2_401180 = add nsw i32 %v1_40117c, %v1_401178
  %tmp45 = mul i32 %v2_401180, -63
  %v2_40118c = add i32 %tmp45, %storemerge2.off0
  %v1_401190 = mul i32 %v2_40118c, 4
  %v2_40119c = add i32 %v1_401190, ptrtoint (i32* @global_var_412a70.23 to i32)
  %v1_4011a0 = inttoptr i32 %v2_40119c to i32*
  %v2_4011a0 = load i32, i32* %v1_4011a0, align 4
  %v2_4011ac = add i32 %storemerge2.off0, ptrtoint (i32* @global_var_412970.26 to i32)
  %v1_4011b0 = trunc i32 %v2_4011a0 to i8
  %v3_4011b0 = inttoptr i32 %v2_4011ac to i8*
  store i8 %v1_4011b0, i8* %v3_4011b0, align 1
  %v1_4011c0 = add i32 %storemerge2.off0, 1
  br label %dec_label_pc_401080

dec_label_pc_4011dc:                              ; preds = %dec_label_pc_401148, %dec_label_pc_4013d4
  %v3_4013f4 = phi i32 [ %v3_4011e8.pre, %dec_label_pc_4013d4 ], [ %v3_40108c, %dec_label_pc_401148 ]
  %v3_4013ec = phi i32 [ %v3_4011e0.pre, %dec_label_pc_4013d4 ], [ %v3_401084, %dec_label_pc_401148 ]
  %storemerge3 = phi i32 [ %v1_4013d8, %dec_label_pc_4013d4 ], [ 0, %dec_label_pc_401148 ]
  %v1_4011ec = add i32 %v3_4013ec, -1
  %v2_4011f0 = mul i32 %v1_4011ec, %v3_4013ec
  %v1_4011f4 = urem i32 %v2_4011f0, 2
  %v1_4011f8 = icmp eq i32 %v1_4011f4, 0
  %v2_4011f8 = zext i1 %v1_4011f8 to i32
  %v1_4011fc = icmp slt i32 %v3_4013f4, 10
  %v2_4011fc = zext i1 %v1_4011fc to i32
  %v2_401200 = and i32 %v2_4011f8, %v2_4011fc
  %v2_401204 = xor i32 %v2_4011f8, %v2_4011fc
  %v1_40120c = icmp eq i32 %v2_401200, 0
  br i1 %v1_40120c, label %dec_label_pc_40121c, label %dec_label_pc_401234

dec_label_pc_40121c:                              ; preds = %dec_label_pc_4011dc
  %v1_401224 = icmp eq i32 %v2_401204, 0
  br i1 %v1_401224, label %dec_label_pc_4014b4, label %dec_label_pc_401234

dec_label_pc_401234:                              ; preds = %dec_label_pc_40121c, %dec_label_pc_4011dc, %dec_label_pc_4014b4
  %v3_401248 = phi i32 [ %v3_4013f4, %dec_label_pc_40121c ], [ %v3_4013f4, %dec_label_pc_4011dc ], [ %v3_40124813, %dec_label_pc_4014b4 ]
  %v3_401240 = phi i32 [ %v3_4013ec, %dec_label_pc_40121c ], [ %v3_4013ec, %dec_label_pc_4011dc ], [ %v3_40124011, %dec_label_pc_4014b4 ]
  %v1_401238 = icmp slt i32 %storemerge3, 256
  %v1_40124c = add i32 %v3_401240, -1
  %v2_401250 = mul i32 %v1_40124c, %v3_401240
  %v1_401254 = urem i32 %v2_401250, 2
  %v1_401258 = icmp eq i32 %v1_401254, 0
  %v1_40125c = icmp slt i32 %v3_401248, 10
  %v1_40127c = icmp eq i1 %v1_401258, %v1_40125c
  br i1 %v1_40127c, label %dec_label_pc_40128c, label %dec_label_pc_4012a4

dec_label_pc_40128c:                              ; preds = %dec_label_pc_401234
  %v2_401264 = icmp sgt i32 %v3_401248, 9
  %v3_401264 = zext i1 %v2_401264 to i32
  %v2_40126c = or i32 %v1_401254, %v3_401264
  %v1_401294 = icmp eq i32 %v2_40126c, 1
  br i1 %v1_401294, label %dec_label_pc_4014b4, label %dec_label_pc_4012a4

dec_label_pc_4012a4:                              ; preds = %dec_label_pc_40128c, %dec_label_pc_401234
  %v1_4012ac = icmp eq i1 %v1_401238, false
  br i1 %v1_4012ac, label %dec_label_pc_4013e8, label %dec_label_pc_4012bc

dec_label_pc_4012bc:                              ; preds = %dec_label_pc_4012a4
  br i1 %v1_40120c, label %dec_label_pc_4012fc, label %dec_label_pc_401314

dec_label_pc_4012fc:                              ; preds = %dec_label_pc_4012bc
  %v1_401304 = icmp eq i32 %v2_401204, 0
  br i1 %v1_401304, label %dec_label_pc_4014bc, label %dec_label_pc_401314

dec_label_pc_401314:                              ; preds = %dec_label_pc_4012fc, %dec_label_pc_4012bc, %dec_label_pc_4014bc
  %v3_401340 = phi i32 [ %v3_4013f4, %dec_label_pc_4012fc ], [ %v3_4013f4, %dec_label_pc_4012bc ], [ %v3_40134017, %dec_label_pc_4014bc ]
  %v3_401338 = phi i32 [ %v3_4013ec, %dec_label_pc_4012fc ], [ %v3_4013ec, %dec_label_pc_4012bc ], [ %v3_40133815, %dec_label_pc_4014bc ]
  %v2_401320 = add i32 %storemerge3, ptrtoint (i32* @global_var_412970.26 to i32)
  %v1_401324 = inttoptr i32 %v2_401320 to i8*
  %v2_401324 = load i8, i8* %v1_401324, align 1
  %v1_401330 = icmp eq i8 %v2_401324, 47
  %v1_401344 = add i32 %v3_401338, -1
  %v2_401348 = mul i32 %v1_401344, %v3_401338
  %v1_40134c = urem i32 %v2_401348, 2
  %v1_401350 = icmp eq i32 %v1_40134c, 0
  %v2_401350 = zext i1 %v1_401350 to i32
  %v1_401354 = icmp slt i32 %v3_401340, 10
  %v2_401354 = zext i1 %v1_401354 to i32
  %v2_401358 = and i32 %v2_401350, %v2_401354
  %v1_401368 = icmp eq i32 %v2_401358, 0
  br i1 %v1_401368, label %dec_label_pc_401378, label %dec_label_pc_401390

dec_label_pc_401378:                              ; preds = %dec_label_pc_401314
  %v1_401380 = icmp eq i1 %v1_401350, %v1_401354
  br i1 %v1_401380, label %dec_label_pc_4014bc, label %dec_label_pc_401390

dec_label_pc_401390:                              ; preds = %dec_label_pc_401378, %dec_label_pc_401314
  %v1_401398 = icmp eq i1 %v1_401330, false
  br i1 %v1_401398, label %dec_label_pc_4013d4, label %dec_label_pc_4013a8

dec_label_pc_4013a8:                              ; preds = %dec_label_pc_401390
  store i8 0, i8* %v1_401324, align 1
  %v3_4011e0.pre.pre = load i32, i32* @global_var_412544.24, align 4
  %v3_4011e8.pre.pre = load i32, i32* @global_var_412528.25, align 4
  br label %dec_label_pc_4013d4

dec_label_pc_4013d4:                              ; preds = %dec_label_pc_401390, %dec_label_pc_4013a8
  %v3_4011e8.pre = phi i32 [ %v3_4013f4, %dec_label_pc_401390 ], [ %v3_4011e8.pre.pre, %dec_label_pc_4013a8 ]
  %v3_4011e0.pre = phi i32 [ %v3_4013ec, %dec_label_pc_401390 ], [ %v3_4011e0.pre.pre, %dec_label_pc_4013a8 ]
  %v1_4013d8 = add i32 %storemerge3, 1
  br label %dec_label_pc_4011dc

dec_label_pc_4013e8:                              ; preds = %dec_label_pc_4012a4
  br i1 %v1_40120c, label %dec_label_pc_401428, label %dec_label_pc_401440

dec_label_pc_401428:                              ; preds = %dec_label_pc_4013e8
  %v1_401430 = icmp eq i32 %v2_401204, 0
  br i1 %v1_401430, label %dec_label_pc_4014c4, label %dec_label_pc_401440

dec_label_pc_401440:                              ; preds = %dec_label_pc_401428, %dec_label_pc_4013e8, %dec_label_pc_4014c4
  %v3_40144c = phi i32 [ %v3_4013f4, %dec_label_pc_401428 ], [ %v3_4013f4, %dec_label_pc_4013e8 ], [ %v3_40144c23, %dec_label_pc_4014c4 ]
  %v3_401444 = phi i32 [ %v3_4013ec, %dec_label_pc_401428 ], [ %v3_4013ec, %dec_label_pc_4013e8 ], [ %v3_40144421, %dec_label_pc_4014c4 ]
  %v1_401450 = add i32 %v3_401444, -1
  %v2_401454 = mul i32 %v1_401450, %v3_401444
  %v1_401458 = urem i32 %v2_401454, 2
  %v1_40145c = icmp eq i32 %v1_401458, 0
  %v2_40145c = zext i1 %v1_40145c to i32
  %v1_401460 = icmp slt i32 %v3_40144c, 10
  %v2_401460 = zext i1 %v1_401460 to i32
  %v2_401464 = and i32 %v2_40145c, %v2_401460
  %v2_401468 = xor i32 %v2_40145c, %v2_401460
  %v1_401470 = icmp eq i32 %v2_401464, 0
  br i1 %v1_401470, label %dec_label_pc_401480, label %dec_label_pc_401498

dec_label_pc_401480:                              ; preds = %dec_label_pc_401440
  %v1_401488 = icmp eq i32 %v2_401468, 0
  br i1 %v1_401488, label %dec_label_pc_4014c4, label %dec_label_pc_401498

dec_label_pc_401498:                              ; preds = %dec_label_pc_401480, %dec_label_pc_401440
  %v0_4014a8 = phi i32 [ %v2_401468, %dec_label_pc_401480 ], [ %v2_401460, %dec_label_pc_401440 ]
  ret i32 %v0_4014a8

dec_label_pc_4014ac:                              ; preds = %dec_label_pc_401130, %dec_label_pc_4010c0
  br label %dec_label_pc_4010d8

dec_label_pc_4014b4:                              ; preds = %dec_label_pc_40128c, %dec_label_pc_40121c
  %v3_40124813 = phi i32 [ %v3_401248, %dec_label_pc_40128c ], [ %v3_4013f4, %dec_label_pc_40121c ]
  %v3_40124011 = phi i32 [ %v3_401240, %dec_label_pc_40128c ], [ %v3_4013ec, %dec_label_pc_40121c ]
  br label %dec_label_pc_401234

dec_label_pc_4014bc:                              ; preds = %dec_label_pc_401378, %dec_label_pc_4012fc
  %v3_40134017 = phi i32 [ %v3_401340, %dec_label_pc_401378 ], [ %v3_4013f4, %dec_label_pc_4012fc ]
  %v3_40133815 = phi i32 [ %v3_401338, %dec_label_pc_401378 ], [ %v3_4013ec, %dec_label_pc_4012fc ]
  br label %dec_label_pc_401314

dec_label_pc_4014c4:                              ; preds = %dec_label_pc_401480, %dec_label_pc_401428
  %v3_40144c23 = phi i32 [ %v3_40144c, %dec_label_pc_401480 ], [ %v3_4013f4, %dec_label_pc_401428 ]
  %v3_40144421 = phi i32 [ %v3_401444, %dec_label_pc_401480 ], [ %v3_4013ec, %dec_label_pc_401428 ]
  br label %dec_label_pc_401440
}

define i32 @function_4014cc() local_unnamed_addr {
dec_label_pc_4014cc:
  %a0.global-to-local = alloca i32, align 4
  %v0.global-to-local = alloca i32, align 4
  br label %dec_label_pc_401500

dec_label_pc_401500:                              ; preds = %dec_label_pc_4014cc, %dec_label_pc_401500
  %storemerge3 = phi i32 [ 0, %dec_label_pc_4014cc ], [ %v1_4015bc, %dec_label_pc_401500 ]
  %stack_var_-12.02 = phi i32 [ 0, %dec_label_pc_4014cc ], [ %v2_40155c, %dec_label_pc_401500 ]
  store i32 %storemerge3, i32* %v0.global-to-local, align 4
  %v1_401508 = mul i32 %storemerge3, 4
  store i32 ptrtoint (i32* @global_var_412570.19 to i32), i32* %a0.global-to-local, align 4
  %v2_401514 = add i32 %v1_401508, ptrtoint (i32* @global_var_412570.19 to i32)
  %v1_401518 = inttoptr i32 %v2_401514 to i32*
  %v2_401518 = load i32, i32* %v1_401518, align 4
  %v2_4015241 = add i32 %v2_401518, %stack_var_-12.02
  %v2_401534 = add i32 %storemerge3, ptrtoint (i32* @global_var_412970.26 to i32)
  store i32 %v2_401534, i32* %v0.global-to-local, align 4
  %v1_401538 = inttoptr i32 %v2_401534 to i8*
  %v2_401538 = load i8, i8* %v1_401538, align 1
  %v3_401538 = sext i8 %v2_401538 to i32
  %sum = add i32 %v3_401538, %v2_4015241
  store i32 %sum, i32* %v0.global-to-local, align 4
  %v1_401548 = ashr i32 %sum, 31
  %v1_40154c = udiv i32 %v1_401548, 16777216
  %v2_401550 = add i32 %v1_40154c, %sum
  %v2_401558 = and i32 %v2_401550, -256
  %v2_40155c = sub i32 %sum, %v2_401558
  %v2_401570 = load i32, i32* %v1_401518, align 4
  %v1_40157c = mul i32 %v2_40155c, 4
  %v2_401580 = add i32 %v1_40157c, ptrtoint (i32* @global_var_412570.19 to i32)
  %v1_401584 = inttoptr i32 %v2_401580 to i32*
  %v2_401584 = load i32, i32* %v1_401584, align 4
  store i32 %v2_401584, i32* %v1_401518, align 4
  %v0_4015a4 = load i32, i32* %a0.global-to-local, align 4
  %v2_4015a4 = add i32 %v0_4015a4, %v1_40157c
  store i32 %v2_4015a4, i32* %v0.global-to-local, align 4
  %v2_4015a8 = inttoptr i32 %v2_4015a4 to i32*
  store i32 %v2_401570, i32* %v2_4015a8, align 4
  %v1_4015bc = add i32 %storemerge3, 1
  %v1_4014ec = icmp slt i32 %v1_4015bc, 256
  %v1_4014f0 = icmp eq i1 %v1_4014ec, false
  br i1 %v1_4014f0, label %dec_label_pc_4015cc, label %dec_label_pc_401500

dec_label_pc_4015cc:                              ; preds = %dec_label_pc_401500
  %v0_4015dc = load i32, i32* %v0.global-to-local, align 4
  ret i32 %v0_4015dc
}

define i32 @function_4015e0(i32 %arg1, i32 %arg2) local_unnamed_addr {
dec_label_pc_4015e0:
  %a0.global-to-local = alloca i32, align 4
  %a1.global-to-local = alloca i32, align 4
  %a2.global-to-local = alloca i32, align 4
  %a3.global-to-local = alloca i32, align 4
  %at.global-to-local = alloca i32, align 4
  %t0.global-to-local = alloca i32, align 4
  %t1.global-to-local = alloca i32, align 4
  %t2.global-to-local = alloca i32, align 4
  %t3.global-to-local = alloca i32, align 4
  %v0.global-to-local = alloca i32, align 4
  %v1.global-to-local = alloca i32, align 4
  store i32 %arg2, i32* %a1.global-to-local, align 4
  store i32 %arg1, i32* %a0.global-to-local, align 4
  %stack_var_-48 = alloca i32, align 4
  %v2_4015e0 = ptrtoint i32* %stack_var_-48 to i32
  %v3_4015f0 = load i32, i32* @global_var_412530.27, align 4
  %v3_4015f8 = load i32, i32* @global_var_41254c.28, align 4
  %v1_4015fc = add i32 %v3_4015f0, -1
  %v2_401600 = mul i32 %v1_4015fc, %v3_4015f0
  %v1_401604 = urem i32 %v2_401600, 2
  %v1_401608 = icmp eq i32 %v1_401604, 0
  %v2_401608 = zext i1 %v1_401608 to i32
  %v1_40160c = icmp slt i32 %v3_4015f8, 10
  %v2_40160c = zext i1 %v1_40160c to i32
  store i32 %v2_40160c, i32* %a2.global-to-local, align 4
  store i32 9, i32* %a3.global-to-local, align 4
  %v2_401614 = icmp sgt i32 %v3_4015f8, 9
  %v3_401614 = zext i1 %v2_401614 to i32
  store i32 %v3_401614, i32* %v0.global-to-local, align 4
  %v2_401618 = xor i32 %v2_401608, %v2_40160c
  store i32 %v2_401618, i32* %v1.global-to-local, align 4
  %v2_40161c = or i32 %v1_401604, %v3_401614
  %v1_401620 = xor i32 %v2_40161c, 1
  store i32 %v1_401620, i32* %at.global-to-local, align 4
  %v0_401628 = load i32, i32* %a1.global-to-local, align 4
  %v0_40162c = load i32, i32* %a0.global-to-local, align 4
  %v1_401630 = icmp eq i32 %v2_401618, 0
  br i1 %v1_401630, label %dec_label_pc_401640, label %dec_label_pc_401658

dec_label_pc_401640:                              ; preds = %dec_label_pc_4015e0
  store i32 %v1_401620, i32* %at.global-to-local, align 4
  store i32 %v1_401620, i32* %v0.global-to-local, align 4
  %v1_401648 = icmp eq i32 %v1_401620, 0
  br i1 %v1_401648, label %dec_label_pc_4018dc, label %dec_label_pc_401658

dec_label_pc_401658:                              ; preds = %dec_label_pc_401640, %dec_label_pc_4015e0, %dec_label_pc_4018dc
  %v0_401658 = phi i32 [ %v2_4015e0, %dec_label_pc_401640 ], [ %v2_4015e0, %dec_label_pc_4015e0 ], [ %v0_401658.pre, %dec_label_pc_4018dc ]
  %v1_40165c = add i32 %v0_401658, -8
  store i32 %v1_40165c, i32* %v0.global-to-local, align 4
  %v1_401668 = add i32 %v0_401658, -16
  store i32 %v1_401668, i32* %v1.global-to-local, align 4
  store i32 %v1_401668, i32* %a0.global-to-local, align 4
  %v1_401674 = add i32 %v0_401658, -24
  store i32 %v1_401674, i32* @a1, align 4
  store i32 %v1_401674, i32* %a2.global-to-local, align 4
  %v1_401680 = add i32 %v0_401658, -32
  store i32 %v1_401680, i32* %a3.global-to-local, align 4
  %v1_40168c = add i32 %v0_401658, -40
  store i32 %v1_40168c, i32* %t0.global-to-local, align 4
  %v1_401698 = add i32 %v0_401658, -48
  store i32 %v1_401698, i32* %t1.global-to-local, align 4
  %v1_4016a4 = add i32 %v0_401658, -56
  store i32 %v1_4016a4, i32* %t2.global-to-local, align 4
  %v1_4016b0 = add i32 %v0_401658, -64
  store i32 %v1_4016b0, i32* %t3.global-to-local, align 4
  %v3_4016bc = inttoptr i32 %v1_40165c to i32*
  store i32 %v0_40162c, i32* %v3_4016bc, align 4
  store i32 %v0_401628, i32* %at.global-to-local, align 4
  %v1_4016c4 = load i32, i32* %v0.global-to-local, align 4
  %v2_4016c4 = add i32 %v1_4016c4, -8
  %v3_4016c4 = inttoptr i32 %v2_4016c4 to i32*
  store i32 %v0_401628, i32* %v3_4016c4, align 4
  %v0_4016c8 = load i32, i32* %t2.global-to-local, align 4
  %v1_4016c8 = add i32 %v0_4016c8, -8
  %v2_4016c8 = inttoptr i32 %v1_4016c8 to i32*
  store i32 0, i32* %v2_4016c8, align 4
  %v0_4016cc = load i32, i32* %a2.global-to-local, align 4
  %v1_4016cc = add i32 %v0_4016cc, -8
  %v2_4016cc = inttoptr i32 %v1_4016cc to i32*
  store i32 0, i32* %v2_4016cc, align 4
  %v0_4016d0 = load i32, i32* %a0.global-to-local, align 4
  %v1_4016d0 = add i32 %v0_4016d0, -8
  %v2_4016d0 = inttoptr i32 %v1_4016d0 to i32*
  store i32 0, i32* %v2_4016d0, align 4
  %v3_4016d8 = load i32, i32* @global_var_412530.27, align 4
  %v3_4016e0 = load i32, i32* @global_var_41254c.28, align 4
  %v1_4016e4 = add i32 %v3_4016d8, -1
  %v2_4016e8 = mul i32 %v1_4016e4, %v3_4016d8
  %v1_4016ec = urem i32 %v2_4016e8, 2
  %v1_4016f0 = icmp eq i32 %v1_4016ec, 0
  %v2_4016f0 = zext i1 %v1_4016f0 to i32
  %v1_4016f4 = icmp slt i32 %v3_4016e0, 10
  %v2_4016f4 = zext i1 %v1_4016f4 to i32
  store i32 %v2_4016f4, i32* %t2.global-to-local, align 4
  %v2_4016fc = icmp sgt i32 %v3_4016e0, 9
  %v3_4016fc = zext i1 %v2_4016fc to i32
  store i32 %v3_4016fc, i32* %a0.global-to-local, align 4
  %v2_401700 = xor i32 %v2_4016f0, %v2_4016f4
  store i32 %v2_401700, i32* %a2.global-to-local, align 4
  %v2_401704 = or i32 %v1_4016ec, %v3_4016fc
  %v1_401708 = xor i32 %v2_401704, 1
  store i32 %v1_401708, i32* %v0.global-to-local, align 4
  %v0_401710 = load i32, i32* %v1.global-to-local, align 4
  %v0_401714 = load i32, i32* %t1.global-to-local, align 4
  %v0_401718 = load i32, i32* @a1, align 4
  %v0_40171c = load i32, i32* %t3.global-to-local, align 4
  %v0_401720 = load i32, i32* %a3.global-to-local, align 4
  %v0_401724 = load i32, i32* %t0.global-to-local, align 4
  %v1_401728 = icmp eq i32 %v2_401700, 0
  br i1 %v1_401728, label %dec_label_pc_401738, label %dec_label_pc_401758.preheader

dec_label_pc_401738:                              ; preds = %dec_label_pc_401658
  store i32 %v1_401708, i32* %at.global-to-local, align 4
  store i32 %v1_401708, i32* %v0.global-to-local, align 4
  %v1_401740 = icmp eq i32 %v1_401708, 0
  br i1 %v1_401740, label %dec_label_pc_401738.dec_label_pc_4018dc_crit_edge, label %dec_label_pc_401758.preheader

dec_label_pc_401738.dec_label_pc_4018dc_crit_edge: ; preds = %dec_label_pc_401738
  %v0_4018dc.pre = load i32, i32* @sp, align 4
  br label %dec_label_pc_4018dc

dec_label_pc_401758.preheader:                    ; preds = %dec_label_pc_401738, %dec_label_pc_401658
  store i32 %v0_401710, i32* %at.global-to-local, align 4
  %v1_40175c = inttoptr i32 %v0_401710 to i32*
  %v2_40175c1 = load i32, i32* %v1_40175c, align 4
  store i32 %v2_40175c1, i32* %v0.global-to-local, align 4
  %v1_4017602 = add i32 %v2_40175c1, -1
  store i32 %v1_4017602, i32* %v1.global-to-local, align 4
  store i32 %v1_4017602, i32* %v1_40175c, align 4
  %v0_4017683 = load i32, i32* %v0.global-to-local, align 4
  %v1_4017684 = icmp eq i32 %v0_4017683, 0
  br i1 %v1_4017684, label %dec_label_pc_4018c8, label %dec_label_pc_401778.lr.ph

dec_label_pc_401778.lr.ph:                        ; preds = %dec_label_pc_401758.preheader
  %v1_40177c = inttoptr i32 %v0_401718 to i32*
  %v1_4017a4 = inttoptr i32 %v0_401720 to i32*
  %v2_4017fc = inttoptr i32 %v0_401724 to i32*
  %v2_401878 = inttoptr i32 %v0_401714 to i32*
  %v1_401890 = inttoptr i32 %v0_40171c to i32*
  br label %dec_label_pc_401778

dec_label_pc_401778:                              ; preds = %dec_label_pc_401778.lr.ph, %dec_label_pc_401778
  store i32 %v0_401718, i32* %at.global-to-local, align 4
  %v2_40177c = load i32, i32* %v1_40177c, align 4
  %v1_401780 = add i32 %v2_40177c, 1
  %v1_401784 = ashr i32 %v1_401780, 31
  %v1_401788 = udiv i32 %v1_401784, 16777216
  %v2_40178c = add i32 %v1_401788, %v1_401780
  store i32 -256, i32* %a0.global-to-local, align 4
  %v2_401794 = and i32 %v2_40178c, -256
  store i32 %v2_401794, i32* %v1.global-to-local, align 4
  %v2_401798 = sub i32 %v1_401780, %v2_401794
  store i32 %v2_401798, i32* %v1_40177c, align 4
  store i32 %v0_401720, i32* %v0.global-to-local, align 4
  %v2_4017a4 = load i32, i32* %v1_4017a4, align 4
  store i32 %v2_4017a4, i32* %v1.global-to-local, align 4
  %v0_4017a8 = load i32, i32* %at.global-to-local, align 4
  %v1_4017a8 = inttoptr i32 %v0_4017a8 to i32*
  %v2_4017a8 = load i32, i32* %v1_4017a8, align 4
  store i32 ptrtoint (i32* @global_var_412570.19 to i32), i32* %a2.global-to-local, align 4
  %v1_4017b4 = mul i32 %v2_4017a8, 4
  %v2_4017b8 = add i32 %v1_4017b4, ptrtoint (i32* @global_var_412570.19 to i32)
  store i32 %v2_4017b8, i32* %a1.global-to-local, align 4
  %v1_4017bc = inttoptr i32 %v2_4017b8 to i32*
  %v2_4017bc = load i32, i32* %v1_4017bc, align 4
  store i32 0, i32* %a3.global-to-local, align 4
  %sum = add i32 %v2_4017bc, %v2_4017a4
  store i32 %sum, i32* %a1.global-to-local, align 4
  %v1_4017d0 = ashr i32 %sum, 31
  %v1_4017d4 = udiv i32 %v1_4017d0, 16777216
  store i32 %v1_4017d4, i32* %t0.global-to-local, align 4
  %v2_4017d8 = add i32 %v1_4017d4, %sum
  %v1_4017dc = load i32, i32* %a0.global-to-local, align 4
  %v2_4017dc = and i32 %v1_4017dc, %v2_4017d8
  %v2_4017e0 = sub i32 %sum, %v2_4017dc
  store i32 %v2_4017e0, i32* %v1.global-to-local, align 4
  store i32 %v2_4017e0, i32* %v1_4017a4, align 4
  %v0_4017e8 = load i32, i32* %at.global-to-local, align 4
  %v1_4017e8 = inttoptr i32 %v0_4017e8 to i32*
  %v2_4017e8 = load i32, i32* %v1_4017e8, align 4
  %v1_4017ec = mul i32 %v2_4017e8, 4
  %v0_4017f0 = load i32, i32* %a2.global-to-local, align 4
  %v2_4017f0 = add i32 %v0_4017f0, %v1_4017ec
  store i32 %v2_4017f0, i32* %v1.global-to-local, align 4
  %v1_4017f4 = inttoptr i32 %v2_4017f0 to i32*
  %v2_4017f4 = load i32, i32* %v1_4017f4, align 4
  store i32 %v2_4017f4, i32* %v1.global-to-local, align 4
  store i32 %v0_401724, i32* @a1, align 4
  store i32 %v2_4017f4, i32* %v2_4017fc, align 4
  %v0_401800 = load i32, i32* %v0.global-to-local, align 4
  %v1_401800 = inttoptr i32 %v0_401800 to i32*
  %v2_401800 = load i32, i32* %v1_401800, align 4
  %v1_401804 = mul i32 %v2_401800, 4
  %v0_401808 = load i32, i32* %a2.global-to-local, align 4
  %v2_401808 = add i32 %v0_401808, %v1_401804
  store i32 %v2_401808, i32* %v1.global-to-local, align 4
  %v1_40180c = inttoptr i32 %v2_401808 to i32*
  %v2_40180c = load i32, i32* %v1_40180c, align 4
  store i32 %v2_40180c, i32* %v1.global-to-local, align 4
  %v0_401810 = load i32, i32* %at.global-to-local, align 4
  %v1_401810 = inttoptr i32 %v0_401810 to i32*
  %v2_401810 = load i32, i32* %v1_401810, align 4
  %v1_401814 = mul i32 %v2_401810, 4
  %v2_401818 = add i32 %v1_401814, %v0_401808
  store i32 %v2_401818, i32* %t0.global-to-local, align 4
  %v2_40181c = inttoptr i32 %v2_401818 to i32*
  store i32 %v2_40180c, i32* %v2_40181c, align 4
  %v0_401820 = load i32, i32* @a1, align 4
  %v1_401820 = inttoptr i32 %v0_401820 to i32*
  %v2_401820 = load i32, i32* %v1_401820, align 4
  store i32 %v2_401820, i32* %v1.global-to-local, align 4
  %v0_401824 = load i32, i32* %v0.global-to-local, align 4
  %v1_401824 = inttoptr i32 %v0_401824 to i32*
  %v2_401824 = load i32, i32* %v1_401824, align 4
  %v1_401828 = mul i32 %v2_401824, 4
  %v0_40182c = load i32, i32* %a2.global-to-local, align 4
  %v2_40182c = add i32 %v0_40182c, %v1_401828
  store i32 %v2_40182c, i32* %t0.global-to-local, align 4
  %v2_401830 = inttoptr i32 %v2_40182c to i32*
  store i32 %v2_401820, i32* %v2_401830, align 4
  %v0_401834 = load i32, i32* %at.global-to-local, align 4
  %v1_401834 = inttoptr i32 %v0_401834 to i32*
  %v2_401834 = load i32, i32* %v1_401834, align 4
  %v1_401838 = mul i32 %v2_401834, 4
  %v0_40183c = load i32, i32* %a2.global-to-local, align 4
  %v2_40183c = add i32 %v0_40183c, %v1_401838
  store i32 %v2_40183c, i32* %v1.global-to-local, align 4
  %v1_401840 = inttoptr i32 %v2_40183c to i32*
  %v2_401840 = load i32, i32* %v1_401840, align 4
  store i32 %v2_401840, i32* %v1.global-to-local, align 4
  %v0_401844 = load i32, i32* %v0.global-to-local, align 4
  %v1_401844 = inttoptr i32 %v0_401844 to i32*
  %v2_401844 = load i32, i32* %v1_401844, align 4
  %v1_401848 = mul i32 %v2_401844, 4
  %v2_40184c = add i32 %v1_401848, %v0_40183c
  store i32 %v2_40184c, i32* %t0.global-to-local, align 4
  %v1_401850 = inttoptr i32 %v2_40184c to i32*
  %v2_401850 = load i32, i32* %v1_401850, align 4
  %sum20 = add i32 %v2_401850, %v2_401840
  store i32 %sum20, i32* %t0.global-to-local, align 4
  %v1_401860 = ashr i32 %sum20, 31
  %v1_401864 = udiv i32 %v1_401860, 16777216
  store i32 %v1_401864, i32* %t1.global-to-local, align 4
  %v2_401868 = add i32 %v1_401864, %sum20
  %v1_40186c = load i32, i32* %a0.global-to-local, align 4
  %v2_40186c = and i32 %v2_401868, %v1_40186c
  %v2_401870 = sub i32 %sum20, %v2_40186c
  store i32 %v2_401870, i32* %v1.global-to-local, align 4
  store i32 %v0_401714, i32* %a0.global-to-local, align 4
  store i32 %v2_401870, i32* %v2_401878, align 4
  %v0_40187c = load i32, i32* %a0.global-to-local, align 4
  %v1_40187c = inttoptr i32 %v0_40187c to i32*
  %v2_40187c = load i32, i32* %v1_40187c, align 4
  %v1_401880 = mul i32 %v2_40187c, 4
  %v0_401884 = load i32, i32* %a2.global-to-local, align 4
  %v2_401884 = add i32 %v0_401884, %v1_401880
  store i32 %v2_401884, i32* %v1.global-to-local, align 4
  %v1_401888 = inttoptr i32 %v2_401884 to i32*
  %v2_401888 = load i32, i32* %v1_401888, align 4
  store i32 %v2_401888, i32* %v1.global-to-local, align 4
  store i32 %v0_40171c, i32* %a2.global-to-local, align 4
  %v2_401890 = load i32, i32* %v1_401890, align 4
  store i32 ptrtoint (i32* @global_var_412e70.29 to i32), i32* %t1.global-to-local, align 4
  %v1_40189c = mul i32 %v2_401890, 4
  %v2_4018a0 = add i32 %v1_40189c, ptrtoint (i32* @global_var_412e70.29 to i32)
  store i32 %v2_4018a0, i32* %t0.global-to-local, align 4
  %v2_4018a4 = inttoptr i32 %v2_4018a0 to i32*
  store i32 %v2_401888, i32* %v2_4018a4, align 4
  %v0_4018a8 = load i32, i32* %a2.global-to-local, align 4
  %v1_4018a8 = inttoptr i32 %v0_4018a8 to i32*
  %v2_4018a8 = load i32, i32* %v1_4018a8, align 4
  store i32 1, i32* %t0.global-to-local, align 4
  %v2_4018b4 = add i32 %v2_4018a8, 1
  store i32 %v2_4018b4, i32* %v1.global-to-local, align 4
  store i32 %v2_4018b4, i32* %v1_4018a8, align 4
  %v0_4018bc = load i32, i32* %a3.global-to-local, align 4
  store i32 %v0_4018bc, i32* %stack_var_-48, align 4
  store i32 %v0_401710, i32* %at.global-to-local, align 4
  %v2_40175c = load i32, i32* %v1_40175c, align 4
  store i32 %v2_40175c, i32* %v0.global-to-local, align 4
  %v1_401760 = add i32 %v2_40175c, -1
  store i32 %v1_401760, i32* %v1.global-to-local, align 4
  store i32 %v1_401760, i32* %v1_40175c, align 4
  %v0_401768 = load i32, i32* %v0.global-to-local, align 4
  %v1_401768 = icmp eq i32 %v0_401768, 0
  br i1 %v1_401768, label %dec_label_pc_4018c8, label %dec_label_pc_401778

dec_label_pc_4018c8:                              ; preds = %dec_label_pc_401778, %dec_label_pc_401758.preheader
  ret i32 0

dec_label_pc_4018dc:                              ; preds = %dec_label_pc_401738.dec_label_pc_4018dc_crit_edge, %dec_label_pc_401640
  %v0_4018dc = phi i32 [ %v0_4018dc.pre, %dec_label_pc_401738.dec_label_pc_4018dc_crit_edge ], [ %v2_4015e0, %dec_label_pc_401640 ]
  %v1_4018e0 = add i32 %v0_4018dc, -8
  store i32 %v1_4018e0, i32* %v0.global-to-local, align 4
  %v1_4018ec = add i32 %v0_4018dc, -16
  store i32 %v1_4018ec, i32* %v1.global-to-local, align 4
  %v1_4018f8 = add i32 %v0_4018dc, -24
  store i32 %v1_4018f8, i32* %a0.global-to-local, align 4
  %v1_401928 = add i32 %v0_4018dc, -56
  store i32 %v1_401928, i32* %a1.global-to-local, align 4
  store i32 %v0_40162c, i32* %a2.global-to-local, align 4
  %v3_401940 = inttoptr i32 %v1_4018e0 to i32*
  store i32 %v0_40162c, i32* %v3_401940, align 4
  store i32 %v0_401628, i32* %at.global-to-local, align 4
  %v1_401948 = load i32, i32* %v0.global-to-local, align 4
  %v2_401948 = add i32 %v1_401948, -8
  %v3_401948 = inttoptr i32 %v2_401948 to i32*
  store i32 %v0_401628, i32* %v3_401948, align 4
  %v0_40194c = load i32, i32* %a1.global-to-local, align 4
  %v1_40194c = add i32 %v0_40194c, -8
  %v2_40194c = inttoptr i32 %v1_40194c to i32*
  store i32 0, i32* %v2_40194c, align 4
  %v0_401950 = load i32, i32* %a0.global-to-local, align 4
  %v1_401950 = add i32 %v0_401950, -8
  %v2_401950 = inttoptr i32 %v1_401950 to i32*
  store i32 0, i32* %v2_401950, align 4
  %v0_401954 = load i32, i32* %v1.global-to-local, align 4
  %v1_401954 = add i32 %v0_401954, -8
  %v2_401954 = inttoptr i32 %v1_401954 to i32*
  store i32 0, i32* %v2_401954, align 4
  %v0_401658.pre = load i32, i32* @sp, align 4
  br label %dec_label_pc_401658
}

define i32 @function_401960(i32* %arg1) local_unnamed_addr {
dec_label_pc_401960:
  %a0.global-to-local = alloca i32, align 4
  %tmp36 = ptrtoint i32* %arg1 to i32
  store i32 %tmp36, i32* %a0.global-to-local, align 4
  %stack_var_-200 = alloca i32, align 4
  %v0_401970 = load i32, i32* %a0.global-to-local, align 4
  %v2_401984 = ptrtoint i32* %stack_var_-200 to i32
  store i32 %v2_401984, i32* %a0.global-to-local, align 4
  %v5_401994 = call i32* @memcpy(i32* nonnull %stack_var_-200, i32* nonnull @global_var_4022b4.30, i32 176)
  store i32 %v0_401970, i32* %a0.global-to-local, align 4
  %v1_4019a4 = inttoptr i32 %v0_401970 to i8*
  %v2_4019a4 = call i32 @strlen(i8* %v1_4019a4)
  %v2_4019b4 = icmp eq i32 %v2_4019a4, 44
  br i1 %v2_4019b4, label %dec_label_pc_4019d0, label %dec_label_pc_401f0c

dec_label_pc_4019d0:                              ; preds = %dec_label_pc_401960
  %v3_4019d4 = load i32, i32* @global_var_41252c.31, align 4
  %v3_4019dc = load i32, i32* @global_var_412548.32, align 4
  %v1_4019e0 = add i32 %v3_4019d4, -1
  %v2_4019e4 = mul i32 %v1_4019e0, %v3_4019d4
  %v1_4019e8 = urem i32 %v2_4019e4, 2
  %v1_4019ec = icmp eq i32 %v1_4019e8, 0
  %v1_4019f0 = icmp slt i32 %v3_4019dc, 10
  %v2_4019f0 = zext i1 %v1_4019f0 to i32
  store i32 %v2_4019f0, i32* %a0.global-to-local, align 4
  %v1_401a0c = icmp eq i1 %v1_4019ec, %v1_4019f0
  br i1 %v1_401a0c, label %dec_label_pc_401a1c, label %dec_label_pc_401a34

dec_label_pc_401a1c:                              ; preds = %dec_label_pc_4019d0
  %v2_4019f8 = icmp sgt i32 %v3_4019dc, 9
  %v3_4019f8 = zext i1 %v2_4019f8 to i32
  %v2_401a00 = or i32 %v1_4019e8, %v3_4019f8
  %v1_401a24 = icmp eq i32 %v2_401a00, 1
  br i1 %v1_401a24, label %dec_label_pc_401f28, label %dec_label_pc_401a34

dec_label_pc_401a34:                              ; preds = %dec_label_pc_401a1c, %dec_label_pc_4019d0, %dec_label_pc_401f28
  %v2_401a38 = phi i32 [ 9, %dec_label_pc_401a1c ], [ 9, %dec_label_pc_4019d0 ], [ %v2_401a38.pre, %dec_label_pc_401f28 ]
  %v0_401a38 = phi i32 [ %v2_4019f0, %dec_label_pc_401a1c ], [ %v2_4019f0, %dec_label_pc_4019d0 ], [ ptrtoint ([28 x i8]* @global_var_402278.33 to i32), %dec_label_pc_401f28 ]
  %tmp64 = urem i32 %v0_401a38, 2
  %v1_401a38 = icmp ne i32 %tmp64, 0
  %v3_401a38 = call i32 @function_400ea4(i1 %v1_401a38, i32 %v2_401a38)
  %v0_401a40 = call i32 @function_400fec()
  %v0_401a48 = call i32 @function_4014cc()
  store i32 %v0_401970, i32* %a0.global-to-local, align 4
  %v2_401a58 = call i32 @function_4015e0(i32 %v0_401970, i32 44)
  store i32 ptrtoint ([28 x i8]* @global_var_402278.33 to i32), i32* %a0.global-to-local, align 4
  %v3_401a70 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([28 x i8], [28 x i8]* @global_var_402278.33, i32 0, i32 0))
  %v3_401a7c = load i32, i32* @global_var_41252c.31, align 4
  %v3_401a84 = load i32, i32* @global_var_412548.32, align 4
  %v1_401a88 = add i32 %v3_401a7c, -1
  %v2_401a8c = mul i32 %v1_401a88, %v3_401a7c
  %v1_401a90 = urem i32 %v2_401a8c, 2
  %v1_401a94 = icmp eq i32 %v1_401a90, 0
  %v2_401a94 = zext i1 %v1_401a94 to i32
  %v1_401a98 = icmp slt i32 %v3_401a84, 10
  %v2_401a98 = zext i1 %v1_401a98 to i32
  %v2_401a9c = and i32 %v2_401a94, %v2_401a98
  %v2_401aa0 = xor i32 %v2_401a94, %v2_401a98
  store i32 %v2_401aa0, i32* %a0.global-to-local, align 4
  %v1_401aac = icmp eq i32 %v2_401a9c, 0
  br i1 %v1_401aac, label %dec_label_pc_401abc, label %dec_label_pc_401adc

dec_label_pc_401abc:                              ; preds = %dec_label_pc_401a34
  %v1_401ac4 = icmp eq i32 %v2_401aa0, 0
  br i1 %v1_401ac4, label %dec_label_pc_401f28, label %dec_label_pc_401adc

dec_label_pc_401adc:                              ; preds = %dec_label_pc_401c80, %dec_label_pc_401cdc, %dec_label_pc_401a34, %dec_label_pc_401abc
  %v3_401d08 = phi i32 [ %v3_401a84, %dec_label_pc_401abc ], [ %v3_401a84, %dec_label_pc_401a34 ], [ %v3_401c30, %dec_label_pc_401cdc ], [ %v3_401c30, %dec_label_pc_401c80 ]
  %v3_401d00 = phi i32 [ %v3_401a7c, %dec_label_pc_401abc ], [ %v3_401a7c, %dec_label_pc_401a34 ], [ %v3_401c28, %dec_label_pc_401cdc ], [ %v3_401c28, %dec_label_pc_401c80 ]
  %stack_var_-212.0 = phi i32 [ 0, %dec_label_pc_401abc ], [ 0, %dec_label_pc_401a34 ], [ %v2_401c90, %dec_label_pc_401cdc ], [ %v2_401c90, %dec_label_pc_401c80 ]
  %v1_401aec = add i32 %v3_401d00, -1
  %v2_401af0 = mul i32 %v1_401aec, %v3_401d00
  %v1_401af4 = urem i32 %v2_401af0, 2
  %v1_401af8 = icmp eq i32 %v1_401af4, 0
  %v2_401af8 = zext i1 %v1_401af8 to i32
  %v1_401afc = icmp slt i32 %v3_401d08, 10
  %v2_401afc = zext i1 %v1_401afc to i32
  %v2_401b00 = and i32 %v2_401af8, %v2_401afc
  %v1_401b0c = icmp eq i32 %v2_401b00, 0
  br i1 %v1_401b0c, label %dec_label_pc_401b1c, label %dec_label_pc_401b34

dec_label_pc_401b1c:                              ; preds = %dec_label_pc_401adc
  %v1_401b24 = icmp eq i1 %v1_401af8, %v1_401afc
  br i1 %v1_401b24, label %dec_label_pc_401f78, label %dec_label_pc_401b34

dec_label_pc_401b34:                              ; preds = %dec_label_pc_401b1c, %dec_label_pc_401adc, %dec_label_pc_401f78
  %v3_401b4c = phi i32 [ %v3_401d08, %dec_label_pc_401b1c ], [ %v3_401d08, %dec_label_pc_401adc ], [ %v3_401b4c10, %dec_label_pc_401f78 ]
  %v3_401b44 = phi i32 [ %v3_401d00, %dec_label_pc_401b1c ], [ %v3_401d00, %dec_label_pc_401adc ], [ %v3_401b448, %dec_label_pc_401f78 ]
  %v2_401b3c = icmp slt i32 %stack_var_-212.0, 44
  %v1_401b50 = add i32 %v3_401b44, -1
  %v2_401b54 = mul i32 %v1_401b50, %v3_401b44
  %v1_401b58 = urem i32 %v2_401b54, 2
  %v1_401b5c = icmp eq i32 %v1_401b58, 0
  %v2_401b5c = zext i1 %v1_401b5c to i32
  %v1_401b60 = icmp slt i32 %v3_401b4c, 10
  %v2_401b60 = zext i1 %v1_401b60 to i32
  %v2_401b64 = and i32 %v2_401b5c, %v2_401b60
  store i32 %v2_401b64, i32* %a0.global-to-local, align 4
  %v1_401b74 = icmp eq i32 %v2_401b64, 0
  br i1 %v1_401b74, label %dec_label_pc_401b84, label %dec_label_pc_401b9c

dec_label_pc_401b84:                              ; preds = %dec_label_pc_401b34
  %v1_401b8c = icmp eq i1 %v1_401b5c, %v1_401b60
  br i1 %v1_401b8c, label %dec_label_pc_401f78, label %dec_label_pc_401b9c

dec_label_pc_401b9c:                              ; preds = %dec_label_pc_401b84, %dec_label_pc_401b34
  %v1_401ba4 = icmp eq i1 %v2_401b3c, false
  br i1 %v1_401ba4, label %dec_label_pc_401cfc, label %dec_label_pc_401bb4

dec_label_pc_401bb4:                              ; preds = %dec_label_pc_401b9c
  %v1_401bb8 = mul i32 %stack_var_-212.0, 4
  %v2_401bc4 = add i32 %v1_401bb8, ptrtoint (i32* @global_var_412e70.29 to i32)
  %v1_401bc8 = inttoptr i32 %v2_401bc4 to i32*
  %v2_401bc8 = load i32, i32* %v1_401bc8, align 4
  %v2_401bd0 = add i32 %stack_var_-212.0, %v0_401970
  %v1_401bd4 = inttoptr i32 %v2_401bd0 to i8*
  %v2_401bd4 = load i8, i8* %v1_401bd4, align 1
  %v3_401bd465 = zext i8 %v2_401bd4 to i32
  %v1_401bd8 = and i32 %v2_401bc8, 783274286
  %v2_401be4 = xor i32 %v1_401bd8, 783274286
  store i32 %v2_401be4, i32* %a0.global-to-local, align 4
  %v2_401c08 = xor i32 %v2_401bc8, %v3_401bd465
  %v2_401c14 = add i32 %stack_var_-212.0, ptrtoint (i32* @global_var_462e66.35 to i32)
  %v1_401c18 = trunc i32 %v2_401c08 to i8
  %v3_401c18 = inttoptr i32 %v2_401c14 to i8*
  store i8 %v1_401c18, i8* %v3_401c18, align 1
  %v3_401c28 = load i32, i32* @global_var_41252c.31, align 4
  %v3_401c30 = load i32, i32* @global_var_412548.32, align 4
  %v1_401c34 = add i32 %v3_401c28, -1
  %v2_401c38 = mul i32 %v1_401c34, %v3_401c28
  %v1_401c3c = urem i32 %v2_401c38, 2
  %v2_401c44 = icmp sgt i32 %v3_401c30, 9
  %v3_401c44 = zext i1 %v2_401c44 to i32
  %v1_401c58 = icmp eq i32 %v3_401c44, %v1_401c3c
  br i1 %v1_401c58, label %dec_label_pc_401c68, label %dec_label_pc_401c80

dec_label_pc_401c68:                              ; preds = %dec_label_pc_401bb4
  %v2_401c4c = or i32 %v1_401c3c, %v3_401c44
  %v1_401c70 = icmp eq i32 %v2_401c4c, 1
  br i1 %v1_401c70, label %dec_label_pc_401f80, label %dec_label_pc_401c80

dec_label_pc_401c80:                              ; preds = %dec_label_pc_401c68, %dec_label_pc_401bb4, %dec_label_pc_401f80
  %stack_var_-212.1 = phi i32 [ %v1_401f84, %dec_label_pc_401f80 ], [ %stack_var_-212.0, %dec_label_pc_401c68 ], [ %stack_var_-212.0, %dec_label_pc_401bb4 ]
  %v2_401c90 = add i32 %stack_var_-212.1, 1
  %v1_401cb4 = icmp eq i32 %v1_401c3c, 0
  %v2_401cb4 = zext i1 %v1_401cb4 to i32
  %v1_401cb8 = icmp slt i32 %v3_401c30, 10
  %v2_401cb8 = zext i1 %v1_401cb8 to i32
  %v2_401cbc = and i32 %v2_401cb4, %v2_401cb8
  store i32 %v2_401cbc, i32* %a0.global-to-local, align 4
  %v1_401ccc = icmp eq i32 %v2_401cbc, 0
  br i1 %v1_401ccc, label %dec_label_pc_401cdc, label %dec_label_pc_401adc

dec_label_pc_401cdc:                              ; preds = %dec_label_pc_401c80
  %v1_401ce4 = icmp eq i1 %v1_401cb4, %v1_401cb8
  br i1 %v1_401ce4, label %dec_label_pc_401f80, label %dec_label_pc_401adc

dec_label_pc_401cfc:                              ; preds = %dec_label_pc_401b9c
  %v2_401d1c = icmp sgt i32 %v3_401d08, 9
  %v3_401d1c = zext i1 %v2_401d1c to i32
  %v1_401d30 = icmp eq i32 %v1_401af4, %v3_401d1c
  br i1 %v1_401d30, label %dec_label_pc_401d40, label %dec_label_pc_401d58

dec_label_pc_401d40:                              ; preds = %dec_label_pc_401cfc
  %v2_401d24 = or i32 %v1_401af4, %v3_401d1c
  %v1_401d48 = icmp eq i32 %v2_401d24, 1
  br i1 %v1_401d48, label %dec_label_pc_401f94, label %dec_label_pc_401d58

dec_label_pc_401d58:                              ; preds = %dec_label_pc_401d40, %dec_label_pc_401cfc, %dec_label_pc_401f94
  %v3_401d68 = phi i32 [ %v3_401d08, %dec_label_pc_401d40 ], [ %v3_401d08, %dec_label_pc_401cfc ], [ %v3_401d6820, %dec_label_pc_401f94 ]
  %v3_401d60 = phi i32 [ %v3_401d00, %dec_label_pc_401d40 ], [ %v3_401d00, %dec_label_pc_401cfc ], [ %v3_401d6018, %dec_label_pc_401f94 ]
  %v1_401d6c = add i32 %v3_401d60, -1
  %v2_401d70 = mul i32 %v1_401d6c, %v3_401d60
  %v1_401d74 = urem i32 %v2_401d70, 2
  %v1_401d78 = icmp eq i32 %v1_401d74, 0
  %v1_401d7c = icmp slt i32 %v3_401d68, 10
  %v2_401d7c = zext i1 %v1_401d7c to i32
  store i32 %v2_401d7c, i32* %a0.global-to-local, align 4
  %v1_401d98 = icmp eq i1 %v1_401d78, %v1_401d7c
  br i1 %v1_401d98, label %dec_label_pc_401da8, label %dec_label_pc_401dc8.preheader

dec_label_pc_401da8:                              ; preds = %dec_label_pc_401d58
  %v2_401d84 = icmp sgt i32 %v3_401d68, 9
  %v3_401d84 = zext i1 %v2_401d84 to i32
  %v2_401d8c = or i32 %v1_401d74, %v3_401d84
  %v1_401db0 = icmp eq i32 %v2_401d8c, 1
  br i1 %v1_401db0, label %dec_label_pc_401f94, label %dec_label_pc_401dc8.preheader

dec_label_pc_401dc8.preheader:                    ; preds = %dec_label_pc_401da8, %dec_label_pc_401d58
  br label %dec_label_pc_401de4

dec_label_pc_401de4:                              ; preds = %dec_label_pc_401dc8.preheader, %dec_label_pc_401ee8
  %v3_401e30 = phi i32 [ %v3_401d08, %dec_label_pc_401dc8.preheader ], [ %v3_401e94, %dec_label_pc_401ee8 ]
  %v3_401e28 = phi i32 [ %v3_401d00, %dec_label_pc_401dc8.preheader ], [ %v3_401e8c, %dec_label_pc_401ee8 ]
  %stack_var_-20.01 = phi i32 [ 0, %dec_label_pc_401dc8.preheader ], [ %v1_401eec, %dec_label_pc_401ee8 ]
  %v2_401df0 = add i32 %stack_var_-20.01, ptrtoint (i32* @global_var_462e66.35 to i32)
  %v1_401df4 = inttoptr i32 %v2_401df0 to i8*
  %v2_401df4 = load i8, i8* %v1_401df4, align 1
  %v3_401df4 = sext i8 %v2_401df4 to i32
  %v1_401df8 = mul i32 %stack_var_-20.01, 4
  %v2_401e00 = add i32 %v1_401df8, %v2_401984
  %v1_401e04 = inttoptr i32 %v2_401e00 to i32*
  %v2_401e04 = load i32, i32* %v1_401e04, align 4
  %v2_401e08 = icmp eq i32 %v3_401df4, %v2_401e04
  br i1 %v2_401e08, label %dec_label_pc_401e24, label %dec_label_pc_401f0c

dec_label_pc_401e24:                              ; preds = %dec_label_pc_401de4
  %v1_401e34 = add i32 %v3_401e28, -1
  %v2_401e38 = mul i32 %v1_401e34, %v3_401e28
  %v1_401e3c = urem i32 %v2_401e38, 2
  %v1_401e40 = icmp eq i32 %v1_401e3c, 0
  %v1_401e44 = icmp slt i32 %v3_401e30, 10
  %v2_401e44 = zext i1 %v1_401e44 to i32
  store i32 %v2_401e44, i32* %a0.global-to-local, align 4
  %v1_401e60 = icmp eq i1 %v1_401e40, %v1_401e44
  br i1 %v1_401e60, label %dec_label_pc_401e70, label %dec_label_pc_401e88

dec_label_pc_401e70:                              ; preds = %dec_label_pc_401e24
  %v2_401e4c = icmp sgt i32 %v3_401e30, 9
  %v3_401e4c = zext i1 %v2_401e4c to i32
  %v2_401e54 = or i32 %v1_401e3c, %v3_401e4c
  %v1_401e78 = icmp eq i32 %v2_401e54, 1
  br i1 %v1_401e78, label %dec_label_pc_401fa0, label %dec_label_pc_401e88

dec_label_pc_401e88:                              ; preds = %dec_label_pc_401e70, %dec_label_pc_401e24, %dec_label_pc_401fa0
  %v3_401e94 = phi i32 [ %v3_401e30, %dec_label_pc_401e70 ], [ %v3_401e30, %dec_label_pc_401e24 ], [ %v3_401e9426, %dec_label_pc_401fa0 ]
  %v3_401e8c = phi i32 [ %v3_401e28, %dec_label_pc_401e70 ], [ %v3_401e28, %dec_label_pc_401e24 ], [ %v3_401e8c24, %dec_label_pc_401fa0 ]
  %v1_401e98 = add i32 %v3_401e8c, -1
  %v2_401e9c = mul i32 %v1_401e98, %v3_401e8c
  %v1_401ea0 = urem i32 %v2_401e9c, 2
  %v1_401ea4 = icmp eq i32 %v1_401ea0, 0
  %v2_401ea4 = zext i1 %v1_401ea4 to i32
  %v1_401ea8 = icmp slt i32 %v3_401e94, 10
  %v2_401ea8 = zext i1 %v1_401ea8 to i32
  %v2_401eac = and i32 %v2_401ea4, %v2_401ea8
  %v1_401eb8 = icmp eq i32 %v2_401eac, 0
  br i1 %v1_401eb8, label %dec_label_pc_401ec8, label %dec_label_pc_401ee8

dec_label_pc_401ec8:                              ; preds = %dec_label_pc_401e88
  %v1_401ed0 = icmp eq i1 %v1_401ea4, %v1_401ea8
  br i1 %v1_401ed0, label %dec_label_pc_401fa0, label %dec_label_pc_401ee8

dec_label_pc_401ee8:                              ; preds = %dec_label_pc_401e88, %dec_label_pc_401ec8
  %v1_401eec = add nuw nsw i32 %stack_var_-20.01, 1
  %v2_401dd0 = icmp slt i32 %v1_401eec, 44
  %v1_401dd4 = icmp eq i1 %v2_401dd0, false
  br i1 %v1_401dd4, label %dec_label_pc_401efc, label %dec_label_pc_401de4

dec_label_pc_401efc:                              ; preds = %dec_label_pc_401ee8
  br label %dec_label_pc_401f0c

dec_label_pc_401f0c:                              ; preds = %dec_label_pc_401de4, %dec_label_pc_401960, %dec_label_pc_401efc
  %stack_var_-12.0 = phi i32 [ 1, %dec_label_pc_401efc ], [ 0, %dec_label_pc_401960 ], [ 0, %dec_label_pc_401de4 ]
  ret i32 %stack_var_-12.0

dec_label_pc_401f28:                              ; preds = %dec_label_pc_401abc, %dec_label_pc_401a1c
  %v2_401f2c = phi i32 [ %v2_401a98, %dec_label_pc_401abc ], [ 9, %dec_label_pc_401a1c ]
  %v0_401f2c = phi i32 [ 0, %dec_label_pc_401abc ], [ %v2_4019f0, %dec_label_pc_401a1c ]
  %v1_401f2c = icmp ne i32 %v0_401f2c, 0
  %v3_401f2c = call i32 @function_400ea4(i1 %v1_401f2c, i32 %v2_401f2c)
  %v0_401f34 = call i32 @function_400fec()
  %v0_401f3c = call i32 @function_4014cc()
  store i32 %v0_401970, i32* %a0.global-to-local, align 4
  %v2_401f4c = call i32 @function_4015e0(i32 %v0_401970, i32 44)
  store i32 ptrtoint ([28 x i8]* @global_var_402278.33 to i32), i32* %a0.global-to-local, align 4
  %v2_401f64 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([28 x i8], [28 x i8]* @global_var_402278.33, i32 0, i32 0))
  %v2_401a38.pre = load i32, i32* @a1, align 4
  br label %dec_label_pc_401a34

dec_label_pc_401f78:                              ; preds = %dec_label_pc_401b84, %dec_label_pc_401b1c
  %v3_401b4c10 = phi i32 [ %v3_401b4c, %dec_label_pc_401b84 ], [ %v3_401d08, %dec_label_pc_401b1c ]
  %v3_401b448 = phi i32 [ %v3_401b44, %dec_label_pc_401b84 ], [ %v3_401d00, %dec_label_pc_401b1c ]
  br label %dec_label_pc_401b34

dec_label_pc_401f80:                              ; preds = %dec_label_pc_401cdc, %dec_label_pc_401c68
  %stack_var_-212.2 = phi i32 [ %stack_var_-212.0, %dec_label_pc_401c68 ], [ %v2_401c90, %dec_label_pc_401cdc ]
  %v1_401f84 = add i32 %stack_var_-212.2, 1
  br label %dec_label_pc_401c80

dec_label_pc_401f94:                              ; preds = %dec_label_pc_401da8, %dec_label_pc_401d40
  %v3_401d6820 = phi i32 [ %v3_401d68, %dec_label_pc_401da8 ], [ %v3_401d08, %dec_label_pc_401d40 ]
  %v3_401d6018 = phi i32 [ %v3_401d60, %dec_label_pc_401da8 ], [ %v3_401d00, %dec_label_pc_401d40 ]
  br label %dec_label_pc_401d58

dec_label_pc_401fa0:                              ; preds = %dec_label_pc_401ec8, %dec_label_pc_401e70
  %v3_401e9426 = phi i32 [ %v3_401e94, %dec_label_pc_401ec8 ], [ %v3_401e30, %dec_label_pc_401e70 ]
  %v3_401e8c24 = phi i32 [ %v3_401e8c, %dec_label_pc_401ec8 ], [ %v3_401e28, %dec_label_pc_401e70 ]
  br label %dec_label_pc_401e88
}

define i32 @main(i32 %argc, i8** %argv) local_unnamed_addr {
dec_label_pc_401fa8:
  %fp.global-to-local = alloca i32, align 4
  %ra.global-to-local = alloca i32, align 4
  %stack_var_-52 = alloca i32, align 4
  %stack_var_-96 = alloca i32, align 4
  %v2_401fa8 = ptrtoint i32* %stack_var_-96 to i32
  %v0_401fac = load i32, i32* %ra.global-to-local, align 4
  %v0_401fb0 = load i32, i32* %fp.global-to-local, align 4
  store i32 %v2_401fa8, i32* @fp, align 4
  %v2_401fd4 = ptrtoint i32* %stack_var_-52 to i32
  %v6_401fe8 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @global_var_402294.36, i32 0, i32 0), i32* nonnull %stack_var_-52)
  %v1_401ff8 = call i32 @function_4007a0(i32 %v2_401fd4)
  %v2_402008 = call i32 @function_401960(i32* nonnull @global_var_472e64.18)
  %v2_402018 = icmp eq i32 %v2_402008, 1
  br i1 %v2_402018, label %dec_label_pc_402028, label %dec_label_pc_402044

dec_label_pc_402028:                              ; preds = %dec_label_pc_401fa8
  %v3_402034 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @global_var_402297.37, i32 0, i32 0))
  br label %dec_label_pc_402060

dec_label_pc_402044:                              ; preds = %dec_label_pc_401fa8
  %v3_402050 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([14 x i8], [14 x i8]* @global_var_4022a5.38, i32 0, i32 0))
  br label %dec_label_pc_402060

dec_label_pc_402060:                              ; preds = %dec_label_pc_402044, %dec_label_pc_402028
  store i32 %v0_401fb0, i32* %fp.global-to-local, align 4
  store i32 %v0_401fac, i32* %ra.global-to-local, align 4
  ret i32 0
}

declare i32 @printf(i8*, ...) local_unnamed_addr

declare i32* @memcpy(i32*, i32*, i32) local_unnamed_addr

declare i32 @scanf(i8*, ...) local_unnamed_addr

declare i32 @strlen(i8*) local_unnamed_addr
