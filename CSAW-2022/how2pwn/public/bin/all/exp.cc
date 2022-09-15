#include <linux/seccomp.h>
#include <unistd.h>
#include <cstdlib>
#include <linux/filter.h>
#include <linux/audit.h>
#include <sys/ptrace.h>
#include <cstddef>
#include <cerrno>
#include <sys/syscall.h>
#include <poll.h>
#include <sys/ioctl.h>
#include <sys/prctl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <err.h>

static int seccomp(unsigned int op, unsigned int flags, void *args)
{
  errno = 0;
  return syscall(__NR_seccomp, op, flags, args);
}

int install_notify() {
  struct sock_filter filter[] = {
    BPF_STMT(BPF_LD+BPF_W+BPF_ABS, offsetof(struct seccomp_data, arch)),
    BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, AUDIT_ARCH_X86_64, 1, 0),
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_USER_NOTIF),
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW),
  };
  struct sock_fprog fprog;
  fprog.filter = filter;
  fprog.len = 4;
  int fd = seccomp(SECCOMP_SET_MODE_FILTER,  SECCOMP_FILTER_FLAG_NEW_LISTENER, &fprog);
  if (fd < 0) {
    err(EXIT_FAILURE, "Could not install notify");
  }
  return fd;
}

void handle_notify(int fd) {
  for (;;) {
    struct seccomp_notif req = {};
    struct seccomp_notif_resp resp = {};
    if (ioctl(fd, SECCOMP_IOCTL_NOTIF_RECV, &req) != 0)
      continue;
    resp.id = req.id;
    resp.error = 0;
    resp.val = 0;
    resp.flags = SECCOMP_USER_NOTIF_FLAG_CONTINUE;
    ioctl(fd, SECCOMP_IOCTL_NOTIF_SEND, &resp);
  }
}

int main() {
  int fd = install_notify();
  pid_t p = fork();
  if (p == 0) {
    handle_notify(fd);
  }
}
