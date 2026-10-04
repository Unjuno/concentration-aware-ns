# amr-voxel-mean-reconstruction-v1

Numerical source: `6819ed429172ce37713ab16a9c17b10a3cc301a7`. `analysis.json` records all twelve archived
states. `audit.log` and `full-suite.log` preserve executed measurements and
source-specific local tests. The input archives remain in the previously
published [release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-amr-mean-quality-v1-3566f89),
with exact archive/member identities rechecked by the audit.

Create a JSON map of the four protocol case IDs to downloaded raw archive paths,
install the locked verification requirements, and execute from the source root:

```bash
python -m tools.audit_amr_voxel_mean_reconstruction --raw-map /path/map.json --output /new/output/path --source-commit 6819ed429172ce37713ab16a9c17b10a3cc301a7
```

The output directory must not exist. All Fourier/arithmetic results are scoped
analytical formulas in floating point, not outward-rounded certificates or an
original solver quality verdict. See [full report](../../reports/openfoam-amr-mean-constraint-gradient-2026-10-04.md).

`validation.json` binds the source, inputs, logs and accepted selected-export
replay. Both complete analysis JSON files reproduce byte-for-byte. The selected
export is from `5abbe08`; the earlier reconstruction source files are unchanged
from `6819ed4`, and their Git blob hashes are checked separately. Place
`isolate_replay.py` beside the exported `source/` directory and invoke it from
`source/` with the module name before its usual arguments. The external raw-map
JSON must use archive paths accessible from that directory. `isolation.json`
and `clean-export-replay.log` retain the accepted guard state and raw result.
