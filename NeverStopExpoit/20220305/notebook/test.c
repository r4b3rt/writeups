#include <stdio.h>
#include <stdlib.h>

int main() {
    void *t[7];
    void *r = malloc(0x28);
    for (int i = 0; i < 7; i++) {
        t[i] = malloc(0x208);
    }
    void *p = malloc(0x208);
    malloc(0x18);
    void *q = malloc(0x208);
    malloc(0x18);
    printf("p = %p\n", p);
    printf("q = %p\n", q);
    free(r);
    for (int i = 0; i < 7; i++) {
        free(t[i]);
    }
    free(p);
    free(q);
    p = malloc(0x208);
    q = malloc(0x208);
    printf("p = %p\n", p);
    printf("q = %p\n", q);
    return 0;
}
