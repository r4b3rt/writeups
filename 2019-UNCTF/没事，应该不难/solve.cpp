#include <iostream>
#include <cstring>
using namespace std; //enc_flag：密文，长度24.原文长度推测为18

struct sus_slove
{
    int reg1; //记录这个可能解基于前面的哪一个可能解
    int reg2;
    int reg3;
    unsigned char data;
    unsigned char v5; //记录这个疑似解下的v5
};

unsigned char enc_flag[] = {0xb3, 0x9c, 0xb7, 0xbf, 0xb2, 0xcb, 0xd3, 0xbf, 0xB2, 0xCB, 0xD3, 0xC9, 0xB1, 0xCB, 0xD3, 0xBB, 0xAE, 0xAD, 0xA3, 0xCF, 0xAD, 0xCD, 0x9F, 0xBB, 0x00};
unsigned char flag[100];
unsigned char v4 = 0, v5 = 0;   //混淆变量，v4是一个循环群
sus_slove suspect_slove_1[100]; //记录每组第一个字节的可能解
sus_slove suspect_slove_2[1000];
sus_slove suspect_slove_3[10000];
unsigned int reg_1; //记录可能解的数量
unsigned int reg_2;
unsigned int reg_3;

int main()
{
    int temp = 0; //临时变量
    for (int a = 0; a < 6; ++a)
    { //大循环：分组解密，每组4个数字
        memset(suspect_slove_1, 0, sizeof(suspect_slove_1));
        memset(suspect_slove_2, 0, sizeof(suspect_slove_2));
        memset(suspect_slove_3, 0, sizeof(suspect_slove_3));
        reg_1 = 0;
        reg_2 = 0;
        reg_3 = 0;

        v4 = 0;
        v5 = 0;
        //第一组之后的v5是有初值的
        //后面几组的v5初值在循环体中赋予了
        for (unsigned char i = 32; i < 128; ++i)
        { //第一个循环体，寻找第一个字节的可能解
            temp = (v5 | ((int)i >> (v4 + 2))) - 0x6A;
            if ((unsigned char)temp == enc_flag[a * 4])
            {
                suspect_slove_1[reg_1].reg1 = 0;
                suspect_slove_1[reg_1].reg2 = 0;
                suspect_slove_1[reg_1].reg3 = 0;
                suspect_slove_1[reg_1].data = i;
                temp = 0;
                for (int n = 0; n < v4 + 2; ++n)
                {
                    temp |= (i & (1 << n)) << (4 - v4);
                }
                suspect_slove_1[reg_1].v5 = temp;
                ++reg_1;
            }
        }
        if (!reg_1)
        {
            cout << a << " 1_无解！请检查算法！";
            exit(-1);
        }
        v4 = 2;
        for (int i = 0; i < reg_1; ++i)
        { //第二个循环体，寻找第二个字节的可能解
            v5 = suspect_slove_1[i].v5;
            for (unsigned char n = 32; n < 128; ++n)
            {
                temp = (v5 | ((int)n >> (v4 + 2))) - 0x6A;
                if ((unsigned char)temp == enc_flag[a * 4 + 1])
                {
                    suspect_slove_2[reg_2].reg1 = i;
                    suspect_slove_2[reg_2].reg2 = 0;
                    suspect_slove_2[reg_2].reg3 = 0;
                    suspect_slove_2[reg_2].data = n;
                    temp = 0;
                    for (int t = 0; t < v4 + 2; ++t)
                    {
                        temp |= (n & (1 << t)) << (4 - v4);
                    }
                    suspect_slove_2[reg_2++].v5 = temp;
                }
            }
        }
        if (!reg_2)
        {
            cout << "\n2_无解！请检查算法！\n";
            exit(-1);
        }
        v4 = 4;
        for (int i = 0; i < reg_1; ++i)
        {
            for (int n = 0; n < reg_2; ++n)
            {
                if (suspect_slove_2[n].reg1 == i)
                { //判断，只有两个疑似解匹配的时候才进行运算
                    v5 = suspect_slove_2[n].v5;
                }
                else
                    continue;
                for (unsigned char t = 32; t < 128; ++t)
                {
                    temp = (v5 | (t >> (v4 + 2))) - 0x6A;
                    if ((unsigned char)temp == enc_flag[a * 4 + 2])
                    {
                        suspect_slove_3[reg_3].reg1 = i;
                        suspect_slove_3[reg_3].reg2 = n;
                        suspect_slove_3[reg_3].reg3 = 0;
                        suspect_slove_3[reg_3].data = t;
                        temp = 0;
                        for (int f = 0; f < v4 + 2; ++f)
                        {
                            temp |= (t & (1 << f)) << (4 - v4);
                        }
                        suspect_slove_3[reg_3++].v5 = temp;
                    }
                }
            }
        }
        if (!reg_3)
        {
            cout << a << " 3_无解！请检查算法！";
            exit(-1);
        }
        v4 = 6;
        for (int i = 0; i < reg_1; ++i)
        {
            for (int n = 0; n < reg_2; ++n)
            {
                if (suspect_slove_2[n].reg1 != i)
                    continue;
                //判断，只有两个疑似解匹配的时候才进行运算
                for (int t = 0; t < reg_3; ++t)
                {
                    if (suspect_slove_3[t].reg2 == n && (unsigned char)((int)suspect_slove_3[t].v5 - 0x6A) == enc_flag[a * 4 + 3])
                    { //判断，只有三个疑似解匹配的时候才进行运算
                        cout << suspect_slove_1[i].data << suspect_slove_2[n].data << suspect_slove_3[t].data;
                        goto done;
                    }
                }
            }
        }
    done:;
    }
    return 0;
}