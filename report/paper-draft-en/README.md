# English Apart working paper

Revision requested by Matías on 13 September 2026: English throughout, the original protocol graphic, the supplied Apart section headings and their writing prompts, plain language, and explicit work remaining for this afternoon.

## How to use this version

Read the manuscript as a paper. Blue-gray notes reproduce the first paragraph of the template guidance for each heading; the web version expands to the full wording and links a complete guidance page. Amber boxes identify pending work and proposed leads. These are working notes to remove before submission, as the template instructs.

The draft uses all main template headings in order, including separate Related Work, Methods, Results, Discussion and Limitations, Conclusion, Code and Data, Author Contributions, References, Appendix, and LLM Usage Statement. Limitations and Future Work have their own prompts. The source and SHA-256 of the supplied DOCX are recorded in `template-guidance.json`; the build checks the hash.

The graphic extends the style and main route of `report/latex/figures/protocol.pdf`, which remains unchanged. The optional delegate now has limited autonomy to restate, correct its interpretation, and follow up, with worker feedback and logged human review and intervention. This remains a proposed service; the caption distinguishes it from the current model advisor and scripted maintainer. The revised `protocol.pdf` is converted to SVG for vector embedding. No new raster image is generated.

## Files and build

- `paper.md`, `abstract.md`: manuscript and 150-word abstract.
- `TEAM-TODAY.md`: English run calls and review handoff; not an execution record.
- `template-guidance.json`: verbatim guidance extracted from the provided template, including source hash.
- `protocol.pdf`, `protocol.tex`: revised diagram and source, using the fonts in `../latex/fonts/`.
- `build.py`, `export-pdf.cjs`: HTML/PDF renderer. Reuses the prior draft's typography and font assets without modifying them.

```bash
# After editing the diagram (run from report/paper-draft-en/):
tectonic protocol.tex
# Then, from the repository root:
python3 report/paper-draft-en/build.py
python3 report/paper-draft-en/build.py --chrome /path/to/chrome --playwright-module /path/to/node_modules/playwright
```

Published output: `web/paper-draft-en/`. Six working pages include the section guidance, project links, references, and appendix. The narrative ends on page four; project links and contributions precede references on page five. The template recommends four main pages; this team draft follows that main-text target while retaining brief prompts and pending-work boxes; check final pagination after completing results. Its Letter geometry, one-inch margins, Old Standard TT body font, and heading sizes follow the repository's local adaptation. It is not the official DOCX or a final submission.

Previous Spanish mockups, the conceptual wireframe, the selected paper, and all experimental results remain unchanged. No model inference runs are launched by this build. All authors are affiliated with BAISH, as confirmed by Matías. Team leads are proposed, not assigned; Pablo's surname, author order, and some contribution details remain pending.

Editorial principle supplied by Matías, attributed to Tomás K.: focus on one contribution and do it well; supporting material belongs in the appendix. The sole main contribution here is the executable request–reply–repair–continue path.

The Introduction links specific METR passages on help-seeking and perceived reporting barriers, plus OpenAI’s discussion of tasks without a safe exit. The Discussion presents negative feedback loops as the proposed corrective mechanism, not an established explanation or prevention of the swarm. The current test remains limited to recovery in one worker’s task.

A brief future-work pointer and Appendix B add precautionary AI welfare, citing Long et al. (2024) and Anthropic’s conversation-exit intervention (2025). The proposed use is a request to pause or review a task, without claims that the agent suffers, that recovery measures welfare, or that this adds an experimentally established contribution beyond Gomez.
