# Superseded runner attempt

The Lean process completed successfully and printed all five expected axiom
reports. The first version of the host-side audit script rejected the output
because Lean wrapped one axiom list across multiple lines. This was a parser
failure, not a Lean compile failure. The preserved raw output is `lean.log`.

The script now normalizes whitespace and checks declaration order, the exact
permitted axiom list, and absence of `sorryAx`. The successful rerun and hashed
manifest are in the sibling `cusp-ball-germ-v2` directory.
