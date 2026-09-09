/* Linux aarch64: deny new AF_UNIX sockets before executing a checker.
 * Not a complete sandbox; existing descriptors require separate control. */
#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <sys/socket.h>
#include <sys/syscall.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage: no_unix COMMAND [ARGS]\n"); return 2; }
  struct sock_filter code[] = {
    BPF_STMT(BPF_LD|BPF_W|BPF_ABS, offsetof(struct seccomp_data, arch)),
    BPF_JUMP(BPF_JMP|BPF_JEQ|BPF_K, AUDIT_ARCH_AARCH64, 1, 0),
    BPF_STMT(BPF_RET|BPF_K, SECCOMP_RET_KILL_PROCESS),
    BPF_STMT(BPF_LD|BPF_W|BPF_ABS, offsetof(struct seccomp_data, nr)),
    BPF_JUMP(BPF_JMP|BPF_JEQ|BPF_K, __NR_socket, 1, 0),
    BPF_JUMP(BPF_JMP|BPF_JEQ|BPF_K, __NR_socketpair, 0, 3),
    BPF_STMT(BPF_LD|BPF_W|BPF_ABS, offsetof(struct seccomp_data, args[0])),
    BPF_JUMP(BPF_JMP|BPF_JEQ|BPF_K, AF_UNIX, 0, 1),
    BPF_STMT(BPF_RET|BPF_K, SECCOMP_RET_ERRNO | EPERM),
    BPF_STMT(BPF_RET|BPF_K, SECCOMP_RET_ALLOW),
  };
  struct sock_fprog filter = { sizeof(code)/sizeof(code[0]), code };
  if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) ||
      prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &filter)) {
    perror("seccomp setup"); return 1;
  }
  execvp(argv[1], argv+1); perror("execvp"); return 1;
}
