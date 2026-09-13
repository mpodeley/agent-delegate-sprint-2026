"""Build the hybrid paper mockup, independently of the earlier paper and wireframe.

Pandoc renders Markdown; optional PDF export uses Node, Playwright and Chromium.
Typography and geometry follow the repository's local Apart template adaptation.
"""
import argparse
import html
from pathlib import Path
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "web" / "paper-draft"

STYLE = """
@font-face{font-family:OldStandard;src:url('fonts/OldStandard-Regular.ttf');font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:OldStandard;src:url('fonts/OldStandard-Bold.ttf');font-weight:700;font-style:normal;font-display:swap}
@font-face{font-family:OldStandard;src:url('fonts/OldStandard-Italic.ttf');font-weight:400;font-style:italic;font-display:swap}
*{box-sizing:border-box}body{margin:0;background:#e9e8e4;color:#181b1a;font-family:OldStandard,Georgia,serif;font-size:11pt;line-height:1.24}a{color:#225e57;text-underline-offset:2px}nav{max-width:1000px;margin:auto;padding:18px 22px;display:flex;gap:12px 22px;align-items:center;flex-wrap:wrap;font-family:Arial,sans-serif;font-size:13px}nav strong{margin-right:auto}nav a{text-decoration:none;border-bottom:1px solid #a9b9b3}.page{position:relative;width:8.5in;min-height:11in;padding:1in;margin:0 auto 24px;background:#fff;box-shadow:0 2px 14px #17292015}.page-content{position:relative}.page h1{font-size:20pt;line-height:1.15;margin:12px 0 16px;font-weight:700}.page h2{font-size:14pt;line-height:1.18;margin:18px 0 7px}.page h3{font-size:13pt;line-height:1.18;margin:13px 0 6px}.page p{margin:0 0 8px}.titleblock{text-align:center;border-top:2px solid #171d1a;padding-top:4px;margin-bottom:16px}.titleblock h1{border-bottom:1px solid #9a9e98;padding-bottom:12px}.titleblock p{margin-bottom:7px}.titleblock .draft-status{font-family:Arial,sans-serif;font-size:8px;color:#69716a;margin:9px 0 0}.abstract{margin-bottom:17px}.abstract>p:first-child{text-align:center;margin-bottom:7px}.abstract>p:last-child{font-size:10.5pt;line-height:1.23}.page:first-of-type h2{margin-top:16px}table{width:100%;border-collapse:collapse;font-size:10pt;line-height:1.22;margin:13px 0 6px}th{text-align:left;border-top:1.4px solid #222;border-bottom:.7px solid #777;padding:6px 7px}td{border-bottom:.5px solid #ccc;padding:7px;vertical-align:top}.table-caption,figcaption{font-size:9.5pt;line-height:1.2;margin-top:7px;margin-bottom:11px;color:#3d4640}.protocol{margin:17px 0 15px}.flow{display:flex;gap:6px;align-items:stretch;font-family:Arial,sans-serif}.flow>div{flex:1;border:1px solid #819289;border-radius:3px;padding:10px 8px}.flow span{display:block;color:#617066;font-size:8px;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}.flow strong{display:block;font-size:11px;line-height:1.2;margin-bottom:6px}.flow p{font-size:10px;line-height:1.3;margin:0}.flow>b{align-self:center;color:#53685c;font-size:17px}.return{border-top:1px solid #8da297;border-bottom:1px solid #8da297;padding:8px 10px;margin-top:8px;background:#f1f5f1;font-size:10pt}.delegate-note{padding:7px 10px;font-size:9.5pt;border-left:1px dashed #869288;margin:7px 0 11px}aside{padding:11px 13px;margin:13px 0;border:1px solid #b99b70;background:#fcf7ee;font-size:10pt;line-height:1.25}aside>strong{display:block;font-family:Arial,sans-serif;font-size:9px;letter-spacing:.4px;text-transform:uppercase;margin-bottom:8px}aside p:last-child{margin-bottom:0}.editorial{background:#f4f5f1;border-color:#a2aea2}code{font-family:monospace;font-size:.84em;overflow-wrap:anywhere}.references{font-size:10pt;line-height:1.3}.references ol{padding-left:20px;margin:10px 0 15px}.references li{margin-bottom:10px}footer{position:absolute;left:1in;right:1in;bottom:.45in;border-top:.5px solid #c5cbc5;padding-top:6px;display:flex;justify-content:space-between;color:#707970;font-family:Arial,sans-serif;font-size:8px}.document-note{position:absolute;top:.45in;left:1in;right:1in;text-align:right;font-family:Arial,sans-serif;font-size:8px;color:#80877f}
@media screen and (max-width:850px){main{padding:0 12px}.page{width:100%;min-height:0;padding:35px 23px 65px}.page h1{font-size:27px}.page h2{font-size:23px}.page h3{font-size:20px}.document-note{position:static;margin-bottom:16px}.titleblock p{font-size:14px}.flow{flex-direction:column}.flow>b{transform:rotate(90deg)}.flow strong{font-size:15px}.flow p{font-size:13px}.flow span{font-size:10px}.references{font-size:11pt}footer{left:23px;right:23px;bottom:20px}td,th{padding:6px}table{font-size:9pt}}
@page{size:Letter;margin:0}
@media print{body{background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}nav{display:none}main{padding:0}.page{width:8.5in;height:11in;min-height:0;padding:1in;margin:0;box-shadow:none;break-after:page}.page:last-child{break-after:auto}.flow{flex-direction:row}.flow>b{transform:none}.document-note{position:absolute}figure,table,aside{break-inside:avoid}a{color:inherit;text-decoration:none}}
"""


def render(markdown):
    return subprocess.run(["pandoc", "--from=markdown+raw_html", "--to=html5"],
                          input=markdown, text=True, capture_output=True, check=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chrome", type=Path)
    parser.add_argument("--playwright-module", default="playwright")
    args = parser.parse_args()
    abstract = (HERE / "abstract.md").read_text().strip()
    assert len(abstract.split()) == 150, "Keep the draft abstract at 150 words."
    text = (HERE / "paper.md").read_text().replace("<!-- abstract -->", abstract)
    # A Markdown hard break is intentional; avoid whitespace-only diff warnings.
    text = re.sub(r"  \n", "\\\n", text)
    parts = text.split("<!-- page -->")
    assert len(parts) == 7
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "fonts").mkdir(exist_ok=True)
    for font in (ROOT / "report" / "latex" / "fonts").iterdir():
        if font.is_file():
            shutil.copyfile(font, OUT / "fonts" / font.name)
    pages = []
    for i, part in enumerate(parts, 1):
        pages.append(f'<article class="page" id="page-{i}" aria-label="Página {i}">'
                     '<div class="document-note">Maqueta del manuscrito · 13 de septiembre de 2026</div>'
                     '<div class="page-content">'+render(part)+'</div>'
                     f'<footer><span>Helpline · AI Incident Response Sprint · Borrador</span><span>{i} / {len(parts)}</span></footer></article>')
    nav = '<nav aria-label="Versiones del entregable"><strong>HELPLINE · MAQUETA DEL PAPER</strong><a href="paper-draft.pdf">PDF</a><a href="paper.md">Texto editable</a><a href="../wireframe/">Wireframe</a><a href="../paper.pdf">Paper anterior</a><a href="../wireframe/run-today.html">Corridas para hoy</a></nav>'
    page = '<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'+f'<title>{html.escape("Helpline — maqueta del paper")}</title><style>{STYLE}</style></head><body>'+nav+'<main>'+"\n".join(pages)+'</main></body></html>'
    (OUT / "index.html").write_text(page)
    (OUT / "paper.md").write_text(text)
    shutil.copyfile(HERE / "abstract.md", OUT / "abstract.md")
    if args.chrome:
        subprocess.run(["node", str(HERE / "export-pdf.cjs"), str(args.chrome), args.playwright_module], check=True, timeout=60)
    print("Built paper mockup: five main pages, references, appendix; 150-word abstract.")


if __name__ == "__main__":
    main()
