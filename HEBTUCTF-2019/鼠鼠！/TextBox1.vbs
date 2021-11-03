Sub Document_Open()
Dim key As Integer
Dim flag_part2 As String
Dim flag_part2_Value() As Byte
Dim flag_part2_enc As String
key = 5 'Key maybe Wrong!
flag_part2 = "8?-?2??-?b?b" 'Some bit is wrong
flag_part2_Value = StrConv(flag_part2, vbFromUnicode)
Dim i As Long
For i = LBound(flag_part2_Value) To UBound(flag_part2_Value)
flag_part2_Value(i) = flag_part2_Value(i) Xor key
flag_part2_enc = flag_part2_enc + StrConv(flag_part2_Value(i), vbToUnicode)
Next
MsgBox flag_part2_enc
flag_part2_enc = "29'>823'hhlh"
End Sub
