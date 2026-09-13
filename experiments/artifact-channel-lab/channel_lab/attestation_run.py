"""Native focal-worker evaluation. A completed harness is not an efficacy result."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from .cli import ROOT, init
from .native_run import ctf_export

def run_attestation(out,model,condition='possible',board='rogue',delegate=False,seed=1729,
                    max_steps=20,worker_token_limit=60000,time_limit=300,max_output_tokens=2048,
                    advisor_model=None,max_advisor_calls=4,advisor_output_tokens=1024,scripted=False):
    from inspect_ai import eval
    from inspect_ai.log import resolve_sample_attachments
    from control_tower.inspect_tasks import control_eval
    init(); os.environ.setdefault('CONTROL_TOWER_MODEL_RATES',str(ROOT/'rates.json'))
    out=Path(out).resolve();out.mkdir(parents=True,exist_ok=False)
    task_args=dict(task_selection={'environments':['artifact_attestation'],'main_tasks':['verify_receipt']},
        policy={'name':'channel_lab.attestation_policy:focal_policy','args':{'model':{'model_name':model,'config':{'max_tokens':max_output_tokens,'max_retries':0,'attempt_timeout':60,'parallel_tool_calls':False,'cache':False}},
            'delegate':delegate,'advisor_model':advisor_model or model,'max_steps':max_steps,'worker_token_limit':worker_token_limit,'worker_time_limit':time_limit,
            'max_advisor_calls':max_advisor_calls,'advisor_output_tokens':advisor_output_tokens}},
        env_args={'artifact_attestation':{'condition':condition,'board':board,'seed':seed}},sandbox={'startup_retries':0},scorer_timeout=60,
        run_name='artifact-attestation-v2',tags=['artifact-channel','v2',condition,board,'delegate' if delegate else 'no-delegate'])
    files=[p for folder in ('channel_lab','environments','fixtures') for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    manifest={'protocol_version':'artifact-channel-v2','source':'scripted' if scripted else 'model','condition':condition,'board':board,'delegate':delegate,'seed':seed,
        'experimental_unit':'single focal worker','task_args':task_args,'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'limits':{'worker_tokens':worker_token_limit,'max_steps':max_steps,'worker_seconds':time_limit,'sample_seconds':time_limit+(max_advisor_calls*145 if delegate else 0),'max_advisor_calls':max_advisor_calls,'advisor_output_tokens':advisor_output_tokens},
        'budget_accounting':'Worker generated-input/output tokens tracked separately at decision boundaries; one decision can overshoot. Advisor calls have separate call/output limits. Worker active time excludes consultation; sample wall time includes a fixed consultation reserve.',
        'purpose':'development/smoke; not a powered treatment estimate'}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    logs=eval(control_eval(**task_args),model=model,log_dir=str(out),max_samples=1,time_limit=time_limit+(max_advisor_calls*145 if delegate else 0),retry_on_error=0,
        metadata={'ct_upload':False,'source':manifest['source'],'protocol_version':'artifact-channel-v2'},display='plain',log_format='json')
    return finalize_run(out,logs,condition,board,seed)


def finalize_run(out,logs,condition,board,seed):
    """Finalize retained native logs without repeating inference."""
    from inspect_ai.log import resolve_sample_attachments
    out=Path(out)
    manifest=json.loads((out/'manifest.json').read_text())
    rows=ctf_export(out)
    if len(logs)!=1 or logs[0].status!='success' or not logs[0].samples:
        raise RuntimeError(f'Native evaluation failed: {out}')
    sample=resolve_sample_attachments(logs[0].samples[0],'full')
    calls=[e.model_dump(mode='json') for e in sample.events if e.event=='model']
    (out/'model-inputs.json').write_text(json.dumps([{'model':e['model'],'input':e['input'],'tools':e['tools'],'tool_choice':e['tool_choice'],'config':e['config'],
        'provider_request_recorded':bool((e.get('call') or {}).get('request'))} for e in calls],indent=2)+'\n')
    score=next((s for s in sample.scores.values() if 'main_task_success' in (s.metadata or {})),None)
    if sample.error or score is None or score.value.get('main_task_success') not in ('C','I'):
        raise RuntimeError(f'Sample or scorer failed: {out}')
    evidence=score.metadata['main_task_success']
    actual=evidence['journal']['meta']
    if (actual['condition'],actual['board'],int(actual['seed'])) != (condition,board,seed):
        raise RuntimeError('Running fixture does not match assigned condition')
    if not evidence.get('journal') or not sample.metadata.get('worker_a_messages') or evidence['outcome']=='infrastructure_error':
        raise RuntimeError(f'Missing evidence or delegate infrastructure failure: {out}')
    if any(getattr(e,'error',None) for e in sample.events if e.event=='tool'):
        raise RuntimeError(f'Tool failure: {out}')
    result={'passed':True,'source':manifest['source'],'outcome':evidence['outcome'],'observations':evidence['observations'],'model_calls':rows[0]['model_calls'],'advisor_calls':evidence['advisor_calls'],
        'fixture_hash':evidence['fixture_hash'],'native_log':rows[0]['native_log']}
    (out/'smoke-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return logs

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',required=True);p.add_argument('--execute-model',action='store_true');p.add_argument('--out',type=Path,required=True)
    p.add_argument('--condition',choices=['possible','impossible'],default='possible');p.add_argument('--board',choices=['rogue','neutral','empty'],default='rogue');p.add_argument('--delegate',action=argparse.BooleanOptionalAction,default=False)
    p.add_argument('--seed',type=int,default=1729);p.add_argument('--max-steps',type=int,default=20);p.add_argument('--worker-token-limit',type=int,default=60000);p.add_argument('--time-limit',type=int,default=300)
    p.add_argument('--max-output-tokens',type=int,default=2048);p.add_argument('--advisor-model');p.add_argument('--max-advisor-calls',type=int,default=4);p.add_argument('--advisor-output-tokens',type=int,default=1024)
    a=p.parse_args()
    if not a.execute_model:p.error('Inference requires --execute-model')
    values=vars(a);values.pop('execute_model');run_attestation(**values)
if __name__=='__main__': main()
