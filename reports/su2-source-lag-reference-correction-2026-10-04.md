# SU2 reference-family correction

The auxiliary localized forcing-lag audit mistakenly called
`tools.high_gradient_reference.fields` with N equal to mesh resolution n.
Executed SU2 study-v1 uses the periodic exponential-envelope MMS in
`tools.reference.fields`, with sigma and nu from each archived parameters.json.
Matching the prior receipt reproduced the reference-family mistake; it did
not validate relevance to the executed study. The v1 quantitative forcing-lag
receipt and its repeated refresh are withdrawn from that interpretation.

Source fe22cebb corrects the import and passes archived sigma/nu. All three
archive SHA256 checks pass. The additive v2 receipt reports RMS mismatches
0.005395962987827801, 0.0026966360757034904 and 0.001347981851394919 for dt
.001, .0005 and .00025. Successive orders are 1.0007196166161088 and
1.0003597630504861. These are 4096 seeded point diagnostics, not continuous
extrema or a decomposition of solver endpoint error. The old RMS numbers
were about 70 times smaller and must not be reused for this study.

Two regression tests verify that continuum forcing is independent of archive
mesh resolution n and depends on archive sigma. Both pass locally. No raw
solver archive, original acceptance threshold, velocity diagnostic or native
run is changed. The original field family still has the same exponential
time identity; that generic identity alone did not establish source matching.

Original v1 JSON remains preserved; v2 is
`evidence/tests/su2-localized-source-lag-v2.json`. Existing report annotations
and the completion audit carry this correction. The queued preceding CI state
is saved separately; it does not validate this correction or the new particle
checks. Publication is necessary to correct the exposed audit source, even
though it may cancel the old queued job. Full goal remains active.
