#define _GNU_SOURCE 1
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <malloc.h>
#include <errno.h>

#include <sys/prctl.h>
#ifndef PR_SET_NO_NEW_PRIVS
# define PR_SET_NO_NEW_PRIVS 38
#endif

#include <linux/unistd.h>
#include <linux/audit.h>
#include <linux/filter.h>
#ifdef HAVE_LINUX_SECCOMP_H
# include <linux/seccomp.h>
#endif
#ifndef SECCOMP_MODE_FILTER
# define SECCOMP_MODE_FILTER    2 /* uses user-supplied filter. */
# define SECCOMP_RET_KILL   0x00000000U /* kill the task immediately */
# define SECCOMP_RET_TRAP   0x00030000U /* disallow and force a SIGSYS */
# define SECCOMP_RET_ALLOW  0x7fff0000U /* allow */
struct seccomp_data {
    int nr;
    __u32 arch;
    __u64 instruction_pointer;
    __u64 args[6];
};
#endif
#ifndef SYS_SECCOMP
# define SYS_SECCOMP 1
#endif

#define syscall_nr (offsetof(struct seccomp_data, nr))
#define arch_nr (offsetof(struct seccomp_data, arch))

#if defined(__i386__)
# define REG_SYSCALL    REG_EAX
# define ARCH_NR    AUDIT_ARCH_I386
#elif defined(__x86_64__)
# define REG_SYSCALL    REG_RAX
# define ARCH_NR    AUDIT_ARCH_X86_64
#else
# warning "Platform does not support seccomp filter yet"
# define REG_SYSCALL    0
# define ARCH_NR    0
#endif

#define VALIDATE_ARCHITECTURE \
    BPF_STMT(BPF_LD+BPF_W+BPF_ABS, arch_nr), \
    BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, ARCH_NR, 1, 0), \
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_KILL)

#define EXAMINE_SYSCALL \
    BPF_STMT(BPF_LD+BPF_W+BPF_ABS, syscall_nr)

#define ALLOW_SYSCALL(name) \
    BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, __NR_##name, 0, 1), \
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW)

#define KILL_PROCESS \
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_KILL)

char banner[] = "\
  _______  __    _  ___      __   __  _______  __    _  _______ \n\
 |       ||  |  | ||   |    |  | |  ||       ||  |  | ||       |\n\
 |   _   ||   |_| ||   |    |  |_|  ||   _   ||   |_| ||    ___|\n\
 |  | |  ||       ||   |    |       ||  | |  ||       ||   |___ \n\
 |  |_|  ||  _    ||   |___ |_     _||  |_|  ||  _    ||    ___|\n\
 |       || | |   ||       |  |   |  |       || | |   ||   |___ \n\
 |_______||_|  |__||_______|  |___|  |_______||_|  |__||_______|\n\
";

char menu[] = "\
+-------------+\n\
|  1. add     |\n\
|  2. edit    |\n\
|  3. show    |\n\
|  4. delete  |\n\
|  5. exit    |\n\
+-------------+\n\
";

struct chunk {
    struct chunk * fd;
    struct chunk * bk;
    int64_t magic;
};

struct only {
    int64_t cnt;
    void * ptr[3];
    void (* add_func)();
    void (* edit_func)();
    void (* show_func)();
    void (* del_func)();
};

void add(void);
void edit(void);
void show(void);
void del(void);
void rev(void);

struct only * one;

int64_t global_magic = 0;

/* https://github.com/gebi/teach-seccomp/tree/master/step-2 */
int sandbox() {
    struct sock_filter filter[] = {
        /* Validate architecture. */
        VALIDATE_ARCHITECTURE,
        /* Grab the system call number. */
        EXAMINE_SYSCALL,
        ALLOW_SYSCALL(open),
        ALLOW_SYSCALL(read),
        ALLOW_SYSCALL(write),
        ALLOW_SYSCALL(exit),
        ALLOW_SYSCALL(exit_group),
        ALLOW_SYSCALL(mprotect),
        KILL_PROCESS,
    };
    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
        perror("prctl(NO_NEW_PRIVS)");
        goto failed;
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)) {
        perror("prctl(SECCOMP)");
        goto failed;
    }
    return 0;

failed:
    if (errno == EINVAL)
        fprintf(stderr, "SECCOMP_FILTER is not available. :(\n");
    return 1;
}

void get_magic() {
    FILE * fd = fopen("/dev/urandom", "rb");
    if (fd == NULL) {
        perror("fopen");
        exit(-1);
    }
    size_t count;
    do {
        count = fread(&global_magic, sizeof(global_magic), 1, fd);
    } while(count != 1);
    fclose(fd);
}

void init() {
    setvbuf(stdin, 0LL, 2, 0LL);
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stderr, 0LL, 2, 0LL);
    alarm(0x3c);
    one = calloc(sizeof(struct only), 1);
    if (one == NULL) {
        perror("calloc");
        exit(-1);
    }
    get_magic();
    one->cnt = 0;
    one->ptr[0] = NULL;
    one->ptr[1] = NULL;
    one->ptr[2] = NULL;
    one->add_func = add;
    one->edit_func = edit;
    one->show_func = show;
    one->del_func = del;
    puts(banner);
    if (sandbox()) {
        perror("sandbox");
        exit(-1);
    }
}

int64_t read_int() {
    char buf[10];
    int n = read(0, buf, 10);
    return atol(buf);
}

void read_str(char * str, int len) {
    int n = read(0, str, len);
}

void write_str(char * str, int len) {
    int n = write(1, str, len);
    n = write(1, "\n", 1);
}

void add() {
    if (one->cnt >= 3 || one->cnt < 0) {
        puts("[ERROR] access denied.");
        exit(-1);
    }
    void * buf = calloc(0x1f8, 1);
    if (buf == NULL) {
        perror("calloc");
        exit(-1);
    }
    printf("(pls input your message) >> ");
    read_str(buf + 0x18, 0x1f8 - 0x18);
    ((struct chunk *)buf)->magic = global_magic;
    int yes = 0;
    for (int i = 0; i < 3; i++) {
        void * temp_ptr = one->ptr[i];
        if (temp_ptr == NULL || ((struct chunk *)temp_ptr)->magic != global_magic) {
            one->ptr[i] = buf;
            yes = 1;
            break;
        }
    }
    if (yes == 0) {
        puts("[ERROR] access denied...");
        exit(-1);
    }
    one->cnt++;
}

void edit() {
    printf("(pls input the index of message) >> ");
    int idx = read_int();
    if (idx != 0 && idx != 1 && idx != 2) {
        puts("[ERROR] access denied.");
        exit(-1);
    }
    printf("(pls input your message) >> ");
    read_str(one->ptr[idx], 0x1f8);
}

void show() {
    printf("(pls input the index of message) >> ");
    int idx = read_int();
    if (idx != 0 && idx != 1 && idx != 2) {
        puts("[ERROR] access denied.");
        exit(-1);
    }
    printf("(here is your message) >> ");
    write_str(one->ptr[idx], 0x1f8);
}

void del() {
    if (one->cnt <= 0) {
        puts("[ERROR] you should add first.");
        exit(-1);
    }
    printf("(pls input the index of message) >> ");
    int idx = read_int();
    if (idx != 0 && idx != 1 && idx != 2) {
        puts("[ERROR] access denied.");
        exit(-1);
    }
    ((struct chunk *)one->ptr[idx])->magic = 0;
    free(one->ptr[idx]);
    //one->ptr[idx] = NULL;
    one->cnt--;
}

int main() {
    init();
    __asm__ __volatile__ (
        ".intel_syntax noprefix\n\t"
        "jz great\n\t"
        "jnz great\n\t"
        ".byte 0xE8\n\t"
        "great:\n\t"
    );
    int c;
    while (1) {
        puts(menu);
        printf("(your choice) >> ");
        c = read_int();
        if (c == 0) {
            puts("[ERROR] access denied.");
            exit(-1);
        }
        switch(c) {
        case 1:
            one->add_func();
            break;
        case 2:
            one->edit_func();
            break;
        case 3:
            one->show_func();
            break;
        case 4:
            one->del_func();
            break;
        case 5:
            exit(0);
            break;
        default:
            exit(-1);
        }
    }
}
