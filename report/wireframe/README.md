# Helpline wireframe

Spanish discussion draft requested by Matías on 13 September 2026. It develops the plain-language question, uses Gomez 2026 as the closest experimental antecedent, distinguishes retained Kimi observations from proposed runs, and includes today's run callouts. It is a separate artifact from the selected manuscript.

- `paper.md`: editable five-page narrative, with explicit pending-result boxes.
- `RUN-TODAY.md`: operational handoff grounded in the current runners; no model inference performed by building this artifact.
- `build.py`: Pandoc-based HTML renderer, with `export-pdf.cjs` for optional local Chromium PDF export through Node and Playwright.
- Published destination: `web/wireframe/`, served at `/agent-delegate-sprint-2026/wireframe/`.

Build from the repository root:

```bash
python3 report/wireframe/build.py
python3 report/wireframe/build.py --chrome /path/to/chrome --playwright-module /path/to/node_modules/playwright
```

The PDF is a review wireframe, not the official-template submission. To prepare a later submission, adapt the reviewed text into the canonical template and complete its abstract, author details, references and required appendices. The existing paper, PDF, homepage and experimental records are not modified by this builder.

Authorship follows Matías's request: Matías Podeley, Agustín Brusco, Mateo Zárate, Alejandro Garibotti and Pablo (surname pending). Author order, affiliations and final contribution wording remain to be completed with the team. No surname or contribution has been invented.
