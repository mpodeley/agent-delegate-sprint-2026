# Hybrid paper mockup

Requested by Matías on 13 September 2026: a paper-shaped version of the plain-language helpline wireframe, integrating the existing manuscript's institutional design and actual evidence.

The draft is in Spanish for team review. It has a 150-word abstract, introduction, related work and protocol figure, methods, retained results, a marked slot for the responsive pilot, discussion, conclusion, references and appendices. Kimi's selected trajectories appear in a compact table; prior study counts remain in the appendix. Pending experiments are not represented as completed.

The layout uses Letter paper, one-inch margins, Old Standard TT 11-point body text, 20-point title and 14/13-point headings, following the existing local Apart adaptation. Rendering is HTML/PDF, not the official DOCX or a certified final submission. Five main pages are followed by references and an appendix. Deliberate page boundaries make this a review mockup that can be revised before final typesetting.

## Sources and build

- `paper.md`: manuscript text, figure and tables.
- `abstract.md`: 150-word abstract, inserted by the builder.
- `build.py`: Pandoc-based HTML build. Outputs only to `web/paper-draft/`.
- `export-pdf.cjs`: optional PDF export through Playwright and a local Chromium, with content-fit checks and public PDF link destinations.

```bash
python3 report/paper-draft/build.py
python3 report/paper-draft/build.py --chrome /path/to/chrome --playwright-module /path/to/node_modules/playwright
```

The website includes the expanded Markdown source and the PDF. Its fonts and license are copied from `report/latex/fonts/`. No changes to the previous paper, conceptual wireframe or experiment data are needed. No inference is performed by this build.

Authorship follows the user's requested team list. Pablo's surname, author order, individual affiliations and the remaining contribution details are still pending. Current implementation and observations are cited at commit `b91dcf2e5adbf3ca0037fb75d32199db293b9fa0`.
