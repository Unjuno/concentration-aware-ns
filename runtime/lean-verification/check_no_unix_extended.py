"""Linux aarch64 launch controls, including inherited descriptors."""
import json
import socket
import subprocess
import sys

launcher = '/bincheck/no_unix'
a, b = socket.socketpair()
fd = a.fileno()
probe = f'import os; os.fstat({fd})'
baseline = subprocess.run([sys.executable, '-c', probe], pass_fds=(fd,), capture_output=True)
restricted = subprocess.run([launcher, sys.executable, '-c', probe], pass_fds=(fd,), capture_output=True)
stdio = subprocess.run([launcher, '/usr/bin/true'], stdin=a, capture_output=True)
creation = subprocess.run([launcher, sys.executable, '/src/check_no_unix.py'], capture_output=True, text=True, check=True)
results = {'inherited_fd_baseline_exit': baseline.returncode,
           'inherited_fd_restricted_exit': restricted.returncode,
           'inherited_fd_restricted_stderr': restricted.stderr.decode(),
           'socket_stdio_exit': stdio.returncode, 'socket_stdio_stderr': stdio.stderr.decode(),
           'child_socket_creation': json.loads(creation.stdout)}
assert baseline.returncode == 0
assert restricted.returncode != 0 and b'Bad file descriptor' in restricted.stderr
assert stdio.returncode != 0 and b'socket stdio rejected' in stdio.stderr
assert results['child_socket_creation'] == {'unix_socket': 'EPERM', 'unix_pair': 'EPERM', 'inet_socket': 'allowed'}
print(json.dumps({'passed': True, 'scope': 'Inherited socket descriptor closure, socket stdio rejection, and child syscall controls; not a complete sandbox audit.', 'results': results}, indent=2))
a.close(); b.close()
