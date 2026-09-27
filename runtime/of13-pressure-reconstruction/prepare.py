"""Generate an observation-only library copy from the pinned GPL upstream source."""
import hashlib,json,shutil,sys
from pathlib import Path
source,target=map(Path,sys.argv[1:])
expected='1e6b6d38e1f2730368b5de45a4fc76017b06284748349149da41c90c6d84efb2'
assert hashlib.sha256((source/'correctPressure.C').read_bytes()).hexdigest()==expected
assert not target.exists()
shutil.copytree(source,target)
p=target/'correctPressure.C';s=p.read_text();s=s.replace('#include "incompressibleFluid.H"','#include "incompressibleFluid.H"\n#include <type_traits>')
needle='    volScalarField& p(p_);';assert s.count(needle)==1
s=s.replace(needle,'''    // Diagnostic snapshots are unregistered and never used in the solver update.
    const bool cansWrite = mesh.time().writeTime();
    const auto cansSnapshot = [&](const word& name, const auto& field)
    {
        if (cansWrite)
        {
            typename std::decay<decltype(field)>::type snapshot
            (
                IOobject(name, mesh.time().name(), mesh,
                         IOobject::NO_READ, IOobject::NO_WRITE, false),
                field
            );
            snapshot.write();
        }
    };
'''+needle)
needle='    p.relax();';assert s.count(needle)==1
s=s.replace(needle,'''    cansSnapshot("cansPressureBeforeRelax", p);
    cansSnapshot("cansPhiHbyA", phiHbyA);
    cansSnapshot("cansPhiCorrected", phi);
'''+needle+'''
    cansSnapshot("cansPressureAfterRelax", p);
    cansSnapshot("cansHbyA", HbyA);
    cansSnapshot("cansRAU", rAU);
    cansSnapshot("cansRAtU", rAtU());
    if (cansWrite)
    {
        const volVectorField cansGradient(fvc::grad(p));
        const volVectorField cansCorrection(rAtU()*cansGradient);
        cansSnapshot("cansGradP", cansGradient);
        cansSnapshot("cansPressureCorrection", cansCorrection);
        Info<< "CANS_PRESSURE_RECONSTRUCTION time=" << mesh.time().name()
            << " consistent=" << pimple.consistent() << endl;
    }
''')
needle='    U = HbyA - rAtU*fvc::grad(p);';assert s.count(needle)==1
s=s.replace(needle,needle+'\n    cansSnapshot("cansUBeforeConstraints", U);')
needle='    fvConstraints().constrain(U);';assert s.count(needle)==1
s=s.replace(needle,needle+'\n    cansSnapshot("cansUAfterConstraints", U);')
p.write_text(s)
p=target/'Make/files';s=p.read_text();assert '$(FOAM_LIBBIN)' in s;p.write_text(s.replace('$(FOAM_LIBBIN)','/diag/lib'))
(target/'instrumentation.json').write_text(json.dumps({'original_correctPressure_sha256':expected,'modified_correctPressure_sha256':hashlib.sha256((target/'correctPressure.C').read_bytes()).hexdigest(),'scope':'Write-time snapshots; successive corrections overwrite same names, retaining final call only. No trajectory attribution.'},indent=2)+'\n')
