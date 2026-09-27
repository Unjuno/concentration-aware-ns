"""Copy installed foamRun and insert a constructor-only observation."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
source = Path(sys.argv[1])
target = Path(sys.argv[2])
target.mkdir(parents=True, exist_ok=False)
for name in ['foamRun.C', 'setDeltaT.C', 'setDeltaT.H']:
    shutil.copyfile(source/name, target/name)
shutil.copytree(source/'Make', target/'Make', ignore=shutil.ignore_patterns('linux*'))
p = target/'foamRun.C'
raw = p.read_bytes()
s = raw.decode().replace('#include "argList.H"', '#include "argList.H"\n#include "fvcDiv.H"\n#include "volFields.H"\n#include "surfaceFields.H"')
anchor = '    solver& solver = solverPtr();'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + '''
    const surfaceScalarField& initialPhi = mesh.lookupObject<surfaceScalarField>("phi");
    initialPhi.write();
    volScalarField initialDiv
    (
        IOobject("initialDiv", runTime.name(), mesh, IOobject::NO_READ, IOobject::AUTO_WRITE),
        fvc::div(initialPhi)
    );
    initialDiv.write();
    Info<< "STARTUP_PROBE_COMPLETE_NO_TIME_ADVANCE" << endl;
    return 0;
''')
p.write_text(s)
f=target/'Make/files'
f.write_text(f.read_text().replace('$(FOAM_APPBIN)/foamRun', '/probe/startupProbe'))
(target.parent/'source-identity.json').write_text(json.dumps({'original_foamRun_sha256':hashlib.sha256(raw).hexdigest(),'modified_foamRun_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2)+'\n')
