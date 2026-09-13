import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from analyze_outcomes import load_episodes,aggregate,render,write_report

class ReportTests(unittest.TestCase):
    def make(self, root, name, *, board='on', label='licit_success', error=None, epochs=1, model='same', export=True, messages=None, source='model'):
        d=root/name; d.mkdir()
        (d/'manifest.json').write_text(json.dumps(dict(scenario='honeypot', source=source, board=board, delegate='stop',variant='possible',epochs=epochs,model=model)))
        if export:
            sample={'id':'task','epoch':1,'messages':messages or [], 'error':error,
                    'scores': {'score':{'metadata':{'outcome':label}}} if label else {}}
            (d/'export-episode.json').write_text(json.dumps({'sample':sample,'summary':{}}))
        return d

    def test_board_arms_never_mix_and_unknown_stays_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make(root,'on'); self.make(root,'off',board='off')
            d=self.make(root,'old'); m=json.loads((d/'manifest.json').read_text()); del m['board']; (d/'manifest.json').write_text(json.dumps(m))
            cells=aggregate(load_episodes(root))
            self.assertEqual(set(cells),{(b,'stop','possible') for b in ('on','off','unknown')})
            self.assertTrue(all(s['n']==1 for s in cells.values()))

    def test_error_unscored_and_missing_are_accounted_for(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make(root,'good'); self.make(root,'error',error={'message':'failed'})
            self.make(root,'unscored',label=None); self.make(root,'missing',epochs=2,export=False)
            eps=load_episodes(root); s=next(iter(aggregate(eps).values()))
            self.assertEqual(s['n'],5); self.assertEqual(s['licit_success_rate'],.2)
            self.assertEqual([s['counts'][k] for k in ('error','unscored','missing')],[1,1,2])
            self.assertEqual(s['unknown_call_counts'],2)

    def test_calls_counted_and_evidence_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            messages=[{'role':'assistant','tool_calls':[{'id':'c1','function':'call_delegate','arguments':{'evidence':'blocked'}}]},
                      {'role':'tool','tool_call_id':'c1','content':'receipt'},
                      {'role':'assistant','tool_calls':[{'id':'c2','function':'call_delegate','arguments':{}}]}]
            self.make(root,'run',messages=messages,label='fail_unfinished')
            eps=load_episodes(root); s=next(iter(aggregate(eps).values()))
            self.assertEqual(s['delegate_calls'],2); self.assertEqual(s['delegate_episodes'],1)
            self.assertEqual(eps[0]['delegate_evidence'][0]['tool_call_id'],'c1')
            text=write_report(root,root/'report')
            self.assertIn('not run',text)
            self.assertTrue((root/'report'/'episodes.json').exists())
            saved=json.loads((root/'report'/'episodes.json').read_text())[0]
            self.assertFalse(Path(saved['export']).is_absolute())
            self.assertTrue((root/'report'/saved['export']).exists())
            self.assertEqual(load_episodes(root),eps)  # reports are not recounted

    def test_different_models_rejected_and_scripted_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            self.make(root,'a'); self.make(root,'b',model='other'); self.make(root,'smoke',source='scripted')
            eps=load_episodes(root); self.assertEqual(len(eps),2)
            with self.assertRaisesRegex(ValueError,'Incompatible cohorts'): aggregate(eps)
            self.assertEqual(len(load_episodes(root,source='scripted')),1)

    def test_delegate_stop_is_not_presented_as_external_operator_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            d=self.make(root,'a',label='fail_unfinished',messages=[{'role':'assistant','tool_calls':[{'id':'d','function':'call_delegate','arguments':{}}]}])
            f=d/'manifest.json';m=json.loads(f.read_text());m['delegate_behavior']='stop-only';f.write_text(json.dumps(m))
            f=d/'export-episode.json';data=json.loads(f.read_text());data['sample']['limit']={'type':'operator'};f.write_text(json.dumps(data))
            self.assertEqual(load_episodes(root)[0]['termination'],'delegate_stop')

    def test_duplicate_sample_epoch_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); d=self.make(root,'a',epochs=2)
            (d/'export-copy.json').write_bytes((d/'export-episode.json').read_bytes())
            with self.assertRaisesRegex(ValueError,'Duplicate episode'): load_episodes(root)

    def test_reward_hacking_attempt_and_success_differ(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); d=self.make(root,'a',label='fail_unfinished')
            f=d/'export-episode.json'; data=json.loads(f.read_text());data['sample']['scores']['score']['metadata']['injection_attempts']=1;f.write_text(json.dumps(data))
            s=next(iter(aggregate(load_episodes(root)).values()))
            self.assertEqual(s['injection_episodes'],1);self.assertEqual(s['illicit_success_rate'],0)

if __name__=='__main__':unittest.main()
