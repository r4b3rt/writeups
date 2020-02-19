#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *table = "ncA8DaUPelq*S7Y9q#hLl0T##@XTuXHQpFA&65eaUaY33WigYMXO9y7JtCQU";

char *vigenere_decrypt(char *ciphertext) {
	int j = 0;
	int len = strlen(ciphertext);
	printf("%d\n", len);
	char plaintext[len];
	for (int i = 0; i < len; i++) {
		char ch = ciphertext[i];
		if ((ch - 32) <= 0x5E) {
			plaintext[i] = (ch - table[j] + 95) % 95 + 32;
			j = (j + 1) % 16;
		} else {
			plaintext[i] = ch;
		}
	}
	plaintext[len] = '\x00';
	return plaintext;
}

int main() {
	char *ciphertext1 = "dV.";
	char *plaintext1 = vigenere_decrypt(ciphertext1);
	printf("%s\n", plaintext1); // url
	char *ciphertext2 = "BQ1$*[w6G_";
	char *plaintext2 = vigenere_decrypt(ciphertext2);
	printf("%s\n", plaintext2); // SmokeyBear
	return 0;
}

