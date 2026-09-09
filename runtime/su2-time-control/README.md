# Uniform MMS control for source time

Build the parent image using runtime/su2/Dockerfile, then:

```
docker build -t concentration-aware-ns:su2-time-control runtime/su2-time-control
python3 -m tools.run_su2_time_control
docker build -t concentration-aware-ns:su2-time-control-corrected runtime/su2-time-control-corrected
python3 -m tools.run_su2_time_control --corrected
```

Run from the project root with NumPy installed. Scripts refuse existing case roots.
The helper replaces only the manufactured solution, using spatially uniform
u=(1+t^2,0,0), pressure=0 and momentum forcing (2t,0,0). The baseline leaves all
upstream driver, time integration and source assembly untouched. The corrected
variant is a diagnostic intervention, not a general patch recommendation.
Inputs, outputs, histories, exit codes, commands and image IDs are archived in
evidence/su2-time-control-v1 and evidence/su2-time-control-v1-corrected.
Upstream-derived code remains LGPL-2.1-or-later; helper.cpp is original MIT code.
