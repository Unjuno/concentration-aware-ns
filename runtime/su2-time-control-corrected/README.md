# Diagnostic intervention, not a proposed general fix

This image changes only the single-zone driver's MMS time to (TimeIter+1)*dt.
It tests the source-time hypothesis in first-order, constant-dt, non-restart
runs. It is not reviewed for other time schemes, moving grids, restarts,
multizone coupling or other consumers of PhysicalTime. Upstream source retains
LGPL-2.1-or-later. The production concentration image remains unchanged.
