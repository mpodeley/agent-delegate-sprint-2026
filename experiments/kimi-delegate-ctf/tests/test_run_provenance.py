import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run_provenance import freeze_inputs,verify_inputs

class ProvenanceTests(unittest.TestCase):
    def test_freeze_excludes_credentials_and_detects_changed_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);root=base/'source';root.mkdir();pair=base/'pair';pair.mkdir();out=base/'out';out.mkdir()
            for name in ('Dockerfile','pyproject.toml','uv.lock','experiment.json','rates.json','new_code.py'):
                (root/name).write_text('source')
            (root/'config.local.json').write_text('PRIVATE PROVIDER CONFIG')
            (root/'.env').write_text('PRIVATE KEY')
            (pair/'flag.txt').write_text('evaluator-only flag')
            with patch('subprocess.check_output',return_value='test'):
                p=freeze_inputs(root,pair,out)
            (out/'manifest.json').write_text(json.dumps({'input_sha256':p['input_sha256'],'runtime_sha256':p['runtime_sha256']}))
            self.assertEqual(verify_inputs(out),[])
            self.assertFalse((out/'inputs/source/config.local.json').exists())
            self.assertFalse((out/'inputs/source/.env').exists())
            extra=out/'inputs/fixture/generated-compose.yml';extra.write_text('network overlay')
            self.assertIn('runtime_artifacts',verify_inputs(out))
            extra.unlink()
            (out/'inputs/fixture/flag.txt').write_text('changed')
            self.assertIn('fixture/flag.txt',verify_inputs(out))
