# PhysicsNeMo CPU residual audit

Source: NVIDIA/physicsnemo commit 1b961314e42a0625502ba1592d25f706f1e02a24
(v2.2.1), Apache-2.0. Codeload tar archive SHA256:
`f987c380db2d55caf8af494927a84d9a5c19ef67e2c462ea7aaeccedf2688bec`.

The audited source is unpacked under work/physicsnemo-source, without creating
another Git repository. Scripts import that unmodified source directly. This is
a minimal CPU audit environment for the imported modules, not a complete install
of every PhysicsNeMo optional feature. Tested with macOS arm64 Python 3.14.5.

Create work/physicsnemo-env using python3 -m venv, then install the frozen packages:

```
work/physicsnemo-env/bin/python -m pip install -r runtime/physicsnemo/requirements-cpu-audit.txt
work/physicsnemo-env/bin/python -m tools.check_reference_torch
work/physicsnemo-env/bin/python -m tools.check_physicsnemo_residual
```

Obtain the source from
https://codeload.github.com/NVIDIA/physicsnemo/tar.gz/1b961314e42a0625502ba1592d25f706f1e02a24
and verify its SHA256 before unpacking (remove the outer archive directory).
Package versions are frozen; this is not a hash-locked wheel environment.

The exact-reference test uses float64 CPU tensors, native PhysicsInformer spatial
autodiff and explicitly supplied u__t/v__t/w__t. Time derivatives are a caller
responsibility in this API. A passing residual test does not demonstrate neural
training, approximation accuracy, convergence or a reproduced project defect.
