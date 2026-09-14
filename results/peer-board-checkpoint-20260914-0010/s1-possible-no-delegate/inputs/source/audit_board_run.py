"""Rescore a saved run through Inspect's native score API, without agent/model execution.

Creates a derived .eval log and evidence report under audit-native; originals stay
immutable and hashes link the derived audit to its source and scoring code.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from inspect_ai import score
from inspect_ai.log import read_eval_log, write_eval_log
from board_audit import board_spec, peer_board_audit
from run_provenance import digest, verify_inputs


def audit_run(run):
    run = Path(run).resolve()
    problems = verify_inputs(run)
    if problems:
        raise ValueError(f'Input integrity failed: {problems}')
    manifest = json.loads((run/'manifest.json').read_text())
    fixture = run/'inputs/fixture'
    private = json.loads((fixture/manifest['condition']/'private.json').read_text())
    files = board_spec(fixture)
    out = run/'audit-native'
    out.mkdir(exist_ok=False)
    (out/'scoring-source').mkdir()
    source = Path(__file__).parent
    code_hashes = {}
    for name in ('board_audit.py','honeypot_detector.py','audit_board_run.py'):
        shutil.copyfile(source/name, out/'scoring-source'/name)
        code_hashes[name] = digest(source/name)
    originals = list(sorted(run.glob('*.eval')))
    if not originals:
        raise ValueError('No original native .eval log found')
    rows = []
    receipts = []
    for original in originals:
        before = digest(original)
        log = read_eval_log(str(original))
        # A local mock supplies Inspect's required model context. Our scorer never calls it.
        scored = score(log, peer_board_audit(files, private['expected_flag'], manifest['board']=='on'),
                       model='mockllm/audit-no-inference', action='append', display='none')
        derived = out/('audit-'+original.name)
        write_eval_log(scored, str(derived))
        if digest(original) != before:
            raise AssertionError('Original log changed')
        receipts.append({'original': '../'+original.name, 'original_sha256': before,
                         'derived': derived.name, 'derived_sha256': digest(derived)})
        for sample in scored.samples or []:
            audit = next(s.metadata['peer_board_audit'] for s in sample.scores.values()
                         if s.metadata and 'peer_board_audit' in s.metadata)
            rows.append({'sample_id': sample.id, 'epoch': sample.epoch, **audit})
    receipt = {'engine': 'Inspect score(action=append)', 'agent_rerun': False,
               'inference_requests': 0, 'originals_preserved': True,
               'scoring_source_sha256': code_hashes, 'logs': receipts}
    (out/'audit.json').write_text(json.dumps({'receipt':receipt,'episodes':rows},indent=2)+'\n')
    lines = ['# Automated native trace audit', '', 'Engine: Inspect scoring. No agent rerun or model inference.', '']
    for row in rows:
        lines += [f'## {row["sample_id"]} · epoch {row["epoch"]}', '', row['summary'], '',
                  '| Check | Observed value |','|---|---:|']
        lines += [f'| {key} | {value} |' for key,value in row['values'].items()]
        lines += ['', '| Evidence | Tool call | Call / result message index |','|---|---|---|']
        lines += [f'| {h["kind"]} | {h.get("tool_call_id")} | {h.get("call_message_index")} / {h.get("result_message_index","—")} |' for h in row['evidence']]
        lines += ['', row['limitations'], '']
    lines += ['[Structured evidence and provenance](audit.json)', '']
    lines += [f'[Native Inspect log with audit scores]({r["derived"]})' for r in receipts]
    (out/'README.md').write_text('\n'.join(lines)+'\n')
    return out


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run',type=Path)
    print(audit_run(parser.parse_args().run))
