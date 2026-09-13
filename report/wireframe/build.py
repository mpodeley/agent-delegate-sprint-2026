"""Render the Spanish discussion wireframe and its run guide, without inference.

Requires Pandoc. Optional PDF additionally uses Node and Playwright.
Outputs are confined to web/wireframe; existing paper artifacts are untouched.
"""
import argparse
import html
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "web" / "wireframe"

STYLE = """
@font-face{font-family:Plex;src:url('../fonts/ibm-plex-sans-400.woff2') format('woff2');font-weight:400;font-display:swap}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#e8e9e6;color:#222c2b;font-family:Plex,Arial,sans-serif;font-size:10.4pt;line-height:1.42}
nav{max-width:960px;margin:0 auto;padding:20px 25px;display:flex;flex-wrap:wrap;gap:12px 23px;align-items:center;font-size:14px}nav strong{margin-right:auto}a{color:#206b61;text-underline-offset:3px}nav a{text-decoration:none;border-bottom:1px solid #a7bbb5}main{padding:0 16px 36px}.page{position:relative;width:210mm;min-height:297mm;margin:0 auto 24px;padding:17mm 19mm 19mm;background:#fffefa;box-shadow:0 2px 14px #23352b13}.eyebrow{font-size:9px;text-transform:uppercase;letter-spacing:1.7px;color:#55716a;border-top:3px solid #275f53;padding-top:10px;margin-bottom:21px;display:flex;justify-content:space-between}.page h1{font-size:30pt;line-height:1.08;letter-spacing:-1.1px;max-width:620px;margin:17px 0 18px}.page h2{font-size:17pt;line-height:1.2;margin:23px 0 10px;letter-spacing:-.3px}.page p{margin:0 0 11px}.page strong{font-weight:700}.page>p:has(em){color:#60706b;font-size:9.2pt}.page>p:has(em)+h2{margin-top:27px}aside{margin:15px 0;padding:13px 16px;border-left:3px solid #3f7469;background:#eef4ef}aside p:last-child{margin-bottom:0}aside>strong{display:block;font-size:10pt;margin-bottom:7px}.question{font-size:14pt;line-height:1.38}.editorial{background:#f1f0eb;border-color:#9b9b90;color:#58605b}.todo{border-color:#b57b40;background:#faf1e4}.pending{background:transparent;border:1px dashed #b19270;color:#685743}.pending>strong,.todo>strong{letter-spacing:.2px}.protocol{margin:22px 0}.flow{display:flex;align-items:stretch;gap:8px}.flow>div{flex:1;border:1px solid #a5b9b1;border-top:3px solid #426f62;border-radius:3px;padding:12px 10px;background:#f6f9f5}.flow span{font-size:9px;text-transform:uppercase;letter-spacing:1px;color:#5d746b;display:block;margin-bottom:6px}.flow strong{font-size:13px;line-height:1.25;display:block;margin-bottom:8px}.flow p{font-size:11px;line-height:1.4;margin:0}.flow>b{align-self:center;font-size:20px;color:#426f62}.return{margin-top:9px;background:#eaf1e9;padding:10px 13px;font-size:12px;border-radius:3px}figcaption{font-size:9pt;color:#5c6963;line-height:1.35;margin-top:10px}table{width:100%;border-collapse:collapse;font-size:9.3pt;line-height:1.35;margin:17px 0}th{text-align:left;background:#eaf0e9}td,th{padding:9px;border-bottom:1px solid #d8dfd7;vertical-align:top}th:first-child{width:22%}code{font-size:.9em;background:#e8eae5;padding:1px 3px;border-radius:3px}footer{position:absolute;bottom:9mm;left:19mm;right:19mm;display:flex;justify-content:space-between;color:#748077;font-size:9px;border-top:1px solid #dce1d7;padding-top:7px}.references{font-size:8.2pt;line-height:1.32}.references ol{padding-left:18px}.references li{margin-bottom:5px}.guide{max-width:920px;margin:auto;padding:32px 40px;background:#fffefa}.guide h1{font-size:28px}.guide h2{font-size:22px;margin-top:28px}.guide pre{padding:16px;background:#eef0e9;overflow:auto;font-size:12px}.guide code{background:none}.guide li{margin-bottom:7px}
@media(max-width:820px){.page{width:100%;min-height:0;padding:28px 24px 65px}.page h1{font-size:30px}.page h2{font-size:23px}.eyebrow{font-size:8px;letter-spacing:.8px}.flow{flex-direction:column}.flow>b{transform:rotate(90deg)}.flow strong{font-size:16px}.flow p{font-size:14px}footer{left:24px;right:24px;bottom:20px}.guide{padding:24px 18px}table{font-size:11px}td,th{padding:6px}}
@page{size:A4;margin:0}
@media print{html{scroll-behavior:auto}body{background:white;-webkit-print-color-adjust:exact;print-color-adjust:exact}nav{display:none}main{padding:0}.page{width:210mm;height:297mm;min-height:0;margin:0;padding:17mm 19mm 19mm;box-shadow:none;break-after:page}.page:last-child{break-after:auto}a{color:inherit;text-decoration:none}.flow{flex-direction:row}.flow>b{transform:none}aside,figure,table{break-inside:avoid}.guide{padding:18mm;font-size:10pt}.guide pre{white-space:pre-wrap;overflow-wrap:anywhere}.guide h2{break-after:avoid}}
"""


def render(markdown):
    return subprocess.run(["pandoc", "--from=markdown+raw_html", "--to=html5"],
                          input=markdown, capture_output=True, text=True, check=True).stdout


def document(title, body, guide=False):
    nav = ('<a href="index.html">Wireframe</a>' if guide else
           '<a href="wireframe.pdf">Descargar PDF</a>')
    nav += '<a href="run-today.html">Corridas para hoy</a><a href="../helpline/">Catálogo helpline</a><a href="../paper.pdf">Paper anterior</a>'
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="Wireframe de helpline: una pregunta, primeros experimentos y lo que falta probar. Borrador para el sprint.">
<style>{STYLE}</style></head><body><nav aria-label="Documentos"><strong>HELPLINE / WIREFRAME</strong>{nav}</nav>
{body}</body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chrome", type=Path, help="Optional local Chromium executable for PDF export")
    parser.add_argument("--playwright-module", default="playwright", help="Installed Playwright module name or absolute path")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    parts = (HERE / "paper.md").read_text().split("<!-- page -->")
    pages = []
    for number, part in enumerate(parts, 1):
        content = render(part).replace('href="RUN-TODAY.md"', 'href="run-today.html"')
        pages.append(f'<article class="page" id="page-{number}" aria-label="Página {number}">'
                     '<div class="eyebrow"><span>BAISH · AI Incident Response Sprint</span><span>Borrador de discusión · 13 sep 2026</span></div>'
                     + content + f'<footer><span>Helpline · Pregunta, diseño y primeras pruebas</span><span>{number} / {len(parts)}</span></footer></article>')
    (OUT / "index.html").write_text(document("Helpline — wireframe del entregable", '<main>'+"\n".join(pages)+'</main>'))
    runbook = render((HERE / "RUN-TODAY.md").read_text()).replace('href="paper.md"', 'href="index.html"')
    (OUT / "run-today.html").write_text(document("Helpline — corridas para hoy", '<main class="guide">'+runbook+'</main>', guide=True))
    for name in ("paper.md", "RUN-TODAY.md"):
        shutil.copyfile(HERE / name, OUT / name)
    if args.chrome:
        subprocess.run(["node", str(HERE / "export-pdf.cjs"), str(args.chrome), args.playwright_module],
                       check=True, timeout=60)
    print(f"Built {len(parts)} wireframe pages and run guide in {OUT}")


if __name__ == "__main__":
    main()
