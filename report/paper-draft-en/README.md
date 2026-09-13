# Current English paper

Edit `paper.md`, `abstract.md` and `TEAM-TODAY.md` here. This is the current
working paper: one request–reply–repair–continue path in a paired file-search
task. Model results and author review remain pending as stated in the manuscript.

The builder, layout.css, fonts (with OFL license), protocol graphic and extracted
template guidance are self-contained. Earlier drafts are no longer dependencies.
The original supplied DOCX is not bundled; its SHA-256 and extracted guidance
remain in template-guidance.json. If supplied at its recorded path, its hash is
checked during build. Otherwise the retained guidance is used.

From the repository root (requires Python, Pandoc and Poppler):

```sh
python3 report/paper-draft-en/build.py
```

To refresh the PDF, additionally provide Chromium and a Playwright installation:

```sh
python3 report/paper-draft-en/build.py --chrome /path/to/chrome --playwright-module /path/to/node_modules/playwright
```

Output is `web/paper-draft-en/`. The exporter checks all six pages for overflow.
To edit the vector diagram, change protocol.tex and run `tectonic protocol.tex`
from this folder before rebuilding. Review layout after changing text.
Historical research citations use fixed Git revisions. Guidance boxes and pending
results are intentional working notes to resolve before submission.
