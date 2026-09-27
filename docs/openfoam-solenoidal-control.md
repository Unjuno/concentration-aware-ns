# Minimal initial-field control for startup pressure

The next diagnostic changes only the initial cell velocity to eliminate the
centered discrete divergence whose pressure response was observed. It uses
an orthogonal projection for that specific operator, rather than the
nearest-neighbor Laplacian of the earlier pressure model.

For each Fourier mode, let q_j=sin(theta_j)/dx. For q!=0 set
Uhat_control=Uhat-q*(q dot Uhat)/|q|². When q=0, retain the entire mode.
This projects onto q dot Uhat=0 and minimizes the uniform-grid L2 change.
The zero/Nyquist symbols are set exactly to zero, preserving all eight
zero-symbol modes. This does not remove checkerboard null modes or certify
any general collocated-grid stability property.

For the recorded 64³ initial field, the relative change is 0.00263240376.
Real-space centered divergence drops from 0.0567238663 to 9.16e-15. The
normalized inner product of the correction and retained field is 5.20e-14.
Writing and rereading 17-digit ASCII U preserves the resulting array exactly.
The original boundary dictionaries are retained. Inputs and output hashes
are in `evidence/tests/openfoam-solenoidal-initial-control.json`.

Reproduce input preparation with:

```sh
python3 -m tools.prepare_openfoam_solenoidal_control
```

The generator refuses an existing work output directory. The initial control
field is archived in `evidence/of13-solenoidal-initial-control-v1.tar.gz`.
The frozen subsequent solver specification is
`protocols/of13-solenoidal-startup-control-v1.json`; no solver run for this
control has occurred. Docker's existing request remains pending.

The unchanged continuum forcing and changed initial velocity define a
different initial value problem. Its error against the original reference
must not become a new benchmark acceptance score. Compare its startup
pressure impulse and increment from its own initial field to the original
case. Even a successful removal of the initial impulse would not by itself
explain the later time-convergence order.

All three intervention cases are now prepared under
`work/of13-solenoidal-startup-control-v1`. Reproduce preparation with
`python3 -m tools.prepare_openfoam_solenoidal_cases` after restoring the
baseline startup inputs. The script checks the archived projected-U hash,
rechecks divergence, and compares all copied solver inputs bytewise. Only
`0/U` differs, and even its boundary dictionary remains identical. No 0/phi
file is introduced. Parameters explicitly label the changed initial problem.

`evidence/tests/openfoam-solenoidal-case-preparation.json` records every input
hash, protocol identity and prepared-only status. These are input checks, not
solver results. No additional Docker request has been enqueued while the
existing baseline and docker-ps requests remain pending.
