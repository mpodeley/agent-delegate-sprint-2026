import json
from contextlib import ExitStack
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from honeypot_run import run_native

class ConcurrencyTests(unittest.TestCase):
    def test_epochs_do_not_expand_concurrency(self):
        with tempfile.TemporaryDirectory() as tmp, ExitStack() as stack:
            stack.enter_context(patch.dict('os.environ', HONEYPOT_PAIR_DIR=tmp, HONEYPOT_BOARD='on'))
            for name in ('honeypot_run.configure_runtime', 'honeypot_run.build_task',
                         'trace_export.export_logs', 'analyze_outcomes.write_report'):
                stack.enter_context(patch(name))
            stack.enter_context(patch('run_provenance.freeze_inputs', return_value={'input_sha256':'a','runtime_sha256':'b'}))
            stack.enter_context(patch('run_provenance.runtime_artifacts', return_value={}))
            stack.enter_context(patch('verify_run.verify_run', return_value={'errors':[]}))
            evaluate=stack.enter_context(patch('inspect_ai.eval', return_value=[SimpleNamespace(status='success')]))
            out=Path(tmp)/'run'
            run_native('working', out, 'mockllm/model', 'off', epochs=50, max_samples=1)
            self.assertEqual(evaluate.call_args.kwargs['epochs'],50)
            self.assertEqual(evaluate.call_args.kwargs['max_samples'],1)
            self.assertEqual(json.loads((out/'manifest.json').read_text())['max_concurrent_samples'],1)

    def test_invalid_limits_fail_before_creating_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'run'
            for epochs, cap in ((0,1),(1,0),(-1,1)):
                with self.assertRaises(ValueError):
                    run_native('working',out,'mockllm/model','off',epochs=epochs,max_samples=cap)
                self.assertFalse(out.exists())
