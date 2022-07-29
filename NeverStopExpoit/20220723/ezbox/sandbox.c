#include <unistd.h>
#include <stdio.h>
#include <sys/prctl.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <stdint.h>
#include <string.h>

#define CHECK_PROT(prot) prot & PROT_WRITE

unsigned char flag[0x30];

char logo[] = ""
"        _            _                   _             _            _               _     _      _      \n"
"       / /\\         / /\\                /\\ \\     _    /\\ \\         / /\\            /\\ \\ /_/\\    /\\ \\    \n"
"      / /  \\       / /  \\              /  \\ \\   /\\_\\ /  \\ \\____   / /  \\          /  \\ \\\\ \\ \\   \\ \\_\\   \n"
"     / / /\\ \\__   / / /\\ \\            / /\\ \\ \\_/ / // /\\ \\_____\\ / / /\\ \\        / /\\ \\ \\\\ \\ \\__/ / /   \n"
"    / / /\\ \\___\\ / / /\\ \\ \\          / / /\\ \\___/ // / /\\/___  // / /\\ \\ \\      / / /\\ \\ \\\\ \\__ \\/_/    \n"
"    \\ \\ \\ \\/___// / /  \\ \\ \\        / / /  \\/____// / /   / / // / /\\ \\_\\ \\    / / /  \\ \\_\\\\/_/\\__/\\    \n"
"     \\ \\ \\     / / /___/ /\\ \\      / / /    / / // / /   / / // / /\\ \\ \\___\\  / / /   / / / _/\\/__\\ \\   \n"
" _    \\ \\ \\   / / /_____/ /\\ \\    / / /    / / // / /   / / // / /  \\ \\ \\__/ / / /   / / / / _/_/\\ \\ \\  \n"
"/_/\\__/ / /  / /_________/\\ \\ \\  / / /    / / / \\ \\ \\__/ / // / /____\\_\\ \\  / / /___/ / / / / /   \\ \\ \\ \n"
"\\ \\/___/ /  / / /_       __\\ \\_\\/ / /    / / /   \\ \\___\\/ // / /__________\\/ / /____\\/ / / / /    /_/ / \n"
" \\_____\\/   \\_\\___\\     /____/_/\\/_/     \\/_/     \\/_____/ \\/_____________/\\/_________/  \\/_/     \\_\\/  \n"
"\t\t\t\t\t\t\t\t\tAuther: 0xb3a1e\n"
"";

void banner() {
    setvbuf(stdin, 0LL, 2, 0LL);
    setvbuf(stdout, 0LL, 2, 0LL);
    setvbuf(stderr, 0LL, 2, 0LL);
    puts(logo);
}

int read_str(int fd, unsigned char *buf, char delim, unsigned int sz) {
    int i, rv, cnt = 0;
    void *ptr = buf;

    for (i = 0; i < sz; i++) {
        rv = read(fd, ptr, 1);
        if (rv != 1) {
            //perror("read");
            return EOF;
        } else if (*(unsigned char *)ptr == delim) {
            *(unsigned char *)ptr = '\0';
            return cnt;
        } else {
            ptr++;
            cnt++;
        }
    }

    return cnt;
}

int read_line(int fd, unsigned char *buf, unsigned int sz) {
    return read_str(fd, buf, '\n', sz);
}

void backdoor() {
    int fd, rv;

    fd = open("flag.txt", 0);
    rv = read_line(fd, (unsigned char *)flag, 0x30);
    flag[rv] = '\0';
    printf("gift: %p\n", flag);
}

int get_prot(uint64_t *addr) {
    int fd, rv, prot = -1;
    char vmmap[1000];
    char *target, *ptr, *pch;

    ptr = malloc(0x10);
    sprintf(ptr, "%p-", addr);
    target = ptr + 2;
    //printf("target => %s\n", target);

    fd = open("/proc/self/maps", 0);
    while ((rv = read_line(fd, vmmap, 1000)) != EOF) {
        //printf("vmmap => %s\n", vmmap);
        if (strstr(vmmap, target)) {
            prot = PROT_NONE;
            //printf("vmmap => %s\n", vmmap);
            pch = strtok(vmmap, " ");
            //printf("%s\n", pch);
            pch = strtok(NULL, " ");
            //printf("%s\n", pch);
            if (*(pch + 0) == 'r') {
                prot = prot | PROT_READ;
            }
            if (*(pch + 1) == 'w') {
                prot = prot | PROT_WRITE;
            }
            if (*(pch + 2) == 'x') {
                prot = prot | PROT_EXEC;
            }
            break;
        }
    }

    return prot;
}

void sandbox(void (*sh)(void)) {
    int i, prot, status;
    pid_t pid;

    /*
    prot = get_prot((uint64_t *)sh);
    //printf("prot = %d\n", prot);
    if (prot == -1) {
        perror("get_prot");
        abort();
    }
    */
    pid = fork();
    if (pid < 0) {
        perror("fork");
        abort();
    }
    if (pid == 0) {
        for (i = 0; i < 1024; i++) {
            close(i);
        }
        prctl(PR_SET_DUMPABLE, 0, 0, 0, 0);
        prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
        if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT, 0, 0, 0)) {
            perror("seccomp");
            abort();
        }
        sh();
        abort();
    }
    waitpid(pid, &status, 0);
    if (!WIFEXITED(status) || WEXITSTATUS(status)) {
        //perror("waitpid");
        abort();
    }
    /*
    if (CHECK_PROT(prot)) {
        perror("check");
        abort();
    }
    */
}

int main() {
    int page_size, rv, status, i;
    void (*sh)(void);

    banner();
    backdoor();

    page_size = sysconf(_SC_PAGESIZE);
    sh = mmap(0, page_size, PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, 0, 0);
    printf("pls input your shellcode: ");
    fflush(stdout);
    rv = read_str(0, (unsigned char *)sh, '\0', 0x500);
    mprotect(sh, page_size, PROT_EXEC | PROT_READ);

    sandbox(sh);
    puts("OVER!");

    return 0;
}

