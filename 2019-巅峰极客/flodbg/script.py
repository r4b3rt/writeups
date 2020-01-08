from ida_bytes import get_bytes,patch_bytes

addr =0x4009A4
end = 0x400C51

pattern1 = "EBFFC0FFC8".lower()
pattern2 = "E8 00 00 00 00 58 48 83 C0 0A FF E0 EB EB EB".replace(' ','').lower()
pattern3 = "E8 00 00 00 00 5B 48 83 C3 0A FF E3 EB EB EB".replace(' ','').lower()
pattern4 = "66 B8 EB 05 31 C0 74 FA EB".replace(' ','').lower()
pattern5 = "E8 00 00 00 00 58 48 83 C0 0C FF E0 EB EB EB EB EB".replace(' ','').lower()
#print(pattern2)

buf_hex = get_bytes(addr,end - addr).encode('hex').lower()

buf_hex = buf_hex.replace(pattern1,'90'*(len(pattern1)/2))
buf_hex = buf_hex.replace(pattern2,'90'*(len(pattern2)/2))
buf_hex = buf_hex.replace(pattern3,'90'*(len(pattern3)/2))
buf_hex = buf_hex.replace(pattern4,'90'*(len(pattern4)/2))
buf_hex = buf_hex.replace(pattern5,'90'*(len(pattern5)/2))

buf = buf_hex.decode('hex')
patch_bytes(addr,buf)
print('done')
