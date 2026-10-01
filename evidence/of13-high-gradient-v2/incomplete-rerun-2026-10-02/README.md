# Incomplete OpenFOAM n=64 time-step rerun

This 2026-10-02 JST run requested 100 steps (`dt=0.0005`, `endTime=0.05`) and recorded 36 converged steps through `t=0.018`. The log then contains a `t=0.0185` time label but no converged step. The runner was intentionally terminated after output stopped; the container and host solver process are now absent. Docker inspection returned `no such object`; no successful solver exit or endpoint archive exists.

Inputs, their original digest list, invocation (workstation path sanitized), and both raw logs are retained here. `status.json` records the observation time and log hashes. The partial attempt is excluded from the completed six-case matrix, standard/local gate results, and all physical or solver-defect conclusions. It is not a validated reproduction of a numerical defect.
