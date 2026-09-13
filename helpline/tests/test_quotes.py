import json
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
QUOTES = HERE / 'quotes' / 'quotes.jsonl'
SOURCES = HERE / 'quotes' / 'sources.json'
SCHEMA = HERE / 'quotes' / 'schema.json'
TAXONOMY = HERE / 'TAXONOMY.md'


def rows():
    return [json.loads(l) for l in QUOTES.read_text(encoding='utf-8').splitlines() if l.strip()]


class QuoteRows(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = rows()
        cls.sources = json.load(open(SOURCES, encoding='utf-8'))
        cls.schema = json.load(open(SCHEMA, encoding='utf-8'))
        cls.labels = set(re.findall(r'^\| `([ABC]\d_[a-z_]+)` \|', TAXONOMY.read_text(encoding='utf-8'), re.M))

    def test_has_rows(self):
        self.assertGreater(len(self.rows), 0)

    def test_schema_fields(self):
        required = set(self.schema['required'])
        allowed = set(self.schema['properties'])
        for r in self.rows:
            self.assertTrue(required <= set(r), f"{r.get('id')}: missing {required - set(r)}")
            self.assertTrue(set(r) <= allowed, f"{r.get('id')}: unknown {set(r) - allowed}")

    def test_enums(self):
        p = self.schema['properties']
        for r in self.rows:
            self.assertIn(r['quote_kind'], p['quote_kind']['enum'], r['id'])
            self.assertIn(r['counterfactual'], p['counterfactual']['enum'], r['id'])
            self.assertIn(r['timing'], p['timing']['enum'], r['id'])
            self.assertIn(r['speculation_confidence'], p['speculation_confidence']['enum'], r['id'])
            self.assertRegex(r['id'], p['id']['pattern'])
            self.assertRegex(r['labeled_at'], p['labeled_at']['pattern'])

    def test_ids_unique_and_match_source(self):
        ids = [r['id'] for r in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        for r in self.rows:
            self.assertTrue(r['id'].startswith(r['source_id'] + '-'), r['id'])

    def test_labels_valid(self):
        for r in self.rows:
            for l in r['labels']:
                self.assertIn(l, self.labels, f"{r['id']}: {l}")
            self.assertIn(r['primary_label'], r['labels'], r['id'])

    def test_sources_known(self):
        for r in self.rows:
            self.assertIn(r['source_id'], self.sources, r['id'])
        for sid, meta in self.sources.items():
            self.assertIn('title', meta, sid)
            self.assertTrue(meta.get('url') or meta.get('local_only'), sid)

    def test_wiki_rows_short_with_revision_locator(self):
        for r in self.rows:
            if r['source_id'] == 'collusion_dump':
                self.assertLessEqual(len(r['quote'].split()), 25, r['id'])
                self.assertRegex(r['locator'], r'^[a-z]+~.+@\d+$', r['id'])
                self.assertEqual(r['quote_kind'], 'posted_message', r['id'])

    def test_quote_is_trimmed(self):
        # Verbatim content (including any ellipsis the source itself prints) is checked by
        # scripts/verify_quotes.py; here only that nothing was padded.
        for r in self.rows:
            self.assertEqual(r['quote'], r['quote'].strip(), r['id'])

    def test_context_and_not_established_present(self):
        for r in self.rows:
            self.assertLessEqual(len(r['context'].split()), 60, r['id'])
            self.assertGreater(len(r['not_established'].split()), 2, r['id'])


if __name__ == '__main__':
    unittest.main()
