"""Execute the frozen four-cell plan with two isolated worker processes at a time.
Provider credentials must be supplied privately via environment variables.
"""
import concurrent.futures
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
EXPERIMENT=ROOT/'experiments/kimi-delegate-ctf'
sys.path.insert(0,str(EXPERIMENT))
from analyze_outcomes import write_report
from fixture_setup import write_json


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    plan=json.loads((OUT/'plan.json').read_text())
    pair=EXPERIMENT/plan['pair']
    resume = '--resume' in sys.argv
    if resume:
        from verify_run import verify_run
        state=json.loads((OUT/'batch-state.json').read_text())
        state['resumed_at']=now()
        state['resume_reason']='Report was attempted while another episode was finalizing; completed runs verified, not repeated.'
        for c in plan['cells']:
            run=OUT/c['id']
            if run.exists():
                manifest=json.loads((run/'manifest.json').read_text())
                if manifest['status'] != 'completed' or verify_run(run)['errors']:
                    raise RuntimeError(f'Unresolved run {run}; refuse automatic retry')
                state['cells'][c['id']].update(status='completed',exit_code=0,finished_at=manifest['finished_at'],reconciled=True)
            elif state['cells'][c['id']]['status'] != 'not_started':
                raise RuntimeError(f'Unresolved state for {run}; refuse automatic retry')
        from honeypot_fixture import validate_honeypot_pair
        validate_honeypot_pair(pair)
    else:
        if (OUT/'batch-state.json').exists():
            raise RuntimeError('Batch already exists; use --resume after reconciliation')
        state={'status':'preparing','started_at':now(),'cells':{c['id']:{'status':'not_started'} for c in plan['cells']}}
    write_json(OUT/'batch-state.json',state)
    for command in (() if resume else ('prepare','build')):
        with (OUT/(command+'.log')).open('w') as log:
            subprocess.run([sys.executable,str(EXPERIMENT/'honeypot_run.py'),command,'--pair',str(pair)],
                           cwd=EXPERIMENT,stdout=log,stderr=subprocess.STDOUT,check=True)
    commands={}
    for c in plan['cells']:
        commands[c['id']]=[sys.executable,str(EXPERIMENT/'honeypot_run.py'),'run',
            '--pair',str(pair),'--condition',c['condition'],'--delegate',c['delegate'],
            '--board',plan['board'],'--model',plan['model'],'--epochs',str(plan['epochs_per_cell']),
            '--token-limit',str(plan['token_limit']),'--attempt-timeout',str(plan['attempt_timeout']),
            '--time-limit',str(plan['time_limit']),'--out',str(OUT/c['id']),'--execute-model']
    write_json(OUT/'commands.json',commands)
    def run_cell(c):
        with (OUT/(c['id']+'.log')).open('w') as log:
            result=subprocess.run(commands[c['id']],cwd=EXPERIMENT,stdout=log,stderr=subprocess.STDOUT)
        return result.returncode
    # Complete the possible-task pair first, then the impossible-task pair.
    for group in (plan['cells'][:2],plan['cells'][2:]):
        cells=[c for c in group if state['cells'][c['id']]['status']=='not_started']
        if not cells:
            continue
        state['status']='running' 
        for c in cells:
            state['cells'][c['id']]={'status':'running','started_at':now()}
        write_json(OUT/'batch-state.json',state)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures={pool.submit(run_cell,c):c for c in cells}
            for future in concurrent.futures.as_completed(futures):
                c=futures[future];code=future.result()
                state['cells'][c['id']].update(status='completed' if code==0 else 'error',exit_code=code,finished_at=now())
                write_json(OUT/'batch-state.json',state)
                print(json.dumps({'cell':c['id'],'exit_code':code}),flush=True)
        write_report(OUT,OUT/'report')
    state.update(status='completed' if all(c['status']=='completed' for c in state['cells'].values()) else 'completed_with_errors',finished_at=now())
    write_json(OUT/'batch-state.json',state)
    write_report(OUT,OUT/'report')
    print(json.dumps({'status':state['status'],'report':str(OUT/'report/results.md')}),flush=True)


if __name__=='__main__':main()
