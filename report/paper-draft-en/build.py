"""Build the English Apart working draft with source-grounded section guidance.

The revised protocol PDF is converted to SVG for vector embedding.
No previous manuscript, wireframe, or experimental output is changed.
"""
import argparse
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "web" / "paper-draft-en"
BASE = "https://mpodeley.github.io/agent-delegate-sprint-2026/paper-draft-en/"

# Reuse the existing template typography; this import does not run its builder.
spec = importlib.util.spec_from_file_location("paper_layout", ROOT / "report/paper-draft/build.py")
layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layout)
STYLE = layout.STYLE.replace("url('fonts/", "url('../paper-draft/fonts/") + """
.template-guide{margin:6px 0 12px;padding:7px 10px;border-left:2px solid #9bafba;background:#f1f5f7;color:#45565e;font-family:Arial,sans-serif;font-size:8.3px;line-height:1.35}.template-guide .guide-label{font-weight:bold;text-transform:uppercase;letter-spacing:.55px;margin-bottom:3px}.template-guide p{margin:0 0 3px}.template-guide p:last-child{margin:0}.template-guide details{margin-top:4px}.template-guide summary{cursor:pointer;font-size:8px;color:#4c646e}.template-guide .full-guidance{padding-top:6px}.original-protocol img{display:block;width:100%;height:auto}.original-protocol{margin:13px 0 14px}.page .titleblock{margin-bottom:13px}.page .titleblock p{font-size:10pt}.page .titleblock .draft-status{font-size:8px}.page h2{margin-top:14px}.page h3{margin-top:12px}.page ul{margin:6px 0 10px;padding-left:21px}.page li{margin-bottom:4px}.compact-references{font-size:9.1pt;line-height:1.19}.compact-references li{margin-bottom:7px}aside{margin:11px 0;padding:10px 12px}.guide-document{max-width:900px;margin:0 auto 30px;padding:35px;background:white}.guide-document h1{font-size:24px}.guide-document h2{margin-top:25px;font-size:20px}.guide-document pre{background:#f2f3ee;padding:12px;overflow-x:auto;font-size:11px;line-height:1.4}.guide-document li{margin-bottom:7px}.guide-document code{font-size:.82em}.guide-document .template-source{font-size:10pt;color:#53665a}.guide-document .template-full{border-left:2px solid #9bafba;padding-left:14px}.page:has(#abstract) #abstract{text-align:center}.page:has(#abstract) #abstract~p:first-of-type{font-size:10.5pt}
@media screen and (max-width:850px){.guide-document{padding:25px 18px}.template-guide{font-size:10px}.template-guide summary{font-size:10px}.page .original-protocol{overflow-x:auto}.page .original-protocol img{min-width:560px}.page .original-protocol figcaption{min-width:0}}
@media print{.template-guide details{display:none}.template-guide{font-size:8.3px;line-height:1.3}.page .original-protocol{overflow:visible}.page .original-protocol img{min-width:0}.guide-document{padding:1in;font-size:10pt}.guide-document pre{white-space:pre-wrap;overflow-wrap:anywhere}}
"""

STYLE += "\n.page:has(#appendix-optional) td{padding-block:6px}\n"


def render(text):
    return subprocess.run(["pandoc", "--from=markdown+raw_html", "--to=html5"], input=text,
                          text=True, capture_output=True, check=True).stdout


def wrap(title, body):
    nav = '<nav aria-label="Draft resources"><strong>HELPLINE · ENGLISH WORKING DRAFT</strong><a href="index.html">Paper</a><a href="paper-draft.pdf">PDF</a><a href="team-today.html">Team tasks and runs</a><a href="template-guidance.html">Full Apart guidance</a><a href="paper.md">Editable text</a></nav>'
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'+f'<title>{html.escape(title)}</title><style>{STYLE}</style></head><body>'+nav+body+'</body></html>'


def guidance_block(key, guides):
    paragraphs = guides[key]
    excerpt = html.escape(paragraphs[0])
    full = ''.join('<p>'+html.escape(p)+'</p>' for p in paragraphs)
    return '<div class="template-guide"><div class="guide-label">Apart template prompt · verbatim</div><p>'+excerpt+'</p><details><summary>Full guidance for this section</summary><div class="full-guidance">'+full+'</div></details></div>'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--chrome", type=Path)
    ap.add_argument("--playwright-module", default="playwright")
    args = ap.parse_args()
    guidance = json.loads((HERE / "template-guidance.json").read_text())
    assert hashlib.sha256((ROOT / guidance['source']).read_bytes()).hexdigest() == guidance['sha256']
    abstract = (HERE / "abstract.md").read_text().strip()
    assert len(abstract.split()) == 150
    source = (HERE / "paper.md").read_text().replace('<!-- abstract -->', abstract)
    keys = re.findall(r'<!-- guidance:(.*?) -->', source)
    assert set(keys) == set(guidance['sections']), "Every template section needs a visible prompt."
    expanded = re.sub(r'<!-- guidance:(.*?) -->', lambda m: guidance_block(m[1], guidance['sections']), source)
    parts = expanded.split('<!-- page -->')
    assert len(parts) == 6
    OUT.mkdir(parents=True, exist_ok=True)
    subprocess.run(['pdftocairo', '-svg', str(HERE / 'protocol.pdf'), str(OUT / 'protocol.svg')], check=True)
    shutil.copyfile(HERE / 'protocol.pdf', OUT / 'protocol.pdf')
    pages = []
    for i, part in enumerate(parts, 1):
        pages.append(f'<article class="page" id="page-{i}" aria-label="Page {i}">'
                     '<div class="document-note">Team working draft · English · 13 September 2026</div>'
                     '<div class="page-content">'+render(part)+'</div>'
                     f'<footer><span>Agent Delegate · Apart working draft · Guidance and pending work retained</span><span>{i} / {len(parts)}</span></footer></article>')
    (OUT / 'index.html').write_text(wrap('Agent Delegate — English Apart working draft', '<main>'+''.join(pages)+'</main>'))
    (OUT / 'paper.md').write_text(expanded)
    (OUT / 'abstract.md').write_text(abstract+'\n')
    team = (HERE / 'TEAM-TODAY.md').read_text()
    (OUT / 'TEAM-TODAY.md').write_text(team)
    (OUT / 'team-today.html').write_text(wrap('Helpline — team tasks for this afternoon', '<main class="guide-document">'+render(team)+'</main>'))
    full = '# Apart template guidance\n\nVerbatim extraction from the supplied DOCX. Guidance is retained in this working draft to help the team fill each section. The template instructs teams to remove it before submission.\n\n'
    full += '## How to use the template\n\n'+'\n\n'.join(guidance['global_guidance'])+'\n\n'
    for heading, paras in guidance['sections'].items():
        full += '## '+heading+'\n\n'+'\n\n'.join(paras)+'\n\n'
    (OUT / 'TEMPLATE-GUIDANCE.md').write_text(full.rstrip()+'\n')
    (OUT / 'template-guidance.html').write_text(wrap('Apart — full source template guidance', '<main class="guide-document template-full">'+render(full)+'</main>'))
    if args.chrome:
        subprocess.run(['node',str(HERE/'export-pdf.cjs'),str(args.chrome),args.playwright_module],check=True,timeout=60)
    proof = {'template_source':guidance['source'],'template_sha256':guidance['sha256'],
             'section_prompts':keys,'abstract_words':150,'planned_pages':len(parts),
             'diagram_source':'report/paper-draft-en/protocol.tex',
             'diagram_predecessor':'report/latex/figures/protocol.pdf',
             'diagram_revision':'Optional delegate with limited autonomy, worker feedback, and human review',
             'diagram_sha256':hashlib.sha256((HERE/'protocol.pdf').read_bytes()).hexdigest(),
             'language':'en','new_model_runs':False}
    (OUT / 'build.json').write_text(json.dumps(proof,indent=2)+'\n')
    print('Built six-page English draft, revised diagram, all template prompts, and team run guide.')


if __name__ == '__main__':
    main()
