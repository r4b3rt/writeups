#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
	int answer = 0;
	char password[6];
	memset(password, 0, sizeof(password));
	scanf("%s", password);
	for(int i = 0; i < 6; i++) {
		answer += (int)password[i] ^ (0x78 + i);
	}
	if(answer == 0) {
		printf("Success!\n");
	} else {
		printf("Failed!\n");
	}
	return 0;
}
