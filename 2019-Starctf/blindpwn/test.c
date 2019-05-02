#include <stdio.h>
#include <stdlib.h>

void vul() {
	char buf[0x20];
	puts("Welcome!");
	read(0, buf, 0x100);
	puts("Goodbye!");	
}

int main() {
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	vul();
}
