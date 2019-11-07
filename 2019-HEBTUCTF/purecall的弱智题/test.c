#include <stdio.h>
#include <string.h>

int main() {
	char input[48]="123\x00";
	int i;
	for ( i = 0; i < strlen(input) - 2 && input[i] <= input[i + 1]; ++i )
		;
	printf("%d\n", strlen(input));
	if ( i == strlen(input) - 2 )
		printf("yes\n");
	return 0;
}
