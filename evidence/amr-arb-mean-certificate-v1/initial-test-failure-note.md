# Initial test failure (tool-output observation)

Before the numerical freeze, the known-shear test returned False because the
squared zero-centred complex Fourier ball produced `nan` on the generic
exponentiation path. The norm accumulation was changed to explicit real/imaginary
products; all three targeted tests and the full suite then passed. No actual
archive certificate was accepted from the failed prototype. This note records
the observed development failure; it is not a reproduced upstream bug claim.
