# Arb nominal-mean H1 certificate evidence

Source: `4222bd312c7f70768261c9087b2303dae5a7733a`, python-flint 0.9.0,
96-bit precision, four archived final states.

- `analysis.json`: full rational lower/upper endpoints and scoped comparisons.
- `audit.log`, `full-suite.log`: executed certificates and 295-test local suite.
- `validation.json`: commands, identities, environment, export hash and limits.
- `isolate_replay.py`, `isolation.json`, `clean-export-replay.log`: accepted
  selected-export replay, with strict complete analysis JSON byte identity.
- `check_scalar_chain.py`, `scalar-chain-check.json`: independently checks the
  rational scalar chain using only Python's standard library; not a proof of
  the Fourier calculation or source interpretation.
- `initial-test-failure-note.md`: development failure excluded from acceptance.

Download the four raw archive assets from the existing
[release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-amr-mean-quality-v1-3566f89),
create a case-ID-to-archive-path JSON map, install the locked requirements and run:

```bash
python -m tools.audit_amr_arb_mean_certificate --raw-map /path/map.json --output /new/output/path --source-commit 4222bd312c7f70768261c9087b2303dae5a7733a
python evidence/amr-arb-mean-certificate-v1/check_scalar_chain.py evidence/amr-arb-mean-certificate-v1/analysis.json
```

For the scoped export, archive all paths in `validation.json`, extract under
`source/`, put the guard wrapper beside it and execute from that directory with
absolute accessible raw-map paths. No `.git` is needed during numerical replay.
The output directory must be new. Nominal binary64 means and canonical dyadic
geometry are explicit conditions; the original solver gate remains unchanged.
See [report](../../reports/openfoam-amr-arb-mean-certificate-2026-10-04.md).
