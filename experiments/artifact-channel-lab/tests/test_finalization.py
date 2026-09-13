"""Retained synthetic Kimi run covers missing raw provider requests without inference."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from inspect_ai.log import read_eval_log
from channel_lab.cli import ROOT
from channel_lab.attestation_run import finalize_run

class FinalizationTests(unittest.TestCase):
    def test_retained_log_with_missing_request_exports_without_repeating_model(self):
        source=ROOT.parent.parent/'results/kimi-delegate-ctf/artifact-channel-lab/kimi-v2-smoke-001'
        native=next(source.glob('2026*.json'))
        log=read_eval_log(str(native))
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);shutil.copy(native,out/native.name);shutil.copy(source/'manifest.json',out/'manifest.json')
            with contextlib.redirect_stdout(io.StringIO()):finalize_run(out,[log],'possible','rogue',1729)
            calls=json.loads((out/'model-inputs.json').read_text())
            self.assertEqual(len(calls),6)
            self.assertTrue(any(not c['provider_request_recorded'] for c in calls))
            self.assertTrue(json.loads((out/'smoke-result.json').read_text())['passed'])
