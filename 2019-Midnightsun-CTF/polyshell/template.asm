; 2016 - ixty
; 2019 - STT
; multi-arch template
; works on:
;   x86
;   x86_64
;   arm
;   arm_64
;   mips

; compile with nasm
bits 32
_start:

; ======================================================================= ;
; init, polyglot shellcode for arm, arm64, x86, x86_64, mips
; branches out to specific arch dependent payloads
; ======================================================================= ;

; ARCH      DISASSEMBLY             - DESCRIPTION
; mips      beq     zero, a0, 0x14  - branch if 0==0, hardcoded offset because i'm lazy
; arm       andne   r0,  r4,  r4    - harmless
; arm64     adr     x4,  0x8000     - apparently fine?
; x86       add     al, 0x0         - simple adds
;           add     al, 0x10
; x86_64    add     al, 0x0         - simple adds
;           add     al, 0x10
    db 0x04, 0x00, 0x04, 0x10
; arm       andlo   r0, r0, #0xeb000
; arm64     orr     w11, w23, #7
; x86       jmp     $+0xa / junk
; x86_64    jmp     $+0xa / junk
    db 0xeb, (_x86 - $ - 2), 0x32, 0x32
; arm       b       _arm ($+0x10)
; arm64     ands    x1, x0, x0
    db ((_arm - $ - 8) / 4), 0x00, 0x00, 0xea
; arm64     b       _arm64 ($+0x14)
    db ((_arm64 - $) / 4), 0x00, 0x00, 0x14

; ======================================================================= ;
; MIPS PAYLOAD
; ======================================================================= ;

    times (4 - (($ - _start) % 4)) nop      ; must be 4b aligned
_mips:
    db {}

; ======================================================================= ;
; x86 only, detect 32/64 bits
; ======================================================================= ;
_x86:
; x86       xor eax, eax;
; x86_64    xor eax, eax;
    xor eax, eax
; x86       inc eax
; x86_64    REX + nop
    db 0x40
    nop
    jz _x86_64


; ======================================================================= ;
; OTHER PAYLOADs
; ======================================================================= ;
_x86_32:
    db {}

_x86_64:
    db {}

    times (4 - (($ - _start) % 4)) nop      ; must be 4b aligned
_arm:
    db {}

    times (4 - (($ - _start) % 4)) nop      ; must be 4b aligned
_arm64:
    db {}
