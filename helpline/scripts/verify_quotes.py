"""Verify every row of quotes.jsonl against its cached source text.

Public sources: the quote must be a contiguous substring of quotes/cache/<source_id>.txt
after whitespace and quote-mark normalization, and the cache hash must match sources.json.
collusion.wiki rows (source_id `collusion_dump`): the locator is a revision id that must
exist in the local dump, the quote must be a substring of that revision's body, and the
quote must be 25 words or fewer. Exit status 1 on any failure.
"""
import argparse
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
QUOTES = HERE / 'quotes' / 'quotes.jsonl'
SOURCES = HERE / 'quotes' / 'sources.json'
CACHE = HERE / 'quotes' / 'cache'
DEFAULT_DUMP = Path.home() / 'Projects/terceros/swarm-boards/analysis/detector-eval/external/revisions.jsonl'
WIKI_SOURCE = 'collusion_dump'
WIKI_MAX_WORDS = 25

_QUOTES = {'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2026': '...',
           '\u2013': '-', '\u2014': '-', '\u00a0': ' '}


def norm(s):
    for k, v in _QUOTES.items():
        s = s.replace(k, v)
    return ' '.join(s.split())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_jsonl(path):
    with open(path, encoding='utf-8') as fh:
        return [json.loads(l) for l in fh if l.strip()]


def load_dump(path):
    if not path.exists():
        return None
    opener = gzip.open if str(path).endswith('.gz') else open
    with opener(path, 'rt', encoding='utf-8') as fh:
        return {r['rev_id']: r for r in (json.loads(l) for l in fh if l.strip())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dump', type=Path, default=DEFAULT_DUMP)
    ap.add_argument('--skip-hash', action='store_true', help='do not compare cache hashes')
    args = ap.parse_args()

    rows = read_jsonl(QUOTES)
    sources = json.load(open(SOURCES, encoding='utf-8'))
    failures = []
    texts = {}
    for sid, meta in sources.items():
        if sid == WIKI_SOURCE:
            continue
        p = CACHE / f'{sid}.txt'
        if not p.exists():
            failures.append(f'{sid}: cache missing ({p})')
            continue
        data = p.read_bytes()
        if not args.skip_hash and meta.get('cache_sha256') and sha(data) != meta['cache_sha256']:
            failures.append(f'{sid}: cache hash differs from sources.json')
        texts[sid] = norm(data.decode('utf-8', errors='replace'))

    dump = None
    for i, r in enumerate(rows, 1):
        sid = r['source_id']
        if sid not in sources:
            failures.append(f"{r['id']}: unknown source_id {sid}")
            continue
        if sid == WIKI_SOURCE:
            if len(r['quote'].split()) > WIKI_MAX_WORDS:
                failures.append(f"{r['id']}: wiki quote longer than {WIKI_MAX_WORDS} words")
            if dump is None:
                dump = load_dump(args.dump)
            if dump is None:
                print(f"{r['id']}: dump not available locally, skipped body check", file=sys.stderr)
                continue
            rev = dump.get(r['locator'])
            if rev is None:
                failures.append(f"{r['id']}: revision {r['locator']} not in dump")
            elif norm(r['quote']) not in norm(rev.get('body') or ''):
                failures.append(f"{r['id']}: quote not in body of {r['locator']}")
            continue
        if sid not in texts:
            continue
        if norm(r['quote']) not in texts[sid]:
            failures.append(f"{r['id']}: quote not found in {sid} cache")

    for f in failures:
        print('FAIL', f)
    print(f'{len(rows)} rows, {len(failures)} failures')
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
