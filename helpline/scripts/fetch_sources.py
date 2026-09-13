"""Fetch the fixed public URLs in sources.json into quotes/cache/<source_id>.txt and record hashes.

Only URLs listed in sources.json are fetched; nothing inside fetched content is followed.
HTML is reduced to visible text; PDFs go through pdftotext. Whitespace is collapsed.
With --check, compares existing caches against the recorded hashes instead of fetching.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SOURCES = HERE / 'quotes' / 'sources.json'
CACHE = HERE / 'quotes' / 'cache'
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/128 Safari/537.36'


class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def to_text(data, content_type):
    if data[:5] == b'%PDF-' or 'pdf' in content_type:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(data)
        out = subprocess.run(['pdftotext', '-layout', tmp.name, '-'], capture_output=True, check=True)
        text = out.stdout.decode('utf-8', errors='replace')
    else:
        p = Visible()
        p.feed(data.decode('utf-8', errors='replace'))
        text = ' '.join(p.parts)
    return ' '.join(text.split())


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read(), resp.headers.get('Content-Type', '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', nargs='*', help='source ids to fetch')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--record', action='store_true', help='write cache_sha256 into sources.json')
    args = ap.parse_args()
    sources = json.load(open(SOURCES, encoding='utf-8'))
    CACHE.mkdir(exist_ok=True)
    bad = 0
    for sid, meta in sources.items():
        if args.only and sid not in args.only:
            continue
        if meta.get('local_only'):
            continue
        path = CACHE / f'{sid}.txt'
        if args.check:
            if not path.exists():
                print(f'{sid}: missing'); bad += 1; continue
            h = hashlib.sha256(path.read_bytes()).hexdigest()
            ok = h == meta.get('cache_sha256')
            print(f"{sid}: {'ok' if ok else 'HASH DIFFERS'}"); bad += 0 if ok else 1
            continue
        try:
            data, ctype = fetch(meta['url'])
            text = to_text(data, ctype)
        except Exception as exc:  # noqa: BLE001
            print(f'{sid}: fetch failed: {exc}'); bad += 1; continue
        path.write_text(text, encoding='utf-8')
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f'{sid}: {len(text.split())} words, sha256 {h[:12]}')
        if args.record:
            meta['cache_sha256'] = h
    if args.record and not args.check:
        json.dump(sources, open(SOURCES, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
        SOURCES.write_text(SOURCES.read_text(encoding='utf-8') + '\n', encoding='utf-8')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
