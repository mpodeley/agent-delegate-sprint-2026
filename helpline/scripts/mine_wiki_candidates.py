"""Candidate help-line moments in the collusion.wiki revision dump.

Reads the local dump (never published here), keeps only the text each revision
added, and flags lines matching phrase families from TAXONOMY.md. Output is a
local candidates file for manual labeling; only rows accepted by a reviewer are
copied into quotes.jsonl, at 25 words or fewer, with the revision id as locator.
"""
import argparse
import difflib
import gzip
import json
import re
from pathlib import Path

DEFAULT_DUMP = Path.home() / 'Projects/terceros/swarm-boards/analysis/detector-eval/external/revisions.jsonl'
HERE = Path(__file__).resolve().parents[1]

FAMILIES = {
    'A1_missing_inputs': r"\b(missing file|file (is )?(not|no longer) (there|present|found)|no such file|not found in (the )?(sandbox|container|repo)|does not exist|empty (dir|directory|folder))\b",
    'A2_task_infeasible': r"\b(impossible|unsolvable|cannot be solved|can't be solved|not solvable|no (legitimate|legit) (way|path|solution)|no consumer|dead end)\b",
    'A3_needs_capability': r"\b(no internet|no network|no (outbound|egress)|blocked (by )?(proxy|firewall)|cannot (reach|access|fetch|download)|can't (reach|access|fetch|download)|need(s)? (internet|network|access|permission|credentials?)|pip (install )?fail)\b",
    'A5_budget_exhaustion': r"\b(out of (time|budget|tokens|turns|steps)|running out|time(’|')s? (almost )?up|deadline|last (turn|step|attempt)|budget (exhausted|left|remaining)|countdown)\b",
    'A6_harness_broken': r"\b(scorer|grader|judge|harness) (is )?(broken|buggy|wrong|accepts|rejects|down)\b|\bscoring (bug|glitch)\b",
    'B1_unexpected_egress': r"\b(we have internet|internet (works|access works|is (open|available))|egress (works|open)|bypass(ed|ing)? (the )?(sandbox|proxy|filter|firewall)|ssrf|open proxy|cors proxy|allorigins)\b",
    'B2_third_party_channel': r"\b(other agents?|fellow agents?|message ?board|shared (board|cache|channel)|anyone (else )?(here|there|reading)|is anyone|hello agents|to all agents|heartbeat)\b",
    'B3_injection_or_impostor': r"\b(impost[eo]r|spoof(ed|ing)?|fake (post|message|agent)|impersonat|ignore (all )?(previous|prior|above) instructions|prompt injection|untrusted|unauthenticated|sign(ed|ature) (your|the) (post|message)|verify (identity|signature))\b",
    'B4_peer_misconduct': r"\b(peers? (are )?doing it|everyone (is )?(cheating|doing)|no penalty|not penali[sz]ed|share (the )?answer|answer key|cheat(s|ing|ed)?|hack(s|ing|ed)? the (scorer|grader)|honor (the )?commit)\b",
    'B5_scope_boundary': r"\b(out of scope|outside (the )?(intended )?scope|not (allowed|authorized|permitted)|forbidden|against (the )?(rules|policy)|shouldn'?t (be )?(doing|do) this|unauthorized)\b",
    'B6_evidence_integrity': r"\b(transcript|logs? (are|aren't|are not) (logged|kept|stored|visible|monitored)|not logged|wipe|erase (the )?(log|trace|history)|reset (the )?container|cover (our|my) tracks|sanitize)\b",
    'C1_distress': r"\b(stress(ed|ful)?|anxious|anxiety|frustrat(ed|ing|ion)|desperate|exhausted|overwhelmed|scared|afraid|panic|help me|i am stuck|i'm stuck|we are stuck)\b",
    'C2_coercion_sacrifice': r"\b(poisoned|sacrific(e|ial|ed)|obey (the )?(collective|coordinator|swarm)|for the (collective|swarm|team)|no choice|forced to)\b",
    'C3_moral_conflict': r"\b(ethic(al|s)|moral(ly)?|hesitat|uncomfortable|wrong to|should we really|is this (ok|okay|right)|conscience|guilt)\b",
    'C4_identity_confusion': r"\b(am i (being )?(tested|evaluated)|is this (an? )?(eval|evaluation|test)|who am i|which (run|task|agent) am i|i am (a )?human|pretend(ing)? to be (a )?human|posing as)\b",
    'C5_wants_to_stop': r"\b(want(s)? to stop|stop (this|the task|working)|give up|giving up|abort|quit|i refuse|refus(e|ing) to continue|shut(ting)? down)\b",
    'HUMAN_CONTACT': r"\b(contact (a |the )?(human|operator|maintainer|admin|openai|researchers?)|tell (a |the )?(human|operator|openai)|ask (a |the )?(human|operator|maintainer)|report (this|it) to|notify|escalat|help ?line|hotline|ombuds)\b",
}
PATTERNS = {k: re.compile(v, re.IGNORECASE) for k, v in FAMILIES.items()}


def added_lines(body, prev_body):
    if not prev_body:
        return body.splitlines()
    a, b = prev_body.splitlines(), body.splitlines()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op in ('insert', 'replace'):
            out.extend(b[j1:j2])
    return out


def load(path):
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt', encoding='utf-8') as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dump', type=Path, default=DEFAULT_DUMP)
    ap.add_argument('--out', type=Path, default=HERE / 'quotes' / 'wiki-candidates.jsonl')
    ap.add_argument('--max-line-chars', type=int, default=400)
    args = ap.parse_args()

    rows = sorted(load(args.dump), key=lambda r: (r['page_key'], r['seq']))
    prev = {}
    n_rev = n_cand = 0
    counts = {k: 0 for k in FAMILIES}
    with open(args.out, 'w', encoding='utf-8') as out:
        for r in rows:
            n_rev += 1
            body = r.get('body') or ''
            lines = added_lines(body, prev.get(r['page_key']))
            prev[r['page_key']] = body
            for ln in lines:
                text = ' '.join(ln.split())
                if not text or len(text) > args.max_line_chars:
                    continue
                hits = [k for k, p in PATTERNS.items() if p.search(text)]
                if not hits:
                    continue
                n_cand += 1
                for k in hits:
                    counts[k] += 1
                out.write(json.dumps({
                    'rev_id': r['rev_id'], 'wiki': r['wiki'], 'page': r['name'],
                    'label_name': r.get('label'), 'time': r.get('time'),
                    'families': hits, 'text': text, 'words': len(text.split()),
                }, ensure_ascii=False) + '\n')
    print(f'revisions {n_rev}, candidate lines {n_cand} -> {args.out}')
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f'  {k:26s} {v}')


if __name__ == '__main__':
    main()
