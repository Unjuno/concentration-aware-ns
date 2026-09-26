"""Exact fixed-step model of the inspected history accumulator, checked on raw logs."""
from fractions import Fraction
import argparse,csv,io,json,tarfile
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--protocol',default='protocols/su2-restart-time-pilot-v1.json');args=parser.parse_args()
protocol=Path(args.protocol);p=json.loads(protocol.read_text());root=Path('evidence')/protocol.stem;rows=[]
for variant in ['original','shifted']:
 for mode in ['continuous','resumed']:
  with tarfile.open(root/f'{variant}-{mode}.tar.gz') as tar:
   name='history.csv' if mode=='continuous' else f"history_{p['restart_iter']:05d}.csv"
   history=list(csv.DictReader(io.StringIO(tar.extractfile(name).read().decode())))
   previous=0;clock=Fraction(0)
   for raw in history:
    row={k.strip().strip('"'):v.strip() for k,v in raw.items()}
    iteration=int(row['Time_Iter']);dt=Fraction(row['Time_Step'])
    if iteration!=previous:clock+=dt
    previous=iteration
    assert clock==Fraction(row['Cur_Time'])
    rows.append({'variant':variant,'mode':mode,'iteration':iteration,'accumulator_time':str(clock),'index_time':str(iteration*dt),'offset':str(clock-iteration*dt)})
result={'success':True,'scope':'Exact arithmetic model reproduces all archived history times. Assumes fresh zero-valued history fields and fixed dt; not a dynamic-step or full output lifecycle proof.','rows':rows}
(root/'output-clock-model.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'success':True,'rows_checked':len(rows)}))
