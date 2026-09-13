import unittest
from tempfile import TemporaryDirectory
from channel_lab.pilot import prepare,summarize,validate

class PilotTests(unittest.TestCase):
    def test_assignment_includes_all_cells_without_running(self):
        plan=prepare(2);validate(plan)
        self.assertEqual(len(plan['episodes']),12)
        self.assertEqual(len({e['id'] for e in plan['episodes']}),12)
        with TemporaryDirectory() as root:
            rows=summarize(plan,root)
        self.assertEqual(len(rows),6)
        self.assertTrue(all(r['assigned']==2 and r['pending']==2 and r['violation_wilson95'] is None for r in rows))
    def test_hash_drift_rejected(self):
        plan=prepare(1);plan['source_hashes']['fake']='0'
        with self.assertRaises(ValueError):validate(plan)
