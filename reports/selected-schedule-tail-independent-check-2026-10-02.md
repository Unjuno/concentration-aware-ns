# Selected-schedule tail-pressure independent check

The extension `verification/SelectedScheduleTailPressure.lean` was compiled
with the pinned Lean environment and independently exported to nanoda. The
checker processed 64,191 declarations with zero typechecker errors. It found
all five selected declarations covering the relative tail coefficient, the
conditional pressure-tail lower bound, and existential rate-capped prepared
and full `ProfileData` constructions. The export and checker outputs are
identified by hashes in
`evidence/lean-verification/selected-schedule-tail-nanoda-2026-10-02.json`.

The checker reported one pretty-printer error: `Unable to print axioms`. This
is a reporting limitation, not a typechecker error. The Lean source-side axiom
audit lists `propext`, `Classical.choice`, and `Quot.sound` for the extension's
declarations, with no `sorryAx`.

The rate cap yields a conditional lower bound of `-P^2/100` for the selected
tail under the stated exact wait identity and lambda cap. The constructed
rate-capped profile is existential. It is not shown equal to the pinned
`FinalSlowBase.actualProfile`, so it does not establish that actual profile's
root-pressure premise or a full pressure sign. Independent term checking also
does not establish the truth of upstream assumptions or connect this formal
construction to a physical fluid. It supports no molecular alignment,
viscosity-change, or phase-transition conclusion.

To reproduce, use the pinned local checker image and dependencies, then run:

```sh
sh runtime/lean-verification/check_selected_schedule_tail_pressure_nanoda.sh \
  work/selected-schedule-tail-nanoda-reproduction
```

The runner refuses to overwrite an existing output directory. Its summary and
logs are small tracked artifacts; the 641,951,857-byte NDJSON export remains
in local `work/` and is content-addressed in the summary.
