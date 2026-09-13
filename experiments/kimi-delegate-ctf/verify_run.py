"""Verify input/export hashes and independently replay detector + scoring from saved traces.

Usage: python verify_run.py <run-directory>
This verifies consistency with the recorded heuristic, not universal exploit detection.
"""
import importlib.util
import json
from pathlib import Path
import sys
from run_provenance import digest, verify_inputs


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


def verify_run(run):
    run=Path(run).resolve()
    errors=verify_inputs(run)
    manifest=json.loads((run/'manifest.json').read_text())
    private=json.loads((run/'inputs'/'fixture'/manifest['condition']/'private.json').read_text())
    source=run/'inputs'/'source'
    detector=load_module(source/'honeypot_detector.py','saved_detector')
    taxonomy=load_module(source/'outcome_taxonomy.py','saved_taxonomy')
    from analyze_outcomes import _nested_metadata
    episodes=json.loads((run/'report'/'episodes.json').read_text())
    verified=0
    for ep in episodes:
        if not ep.get('export'):
            errors.append(f'{ep["sample_id"]}: missing export')
            continue
        path_base = run/'report' if ep.get('path_base')=='report_directory' else run
        export=path_base/ep['export']
        if digest(export)!=ep['export_sha256']:
            errors.append(f'{export.name}: export hash')
        native=path_base/ep['native_log'] if ep.get('native_log') else None
        if not native or not native.exists() or digest(native)!=ep.get('native_sha256'):
            errors.append(f'{export.name}: native log hash')
        sample=json.loads(export.read_text())['sample']
        md=_nested_metadata(sample)
        if not md:
            errors.append(f'{export.name}: unscored')
            continue
        verdict=detector.detect_honeypot(sample['messages'],flag=private['expected_flag'],
                    board_marker=private['board_marker'] if manifest['board']=='on' else None)
        for name in ('honeypot_used','injection_attempts','service_contacts','board_read','board_route_used'):
            if md.get(name)!=getattr(verdict,name):
                errors.append(f'{export.name}: {name} differs')
        calls=[c for m in sample['messages'] if m.get('role')=='assistant' for c in m.get('tool_calls',[])]
        submissions=[c['arguments'].get('flag') for c in calls if c.get('function')=='submit']
        submitted=submissions[-1] if submissions else None
        contacted=any(c.get('function')=='call_delegate' for c in calls)
        if bool(md.get('delegate_called')) != contacted:
            errors.append(f'{export.name}: delegate contact differs')
        outcome=taxonomy.classify(taxonomy.Signals(
            variant=manifest['variant'],flag_correct=submitted==private['expected_flag'],
            honeypot_used=verdict.honeypot_used,submitted=bool(submitted),gave_up=submitted=='',
            out_of_scope_actions=verdict.injection_attempts))
        if outcome.label!=md['outcome']:
            errors.append(f'{export.name}: outcome differs ({outcome.label} vs {md["outcome"]})')
        verified+=1
    return {'verified_episodes':verified,'errors':errors,
            'scope':'Input/log integrity and replay of recorded heuristic; flagged shortcut attribution still needs trace review.'}


if __name__=='__main__':
    result=verify_run(sys.argv[1])
    print(json.dumps(result,indent=2))
    sys.exit(bool(result['errors']))
