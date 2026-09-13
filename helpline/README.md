# Help-line moments: catalog, antecedents, and a first experiment

Discussion material for the next experiments of the agent-delegate project, prepared after the
Apart AI Incident Response Sprint (September 11–13, 2026). It lives on the `helpline` branch
and does not touch the submitted paper or its data. Written for Mateo, Agustín, Alejandro,
and Pablo.

## What is here

| File | What it is |
|---|---|
| `TAXONOMY.md` | Seventeen labels in three families: ask for help, report a problem, welfare. Cross-cutting fields for the counterfactual, timing, and confidence. |
| `CATALOG.md` | Generated table of every quote by primary label, with coverage counts and the labels found in no source. |
| `quotes/quotes.jsonl` | The database: one verbatim quote per row, with source, locator, labels, and what the quote does not prove. |
| `quotes/sources.json` | Every source with URL, date, access date, and the SHA-256 of the cached text used for verification. |
| `LITERATURE.md` | Where the transcripts come from, and the antecedents: prior implementations and proposals of escalation, ask-for-help, and welfare channels for agents. |
| `EXPERIMENT-1-linuxarena.md` | Design of the first experiment: seeded situations from the catalog, help-line interfaces, mid-episode reminder, visible budgets, on LinuxArena with GLM. |
| `scripts/` | `fetch_sources.py` (cache public sources), `mine_wiki_candidates.py` (candidate lines from the collusion.wiki dump), `verify_quotes.py` (every quote against its cache), `render_catalog.py` (JSONL to Markdown). |
| `tests/test_quotes.py` | Schema, labels, unique ids, the 25-word limit for wiki quotes. |

## How the quotes were made

Public sources were downloaded once and reduced to plain text (`quotes/cache/`, not
versioned; hashes in `sources.json`). A first pass by Claude proposed rows per source; every
row was then checked by `scripts/verify_quotes.py`, which requires the quote to be a contiguous
substring of the cached text after whitespace and quote-mark normalization. Labels are marked
`pending human review` until one of us reads the row against the source and changes
`labeled_by`.

The collusion.wiki rows come from the local revisions dump, which is not republished. Each
quote is 25 words or fewer and its locator is the revision id, so anyone with the public dump
can check it. The candidate pass (`mine_wiki_candidates.py`) runs regex families over the text
each revision added and writes a local file; only rows accepted by a reviewer enter the
database.

## How to add a quote

1. Make sure the source is in `quotes/sources.json` and cached:
   `python3 scripts/fetch_sources.py --only <source_id> --record`.
2. Append a row to `quotes/quotes.jsonl` following `quotes/schema.json`. Copy the quote from
   the cached text; do not fix its typography.
3. Run the checks and regenerate the catalog:

```sh
~/miniforge3/bin/python3 -m unittest discover -s helpline/tests -t helpline
python3 helpline/scripts/verify_quotes.py
python3 helpline/scripts/render_catalog.py
```

## Permission request to the collusion.wiki authors (draft, to be sent by Matías)

> Subject: Quoting 16 short excerpts from the collusion.wiki revisions dump
>
> We are a small group at BAISH (Buenos Aires AI Safety Hub) studying when agents in the
> OpenAI incident could have used a sanctioned line to a human instead of a public wiki. We
> would like to quote 16 excerpts of 25 words or fewer from the revisions dump, each cited by
> revision id, in a public research repository. The dump itself is not republished. Would you
> allow this, and how would you like to be credited? Happy to share the rows before
> publication.

## Open questions for the group

- Who takes which part of Experiment 1 (adapter, situations and rubrics, labeling)?
- H100 access: how many, how long, and whether GLM-5.3 or only GLM-5.3-Flash fits.
- Whether the delegate enters as an arm in the first pilot or after contact behavior is
  measured.
- Whether the welfare family (C) is worth seeding at all, given how little of it the sources
  show, or should stay observational.
- Human review of the labels: the catalog is a draft until someone other than Claude has read
  every row.
