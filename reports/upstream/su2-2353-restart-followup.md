I have a bounded restart/history observation that may help separate the time contracts here, without changing the zero-based file labels.

On pinned v8.5.0 (`12eb826f049ef7f67df974dfcb44cf36ee07c0f8`), I used a static 4³-cell incompressible uniform transient MMS, u=(1+t²,0,0), p=0, forcing=(2t,0,0), BDF2, dt=0.1, with verification Dirichlet conditions on all six faces. Restart at iteration 2 imports both saved states 0 and 1, as described above.

Comparing saved indices 2 and 3 against an uninterrupted four-step run:

- Pressure and all velocity components agree within 1.964e-15 (predeclared tolerance 1e-7).
- All saved inner residuals satisfy the predeclared log10 threshold -10.
- At Time_Iter 2 and 3, continuous history reports Cur_Time 0.2 and 0.3, while restarted history reports 0.1 and 0.2.

The same history difference occurs with our diagnostic global PhysicalTime shift, although that intervention changes the MMS boundary values from old-time to target-time values. This is not validation of that intervention as a general fix.

In the pinned source, HistoryOutputField initializes its value to zero, and COutput::LoadCommonHistoryData adds one TIME_STEP whenever TIME_ITER changes. It does not read driver PhysicalTime in that update. A fresh-zero fixed-step accumulator reproduces all 12 observed history rows exactly. This supports treating the output clock separately from the source/boundary clock; it does not show that the physical solve restarted at the wrong time.

[Report, raw archives and reproduction commands](https://github.com/Unjuno/concentration-aware-ns/blob/4e1ff6e/reports/su2-restart-time-pilot.md). The raw-data checker deliberately returns failure for history-time continuity while recording passing field comparison.

I have not tested a fresh master binary, moving meshes, variable time steps or discrete adjoints, and I saw the compatibility concerns on #2857. A focused output-time initialization regression may be useful independently of the broader implicit target-time change. No renumbering of restart files is proposed here.
