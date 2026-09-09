"""Run in the Linux container, both directly and through no_unix."""
import errno
import json
import socket
import subprocess
import sys

if '--child' in sys.argv:
    results = {}
    for name, create in [('unix_socket', lambda: socket.socket(socket.AF_UNIX)),
                         ('unix_pair', socket.socketpair),
                         ('inet_socket', lambda: socket.socket(socket.AF_INET))]:
        try:
            obj = create()
            for sock in obj if isinstance(obj, tuple) else (obj,):
                sock.close()
            results[name] = 'allowed'
        except OSError as exc:
            results[name] = 'EPERM' if exc.errno == errno.EPERM else str(exc)
    print(json.dumps(results))
else:
    child = subprocess.run([sys.executable, __file__, '--child'], capture_output=True, text=True, check=True)
    print(child.stdout, end='')
