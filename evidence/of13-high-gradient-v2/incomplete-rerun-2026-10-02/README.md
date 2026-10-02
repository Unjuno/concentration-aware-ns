# Incomplete OpenFOAM n=64 time-step rerun

This 2026-10-02 JST run requested 100 steps (`dt=0.0005`, `endTime=0.05`) and recorded 36 converged steps through `t=0.018`. The log then contains a `t=0.0185` time label but no converged step. The host runner was stopped after output stopped and no host solver process was observable. At that time the Docker client and API/control requests were blocked, so container removal/liveness could not be authoritatively verified. No successful solver exit or endpoint archive exists. A later process check on 2026-10-03 found neither the recorded host runner PID nor Docker client PID, but this does not establish the earlier container state.

Inputs, their original digest list, invocation (workstation path sanitized), and both raw logs are retained here. `status.json` records the observation time and log hashes. Its observation timestamp is 2026-10-01 22:19 UTC, which is 2026-10-02 JST. The partial attempt is excluded from the completed six-case matrix, standard/local gate results, and all physical or solver-defect conclusions. It is not a validated reproduction of a numerical defect.

This was a later repeat of `n64-dt0.0005`, a row that had already completed
100/100 steps and passed both gates in the September 30 temporal addendum. The
completed archive remains the authoritative matrix row; this incomplete repeat
does not supersede it. Its archive hash and index path are recorded in
`status.json`.
