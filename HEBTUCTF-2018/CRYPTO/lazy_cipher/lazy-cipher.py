enc = 'EULS LS I XCISSLXIC SHNEHNXH: EUH VWLXF YDAKN OAR MWBJS AZHD EUH CIPT GAQ! OLQUE, ING TAW BIT GLH. DWN, ING TAW\'CC CLZH IE CHISE I KULCH. ING GTLNQ LN TAWD YHGS BINT THIDS ODAB NAK. KAWCG TAW YH KLCCLNQ EA EDIGH? ICC EUH GITS ODAB EULS GIT EA EUIE, OAD ANH XUINXH, MWSE ANH XUINXH, EA XABH YIXF UHDH ING EHCC AWD HNHBLHS EUIE EUHT BIT EIFH AWD CLZHS, YWE EUHT\'CC NHZHD EIFH AWD OCIQ!OCIQ LS UHYEWXEO KLONZGSOOGTWYJIBHBS.'
dic = {
    'A': 'o',
    'B': 'm',
    'C': 'l',
    'D': 'r',
    'E': 't',
    'F': 'k',
    'G': 'd',
    'H': 'e',
    'I': 'a',
    'J': 'p',
    'K': 'w',
    'L': 'i',
    'M': 'j',
    'N': 'n',
    'O': 'f',
    'P': 'z',
    'Q': 'g',
    'R': 'x',
    'S': 's',
    'T': 'y',
    'U': 'h',
    'V': 'q',
    'W': 'u',
    'X': '',
    'Y': 'b',
    'X': 'c',
    'Z': 'v',
}
res = ''
for ch in enc:
    flag = False
    for key, value in dic.items():
        if ch == key and value != '':
            res += value
            flag = True
            break
        else:
            continue
    if flag == True:
        continue
    else:
        res += ch
print res