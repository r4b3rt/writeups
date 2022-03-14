#include <stdio.h>
#include <stdlib.h>

int main() {
    void *p = malloc(0x18);
    void *q = malloc(0x28);
    free(p);
    free(q);
    return 0;
}

