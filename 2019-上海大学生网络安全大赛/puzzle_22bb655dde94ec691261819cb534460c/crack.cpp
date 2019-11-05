#include <stdio.h>
#include <iostream>
#include <algorithm>
using namespace std;

bool check(int *arr)
{
    int *choices; // ecx
    bool result;  // al
    int v0 = 0x8A, v1 = 0x1A1, v2 = 0x12A, v3 = 0x269, v4 = 0x209, v5 = 0x68, v6 = 0x39F, v7 = 0x2C8;
    choices = arr;
    while (2)
    {
        switch (*choices)
        {
        case 0:
            v2 &= v6;
            v3 *= v2;
            goto LABEL_4;
        case 1:
            if (!v3)
                goto LABEL_6;
            v2 /= v3;
            v1 += v5;
            goto LABEL_4;
        case 2:
            v4 ^= v5;
            v7 += v0;
            goto LABEL_4;
        case 3:
            v7 -= v4;
            v4 &= v1;
            goto LABEL_4;
        case 4:
            v5 *= v0;
            v3 -= v6;
            goto LABEL_4;
        case 5:
            v0 ^= v3;
            v6 -= v7;
            goto LABEL_4;
        case 6:
            if (!v7)
                goto LABEL_6;
            v5 |= v1 / v7;
            v1 /= v7;
            goto LABEL_4;
        case 7:
            v6 += v2;
            v5 |= v1;
            goto LABEL_4;
        case 8:
            v0 *= v3;
            v4 -= v7;
            goto LABEL_4;
        case 9:
            v2 += v5;
            v3 ^= v4;
        LABEL_4:
            if (++choices != arr + 8)
                continue;
            result = (v6 == 0xE7) + (v5 == 0x3878) + (v4 == 0x3A71) + (v3 == 0xFFFFCC30) + (v2 == 0x10) + (v1 == 0x68) + (v0 == 0xFFFFFC49) == 7;
            if (v7 != 0xFFFFFF11)
                goto LABEL_6;
            break;
        default:
        LABEL_6:
            result = 0;
            break;
        }
        return result;
    }
}

int main()
{
    int k;
    for (int v0 = 0; v0 < 10; v0++)
    {
        for (int v1 = 0; v1 < 10; v1++)
        {
            for (int v2 = 0; v2 < 10; v2++)
            {
                for (int v3 = 0; v3 < 10; v3++)
                {
                    for (int v4 = 0; v4 < 10; v4++)
                    {
                        for (int v5 = 0; v5 < 10; v5++)
                        {
                            for (int v6 = 0; v6 < 10; v6++)
                            {
                                for (int v7 = 0; v7 < 10; v7++)
                                {
                                    int arr[8] = {v0, v1, v2, v3, v4, v5, v6, v7};
                                    for (int i = 0; i < 8; i++)
                                    {
                                        printf("%d", arr[i]);
                                    }
                                    printf("\n");
                                    if (check(arr) == 1)
                                    {
                                        printf("[*] Cracked.");
                                        for (int i = 0; i < 8; i++)
                                        {
                                            printf("%d\n", arr[i]);
                                        }
                                        return 0;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return -1;
}