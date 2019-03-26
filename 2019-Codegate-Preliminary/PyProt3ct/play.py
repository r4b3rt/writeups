def f0(dic):
    str1=2001
    str2=2002
    x46=dic[str1]
    x46=x46.decode("utf-8")
    x11=dic[str2]
    x11=x11.decode("utf-8")
    x11=int(x11)
    dic[x46]=x11
    return
def f1(dic):
    str1=2001
    str2=2002
    x0=dic[str1]
    x0=x0.decode("utf-8")
    x42=dic[str2]
    x42=x42.decode("utf-8")
    x42=dic[x42]
    dic[x0]=x42
    return
def f2(dic):
    str1=2001
    str2=2002
    str3=2003
    x10=dic[str1]
    x10=x10.decode("utf-8")
    x25=dic[str2]
    x25=x25.decode("utf-8")
    x25=dic[x25]
    x58=dic[str3]
    x58=x58.decode("utf-8")
    if x58.isdigit():
        x58=int(x58)
    else:
        x58=dic[x58]
    x74=x25[x58]
    dic[x10]=x74
    return
def f3(dic):
    str1=2001
    str2=2002
    str3=2003
    str4=2004
    x77=dic[str1]
    x77=x77.decode("utf-8")
    x83=dic[str2]
    x83=x83.decode("utf-8")
    x72=dic[str3]
    x72=x72.decode("utf-8")
    if x72.isdigit():
        x72=int(x72)
    else:
        x72=dic[x72]
    x71=dic[str4]
    x71=x71.decode("utf-8")
    if x71.isdigit():
        x71=int(x71)
    else:
        x71=dic[x71]
    x29=x83[x72:x71]
    dic[x77]=x29
    return
def f4(dic):
    str1=2001
    str2=2002
    str3=2003
    x61=dic[str1]
    x61=x61.decode("utf-8")
    x79=dic[str2]
    x79=x79.decode("utf-8")
    if x79.isdigit():
        x79=int(x79)
    else:
        x79=dic[x79]
    x14=dic[str3]
    x14=x14.decode("utf-8")
    if x14.isdigit():
        x14=int(x14)
    else:
        x14=dic[x14]
    x69=dic[x61]
    x69[x79]=x14
    return
def f5(dic):
    str1=2001
    str2=2002
    str3=2003
    x67=dic[str1]
    x67=x67.decode("utf-8")
    x84=dic[str2]
    x84=x84.decode("utf-8")
    if x84.isdigit():
        x84=int(x84)
    else:
        x84=dic[x84]
    x22=dic[str3]
    x22=x22.decode("utf-8")
    if x22.isdigit():
        x22=int(x22)
    else:
        x22=dic[x22]
    x48=x84+x22
    dic[x67]=x48
    return
def f6(dic):
    str1=2001
    str2=2002
    str3=2003
    x81=dic[str1]
    x81=x81.decode("utf-8")
    x7=dic[str2]
    x7=x7.decode("utf-8")
    if x7.isdigit():
        x7=int(x7)
    else:
        x7=dic[x7]
    x70=dic[str3]
    x70=x70.decode("utf-8")
    if x70.isdigit():
        x70=int(x70)
    else:
        x70=dic[x70]
    x26=x7^x70
    dic[x81]=x26
    return
def op_and(dic):
    str1=2001
    str2=2002
    str3=2003
    x92=dic[str1]
    x92=x92.decode("utf-8")
    x6=dic[str2]
    x6=x6.decode("utf-8")
    if x6.isdigit():
        x6=int(x6)
    else:
        x6=dic[x6]
    x60=dic[str3]
    x60=x60.decode("utf-8")
    if x60.isdigit():
        x60=int(x60)
    else:
        x60=dic[x60]
    x3=x6&x60
    dic[x92]=x3
    print('[%s] = and %s, %s' % (x92, x6, x60))
    return
def op_or(dic):
    str1=2001
    str2=2002
    str3=2003
    x76=dic[str1]
    x76=x76.decode("utf-8")
    x62=dic[str2]
    x62=x62.decode("utf-8")
    if x62.isdigit():
        x62=int(x62)
    else:
        x62=dic[x62]
    x53=dic[str3]
    x53=x53.decode("utf-8")
    if x53.isdigit():
        x53=int(x53)
    else:
        x53=dic[x53]
    x64=x62|x53
    dic[x76]=x64
    print('[%s] = or %s, %s' % (x76, x62, x53))
    return
def op_shr(dic):
    str1=2001
    str2=2002
    str3=2003
    x28=dic[str1]
    x28=x28.decode("utf-8")
    x85=dic[str2]
    x85=x85.decode("utf-8")
    if x85.isdigit():
        x85=int(x85)
    else:
        x85=dic[x85]
    x89=dic[str3]
    x89=x89.decode("utf-8")
    if x89.isdigit():
        x89=int(x89)
    else:
        x89=dic[x89]
    x50=x85>>x89
    dic[x28]=x50
    print('[%s] = shr %s, %s' % (x28, x85, x89))
    return
def op_shl(dic):
    str1=2001
    str2=2002
    str3=2003
    x68=dic[str1]
    x68=x68.decode("utf-8")
    x93=dic[str2]
    x93=x93.decode("utf-8")
    if x93.isdigit():
        x93=int(x93)
    else:
        x93=dic[x93]
    x57=dic[str3]
    x57=x57.decode("utf-8")
    if x57.isdigit():
        x57=int(x57)
    else:
        x57=dic[x57]
    x91=x93<<x57
    dic[x68]=x91
    print('[%s] = shl %s, %s' % (x68, x93, x57))
    return
def f11(dic):
    str1=2001
    str2=2002
    ret_val=1001
    x52=dic[str1]
    x52=x52.decode("utf-8")
    x13=dic[str2]
    x13=x13.decode("utf-8")
    if x13.isdigit():
        x13=int(x13)
    else:
        x13=dic[x13]
    x44=eval(x52)
    x34=x44(x13)
    dic[ret_val]=x34
    return
def f12(dic):
    str1=2001
    ret_val=1001
    x8=dic[str1]
    x8=x8.decode("utf-8")
    x17=eval(x8)
    x18=x17()
    dic[ret_val]=x18
    return
def f13(dic):
    str1=2001
    ret_val=1001
    x45=dic[str1]
    x45=x45.decode("utf-8")
    if x45.isdigit():
        x45=int(x45)
    else:
        x45=dic[x45]
    dic[ret_val]=x45
    return
def f14(dic):
    str1=2001
    ret_val=1001
    x43=dic[str1]
    x43=x43.decode("utf-8")
    x33=dic[ret_val]
    dic[x43]=x33
    return
def f15(dic):
    str1=2001
    str2=2002
    str3=2003
    ret_addr=1000
    x21=dic[str1]
    x21=x21.decode("utf-8")
    x21=int(x21)
    x24=dic[str2]
    x24=x24.decode("utf-8")
    if x24.isdigit():
        x24=int(x24)
    else:
        x24=dic[x24]
    x40=dic[str3]
    x40=x40.decode("utf-8")
    if x40.isdigit():
        x40=int(x40)
    else:
        x40=dic[x40]
    if x24==x40:
        dic[ret_addr]=x21
    return
def f16(dic):
    str1=2001
    str2=2002
    str3=2003
    ret_addr=1000
    x66=dic[str1]
    x66=x66.decode("utf-8")
    x66=int(x66)
    x55=dic[str2]
    x55=x55.decode("utf-8")
    if x55.isdigit():
        x55=int(x55)
    else:
        x55=dic[x55]
    x37=dic[str3]
    x37=x37.decode("utf-8")
    if x37.isdigit():
        x37=int(x37)
    else:
        x37=dic[x37]
    if x55 !=x37:
        dic[ret_addr]=x66
    return
def f17(dic):
    str1=2001
    str2=2002
    str3=2003
    ret_addr=1000
    x56=dic[str1]
    x56=x56.decode("utf-8")
    x56=int(x56)
    x47=dic[str2]
    x47=x47.decode("utf-8")
    if x47.isdigit():
        x47=int(x47)
    else:
        x47=dic[x47]
    x87=dic[str3]
    x87=x87.decode("utf-8")
    if x87.isdigit():
        x87=int(x87)
    else:
        x87=dic[x87]
    if x47<x87:
        dic[ret_addr]=x56
    return
def f18(dic):
    str1=2001
    str2=2002
    str3=2003
    ret_addr=1000
    x39=dic[str1]
    x39=x39.decode("utf-8")
    x39=int(x39)
    x31=dic[str2]
    x31=x31.decode("utf-8")
    if x31.isdigit():
        x31=int(x31)
    else:
        x31=dic[x31]
    x2=dic[str3]
    x2=x2.decode("utf-8")
    if x2.isdigit():
        x2=int(x2)
    else:
        x2=dic[x2]
    if x31 >=x2:
        dic[ret_addr]=x39
    return
def f19(dic):
    str1=2001
    ret_addr=1000
    x4=dic[str1]
    x4=x4.decode("utf-8")
    x4=int(x4)
    dic[ret_addr]=x4
    return
def O0O0O0O00OO0O0O0O(code, flag):
    dic=dict()
    ret_addr=1000
    ret_val=1001
    str1=2001
    str2=2002
    str3=2003
    str4=2004
    x54=0
    x63=1
    x16=2
    x38=3
    dic[ret_addr]=0
    dic[ret_val]=0
    dic["flag"]=flag
    x51=0
    while x51==0:
        x19=dic[ret_addr]
        x35=code[x19]
        x19=x19+x63
        x15=code[x19]
        x19=x19+x63
        if x54<x15:
            x36=code[x19]
            x19=x19+x63
            x5=x19
            x1=x19+x36
            x75=code[x5:x1]
            dic[str1]=x75
            x19=x19+x36
        if x63<x15:
            x73=code[x19]
            x19=x19+x63
            x65=x19
            x78=x19+x73
            x86=code[x65:x78]
            dic[str2]=x86
            x19=x19+x73
        if x16<x15:
            x49=code[x19]
            x19=x19+x63
            x32=x19
            x82=x19+x49
            x88=code[x32:x82]
            dic[str3]=x88
            x19=x19+x49
        if x38<x15:
            x23=code[x19]
            x19=x19+x63
            x90=x19
            x12=x19+x23
            x9=code[x90:x12]
            dic[str4]=x9
            x19=x19+x23
        dic[ret_addr]=x19
        if x35==0:
            f0(dic)
        elif x35==2:
            f4(dic)
        elif x35==8:
            f18(dic)
        elif x35==11:
            f19(dic)
        elif x35==34:
            f2(dic)
        elif x35==41:
            f11(dic)
        elif x35==44:
            f12(dic)
        elif x35==49:
            f17(dic)
        elif x35==72:
            f14(dic)
        elif x35==74:
            f13(dic)
        elif x35==81:
            f15(dic)
        elif x35==82:
            f1(dic)
        elif x35==91:
            f16(dic)
        elif x35==99:
            f3(dic)
        elif x35==102:
            f5(dic)
        elif x35==111:
            op_or(dic)
        elif x35==131:
            op_and(dic)
        elif x35==151:
            op_shl(dic)
        elif x35==171:
            op_shr(dic)
        elif x35==186:
            f6(dic)
        x19=dic[ret_addr]
        if x35==74:
            x51=1
    x30=dic[ret_val]
    return x30
