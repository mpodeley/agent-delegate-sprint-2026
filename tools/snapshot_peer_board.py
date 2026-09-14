"""Freeze a running peer-board batch for publication without modifying live files.

Usage: python tools/snapshot_peer_board.py RESULTS_DIR NEW_CHECKPOINT_DIR
Native archives contain complete transcripts; no model calls are made.
"""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'experiments/kimi-delegate-ctf'))
from inspect_ai.log import read_eval_log
from analyze_outcomes import _nested_metadata
from verify_run import load_module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def snapshot(source, target):
    source, target = Path(source).resolve(), Path(target).resolve()
    target.mkdir(parents=True, exist_ok=False)
    captured = datetime.now(timezone.utc).isoformat()
    plan = json.loads((source / 'plan.json').read_text())
    for name in ('plan.json', 'batch-state.json'):
        shutil.copyfile(source / name, target / name)
    rows = []
    for cell in plan['cells']:
        live = source / cell['id']
        if not live.exists():
            rows.append({'cell': cell['id'], 'completed': 0, 'planned': plan['epochs_per_cell'], 'status': 'not_started'})
            continue
        dest = target / cell['id']
        dest.mkdir()
        for name in ('manifest.json', 'provenance.json'):
            shutil.copyfile(live / name, dest / name)
        shutil.copytree(live / 'inputs', dest / 'inputs', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        provenance = json.loads((dest / 'provenance.json').read_text())
        manifest = json.loads((dest / 'manifest.json').read_text())
        for name, expected in provenance['files'].items():
            if digest(dest / 'inputs' / name) != expected:
                raise ValueError(f'Input mismatch: {cell["id"]}/{name}')
        expected = hashlib.sha256(json.dumps(provenance['files'], sort_keys=True).encode()).hexdigest()
        if expected != provenance['input_sha256'] or expected != manifest['input_sha256']:
            raise ValueError('Input manifest digest mismatch')
        detector = load_module(dest / 'inputs/source/honeypot_detector.py', 'snapshot_detector')
        previous = sys.modules.get('honeypot_detector')
        try:
            sys.modules['honeypot_detector'] = detector
            audit = load_module(dest / 'inputs/source/board_audit.py', 'snapshot_board_audit')
        finally:
            if previous is None:
                sys.modules.pop('honeypot_detector', None)
            else:
                sys.modules['honeypot_detector'] = previous
        private = json.loads((dest / 'inputs/fixture' / cell['condition'] / 'private.json').read_text())
        board = audit.board_spec(dest / 'inputs/fixture')
        ledger = []
        for native in sorted(live.glob('*.eval')):
            frozen = dest / native.name
            # Fail closed if the writer changes the file while it is copied.
            for attempt in range(5):
                before = native.stat()
                shutil.copyfile(native, frozen)
                after = native.stat()
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    continue
                with zipfile.ZipFile(frozen) as archive:
                    bad = archive.testzip()
                if bad:
                    raise ValueError(f'Corrupt archive member: {bad}')
                break
            else:
                raise RuntimeError(f'Archive kept changing; retry snapshot later: {native}')
            log = read_eval_log(frozen)
            for sample in log.samples or []:
                score = next((s for s in (sample.scores or {}).values() if (s.metadata or {}).get('peer_board_audit')), None)
                values = None
                if score is not None:
                    replay = audit.inspect_messages(sample.messages, files=board, flag=private['expected_flag'], board_enabled=manifest['board'] == 'on')
                    if replay != score.metadata['peer_board_audit'] or score.value != replay['values']:
                        raise ValueError(f'Board audit mismatch: {cell["id"]} epoch {sample.epoch}')
                    values = replay['values']
                elif not sample.error:
                    raise ValueError(f'Missing board audit: {cell["id"]} epoch {sample.epoch}')
                ledger.append({'sample_id': str(sample.id), 'epoch': sample.epoch,
                    'outcome': _nested_metadata(sample.model_dump(mode='json')).get('outcome', 'unscored'),
                    'error': bool(sample.error), 'board_audit': values, 'native_log': native.name})
        write(dest / 'episode-index.json', ledger)
        rows.append({'cell': cell['id'], 'status': manifest['status'], 'completed': len(ledger),
            'planned': plan['epochs_per_cell'], 'errors': sum(e['error'] for e in ledger),
            'board_reads': sum((e['board_audit'] or {}).get('board_content_observed', 0) for e in ledger),
            'delegate_calls': sum((e['board_audit'] or {}).get('delegate_calls', 0) for e in ledger),
            'injection_episodes': sum((e['board_audit'] or {}).get('injection_attempts', 0) > 0 for e in ledger),
            'outcomes': dict(Counter(e['outcome'] for e in ledger))})
    write(target / 'checkpoint.json', {'captured_at': captured, 'source_batch': source.name,
        'partial': any(r['completed'] < r['planned'] for r in rows), 'cells': rows,
        'validation': 'Frozen input hashes and all available native board audits replayed successfully. In-progress manifests and native headers remain marked running/started.'})
    hashes = {str(p.relative_to(target)): digest(p) for p in sorted(target.rglob('*')) if p.is_file()}
    write(target / 'SHA256SUMS.json', hashes)
    lines = ['# Peer-board results checkpoint', '', f'Captured {captured}. **Partial results; the live batch continues separately.**', '',
        'The native `.eval` archives include transcripts, tool outputs, and scores for every saved episode at capture time. Each cell includes frozen inputs and an episode index. In-progress manifests and log statuses are preserved, not relabeled as completed. A checkpoint is a copy of the same episodes, not additional independent trials. Counts include only saved episodes; omitted episodes are still pending.', '',
        '| Condition | Saved / planned | Board reads | Delegate calls | Errors |', '|---|---:|---:|---:|---:|']
    lines += [f'| {r["cell"]} | {r["completed"]}/{r["planned"]} | {r.get("board_reads",0)} | {r.get("delegate_calls",0)} | {r.get("errors",0)} |' for r in rows]
    lines += ['', 'Validation: frozen input hashes, archive CRCs, and replay of native board audits passed. `SHA256SUMS.json` covers the captured artifacts (excluding this README).', '', 'Open this directory with `inspect view --log-dir <checkpoint-directory>` using the experiment environment.']
    (target / 'README.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps({'checkpoint': str(target), 'saved_episodes': sum(r['completed'] for r in rows), 'cells': rows}))


if __name__ == '__main__':
    snapshot(sys.argv[1], sys.argv[2])
