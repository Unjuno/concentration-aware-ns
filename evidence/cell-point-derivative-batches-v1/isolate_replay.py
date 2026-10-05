import json,os,runpy,sys
from pathlib import Path
expected=Path(__file__).resolve().parent/'source'
assert Path.cwd().resolve()==expected and not (expected/'.git').exists()
sys.path.insert(0,str(expected))
blocked=[]
def audit(event,args):
    if event.startswith('subprocess.') or event.startswith('socket.') or event in ('os.system','os.exec','os.spawn','os.posix_spawn','os.fork'):
        blocked.append(event);raise RuntimeError('process/network access is blocked in this archive replay')
    if event=='open' and isinstance(args[0],(str,bytes)):
        path=os.fsdecode(args[0])
        if '/.git/' in path or path.endswith('/.git'):
            blocked.append('open-git');raise RuntimeError('Git object access is blocked in this archive replay')
sys.addaudithook(audit)
sys.argv=['tools.audit_cell_point_capture_derivative',*sys.argv[1:]]
runpy.run_module('tools.audit_cell_point_capture_derivative',run_name='__main__')
origins={name:str(Path(module.__file__).resolve().relative_to(expected))
         for name,module in sys.modules.items() if name.startswith('tools.') and hasattr(module,'__file__')}
assert origins and not blocked
(Path(__file__).resolve().parent/'isolation.json').write_text(json.dumps({'status':'PASS_GIT_DIRECTORY_FREE_EXPORT_WITH_PROCESS_NETWORK_AND_GIT_OPEN_GUARDS','actual_cwd':str(expected),'tools_module_origins':origins,'blocked_attempts':blocked,'scope':'Raw archives are external SHA-verified data; required source/input files are included in the frozen selected export. The exported analysis completed without Python process/network/Git-object opens; dependencies are the locked same-host verification environment.'},indent=2)+'\n')
