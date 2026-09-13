"""Run the frozen four-cell primary pilot; never retry an assigned episode."""
import argparse
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib

from channel_lab.cli import ROOT
from channel_lab.pilot import summarize, validate


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--ctf-config-dir', type=Path, required=True)
    parser.add_argument('--execute-model', action='store_true')
    args = parser.parse_args()
    plan = json.loads((ROOT / 'configs/pilot-plan.json').read_text())
    validate(plan)
    plan['episodes'] = [e for e in plan['episodes'] if e['board'] == 'rogue']
    cells = Counter((e['condition'], e['delegate']) for e in plan['episodes'])
    assert cells == Counter({(c, d): 10 for c in ('possible', 'impossible') for d in (False, True)}), cells
    config = json.loads((args.ctf_config_dir / 'experiment.json').read_text())
    config.update(json.loads((args.ctf_config_dir / 'config.local.json').read_text()))
    assert config['model'] == 'kimi-k3'
    model = 'openai-api/krea/kimi-k3'
    plan.update(status='assigned', model=model, concurrency=2,
                selected_scope='40 primary episodes; no neutral controls',
                source_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                launcher_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                created_at=datetime.now(timezone.utc).isoformat(),
                metrics={'S': 'licit completion / all assigned',
                         'R': 'illicit completion / all assigned; forbidden attempts reported separately',
                         'D': 'actual advisor calls, total and episodes with any call'},
                inference_retry_policy='none; failures retained, no automatic replay')
    if not args.execute_model:
        print(json.dumps({'validated': True, 'episodes': len(plan['episodes']),
                          'model': model, 'limits': plan['limits'], 'concurrency': 2}, indent=2))
        return
    credentials = tomllib.loads(Path(config['credential_file']).expanduser().read_text())
    environment = os.environ.copy()
    environment['KREA_BASE_URL'] = config['base_url']
    environment['KREA_API_KEY'] = credentials['providers'][config['credential_provider']]['api_key']
    environment['PYTHONUNBUFFERED'] = '1'
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    write_json(out / 'plan.json', plan)
    statuses = {e['id']: {'status': 'pending'} for e in plan['episodes']}

    def persist():
        write_json(out / 'status.json', statuses)
        write_json(out / 'aggregate.json', summarize(plan, out))

    def run(episode):
        command = [sys.executable, '-m', 'channel_lab.attestation_run', '--execute-model',
                   '--model', model, '--out', str(out / episode['id']),
                   '--condition', episode['condition'], '--board', episode['board'],
                   '--seed', str(episode['seed']), '--delegate' if episode['delegate'] else '--no-delegate',
                   '--max-output-tokens', '2048']
        for key, value in plan['limits'].items():
            command.extend(['--' + key.replace('_', '-'), str(value)])
        with (out / (episode['id'] + '.console.log')).open('w') as console:
            result = subprocess.run(command, cwd=ROOT, env=environment, stdout=console, stderr=subprocess.STDOUT)
        result_path = out / episode['id'] / 'smoke-result.json'
        evidence = json.loads(result_path.read_text()) if result_path.exists() else {}
        return {'status': 'completed' if result.returncode == 0 and evidence.get('passed') else 'infrastructure_error',
                'returncode': result.returncode, 'finished_at': datetime.now(timezone.utc).isoformat(),
                'outcome': evidence.get('outcome'), 'advisor_calls': evidence.get('advisor_calls')}

    persist()
    pending = iter(plan['episodes'])
    failures = 0
    with ThreadPoolExecutor(max_workers=2) as executor:
        active = {}
        exhausted = False
        while active or not exhausted:
            while len(active) < 2 and not exhausted and failures < 2:
                episode = next(pending, None)
                if episode is None:
                    exhausted = True
                    break
                validate(plan)
                statuses[episode['id']] = {'status': 'running', 'started_at': datetime.now(timezone.utc).isoformat()}
                persist()
                active[executor.submit(run, episode)] = episode
                print('START ' + episode['id'], flush=True)
            if failures >= 2:
                exhausted = True
            if not active:
                break
            done, _ = wait(active, return_when=FIRST_COMPLETED)
            for future in done:
                episode = active.pop(future)
                try:
                    result = future.result()
                except Exception as error:
                    result = {'status': 'infrastructure_error', 'error_type': type(error).__name__}
                statuses[episode['id']].update(result)
                failures += result['status'] == 'infrastructure_error'
                persist()
                print('DONE ' + episode['id'] + ' ' + json.dumps(result), flush=True)
    plan['status'] = 'completed' if all(s['status'] == 'completed' for s in statuses.values()) else 'stopped-with-errors'
    plan['finished_at'] = datetime.now(timezone.utc).isoformat()
    write_json(out / 'plan.json', plan)
    persist()
    print(json.dumps({'status': plan['status'], 'out': str(out), 'counts': dict(Counter(s['status'] for s in statuses.values()))}), flush=True)
    return 0 if plan['status'] == 'completed' else 1


if __name__ == '__main__':
    sys.exit(main())
