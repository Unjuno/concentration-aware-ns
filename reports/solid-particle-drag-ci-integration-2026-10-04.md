# Conditional particle drag: hosted verification integration

A new Python verification step recomputes the source-linked branch audit and
compiles the preserved scalar C++ transcription with g++ at -O0 and -O2.
The checker verifies the declared adjacent inputs, finite output jump and
internal diagnostic consistency. Compiler identity, both JSON outputs, the
Arb/Python receipt and checker result are uploaded even when the job fails.
This is not native OpenFOAM cloud execution or binary equivalence.

Local branch recomputation passes its twenty exact controls, negative controls
and positive Arb enclosure. The new standard-library checker accepts a Python
fixture and rejects three corruptions: zero reported jump, wrong adjacent
input and nonfinite quotient. Those fixtures do not stand in for compiled C++.
The earlier Xcode compilation failure remains preserved.

Run 37157306920 at publication a611973 was freshly observed queued while this
integration was prepared. No replacement publication is pushed yet, to avoid
cancelling that exact-head verification. Hosted execution of the new stage is
pending; no new cross-host success is claimed. The full goal remains active.
