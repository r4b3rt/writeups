#include <idc.idc>

static main() {
    auto i;
    for(i = 14997; i >= 0; i = i - 3) {
        auto v0 = Byte(0x6010C0 + i);
        auto v3 = Byte(0x6010C0 + (i + 2));
        auto result = v0;
        if(v0 == 1) {
            result = Byte(0x6010C0 + (i + 1));
            PatchByte(0x601060 + result * 4, Byte(0x601060 + result * 4) - v3);
        } if(v0 == 2) {
            result = Byte(0x6010C0 + (i + 1));
            PatchByte(0x601060 + result * 4,Byte(0x601060 + result * 4) + v3);
        } if(v0 ==3 ) {
            result = Byte(0x6010C0 + (i + 1));
            PatchByte(0x601060 + result * 4,Byte(0x601060 + result * 4) ^ v3);
        } if(v0 == 4) {
            result = Byte(0x6010C0 + (i + 1));
            PatchByte(0x601060 + result * 4,Byte(0x601060 + result * 4) / v3);
        } if(v0 == 5) {
            result = Byte(0x6010C0 + (i + 1));
            PatchByte(0x601060 + result * 4, Byte(0x601060 + result * 4) ^ Byte(0x601060 + v3 * 4));
        } else {
            continue;
        }
    }
    for(i = 0; i < 24; i++) {
        Message("%c", Byte(0x601060 + i * 4));
    }
}

// https://blog.csdn.net/whklhhhh/article/details/74793530