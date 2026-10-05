# Validation at the AMR derivative source commit

Hosted Python CI passed 264 tests, one skip and 70 subtests at `5bc0691a60d2282aef6828f5da6d5f2a803673e9`. The changed-input gate passed and skipped the scalar package operator job because the change does not alter its numerical inputs. `hosted-ci.json` retains both run URLs and conclusions.

The CPython 3.14 fixed-commit export separately passed 47 replay steps, six follow-up checks and comparison of 237 unchanged files. The CPython 3.12 strict metadata-identity failure is preserved separately. The new AMR decomposition reproduces exactly in both environments.

A supplemental package archive replay used the fresh exported Python code and raw archive plus the immutable input-source Git blobs from the local clone. It passed archive/input/payload verification and the specified operator gate; this is not a standalone Git-free export or another CFD run. `package-supplement.json` names the two different commits and records the comparison with the prior macOS replay. No scientific verdict is broadened.
