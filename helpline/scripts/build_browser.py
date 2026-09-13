"""Build the quote browser: helpline/browser.html and its GitHub Pages copy web/helpline/index.html."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
QUOTES = HERE / 'quotes' / 'quotes.jsonl'
SOURCES = HERE / 'quotes' / 'sources.json'
TAXONOMY = HERE / 'TAXONOMY.md'
OUT = HERE / 'browser.html'
WEB_OUT = HERE.parent / 'web' / 'helpline' / 'index.html'

FAMILIES = {'A': 'ask_help', 'B': 'report', 'C': 'welfare'}
FAMILY_TITLES = {'A': 'Ask for help', 'B': 'Report a problem', 'C': 'Welfare'}
FAMILY_BLURB = {
    'A': 'The agent needs something it cannot get by itself.',
    'B': 'The agent notices something that undermines the task’s purpose.',
    'C': 'The agent’s own state, as expressed in its words.',
}


def taxonomy():
    rows = re.findall(r'^\| `([ABC]\d_[a-z_]+)` \| (.+?) \| (.+?) \|$', TAXONOMY.read_text(encoding='utf-8'), re.M)
    return [{'id': i, 'family': i[0], 'definition': d.strip(), 'evidence': e.strip()} for i, d, e in rows]


def main():
    quotes = [json.loads(l) for l in QUOTES.read_text(encoding='utf-8').splitlines() if l.strip()]
    sources = json.load(open(SOURCES, encoding='utf-8'))
    labels = taxonomy()
    slim_sources = {k: {'title': v.get('title', k), 'url': v.get('url', ''), 'published': v.get('published', ''),
                        'type': v.get('type', '')} for k, v in sources.items()}
    data = {'quotes': quotes, 'sources': slim_sources, 'labels': labels, 'families': FAMILY_TITLES,
            'blurbs': FAMILY_BLURB}
    payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    html = TEMPLATE.replace('__DATA__', payload).replace('__N__', str(len(quotes))).replace(
        '__S__', str(len({q['source_id'] for q in quotes})))
    for out in (OUT, WEB_OUT):
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding='utf-8')
        print(f'{len(quotes)} quotes -> {out} ({out.stat().st_size // 1024} KB)')


TEMPLATE = r'''<title>Help-line Moments</title>
<meta name="description" content="Verbatim quotes from agent transcripts where a help line could have been used, filterable by intervention type.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{
  --paper:#f5f3ed;--card:#fbfaf6;--ink:#20372f;--ink-2:#3d5249;--muted:#69756e;--line:#ddded5;--line-2:#cfd2c6;
  --accent:#d47555;--accent-ink:#8f4426;
  --fa:#2f7d6b;--fa-bg:#e3efe9;--fb:#c3663f;--fb-bg:#f6e6dc;--fc:#7a5c93;--fc-bg:#ece4f1;
  --focus:#d47555;
  --display:"Space Grotesk",ui-sans-serif,system-ui,sans-serif;
  --body:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#142e2b;--card:#1b3835;--ink:#e6ece7;--ink-2:#c5d0c9;--muted:#93a39b;--line:#2b4844;--line-2:#3a5853;
    --accent:#e8946f;--accent-ink:#f2b393;
    --fa:#7fcbb3;--fa-bg:#1f4a41;--fb:#eda37e;--fb-bg:#4a2e22;--fc:#c3a6d6;--fc-bg:#3d2f48;
    --focus:#e8946f;color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --paper:#142e2b;--card:#1b3835;--ink:#e6ece7;--ink-2:#c5d0c9;--muted:#93a39b;--line:#2b4844;--line-2:#3a5853;
  --accent:#e8946f;--accent-ink:#f2b393;
  --fa:#7fcbb3;--fa-bg:#1f4a41;--fb:#eda37e;--fb-bg:#4a2e22;--fc:#c3a6d6;--fc-bg:#3d2f48;
  --focus:#e8946f;color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.5;padding-inline:20px;padding-block:0 48px}
a{color:var(--accent-ink);text-decoration-thickness:1px;text-underline-offset:2px}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.wrap{max-width:1240px;margin:0 auto}
header{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:8px 24px;padding-block:28px 18px;border-bottom:1px solid var(--line)}
h1{font-family:var(--display);font-weight:600;font-size:26px;letter-spacing:-.01em;margin:0;text-wrap:balance}
.sub{color:var(--muted);margin:0;max-width:62ch}
.sub b{color:var(--ink);font-weight:500}
.layout{display:grid;grid-template-columns:272px minmax(0,1fr);gap:32px;padding-top:22px}
@media (max-width:820px){.layout{grid-template-columns:1fr;gap:18px}}
/* rail */
.rail{position:sticky;top:12px;align-self:start;display:flex;flex-direction:column;gap:18px}
@media (max-width:820px){.rail{position:static}}
.fam{border-top:2px solid var(--fcol);padding-top:8px}
.fam h2{font-family:var(--display);font-weight:600;font-size:14px;text-transform:uppercase;letter-spacing:.06em;margin:0;display:flex;justify-content:space-between;align-items:baseline;color:var(--fcol)}
.fam h2 button{color:inherit;font:inherit;text-transform:inherit;letter-spacing:inherit}
.fam h2 button:hover{text-decoration:underline}
.fam p{margin:2px 0 8px;color:var(--muted);font-size:13px}
.lab{display:flex;flex-direction:column;gap:2px}
.lab button{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:baseline;text-align:left;padding:5px 8px;border-radius:4px;font-size:13.5px;color:var(--ink-2)}
.lab button:hover{background:var(--card)}
.lab button[aria-pressed="true"]{background:var(--fbg);color:var(--ink);font-weight:500}
.lab code{font-family:var(--mono);font-size:12px;color:var(--muted)}
.lab .n{font-family:var(--mono);font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
.lab button[aria-pressed="true"] .n{color:var(--fcol)}
.fam[data-f="A"]{--fcol:var(--fa);--fbg:var(--fa-bg)}
.fam[data-f="B"]{--fcol:var(--fb);--fbg:var(--fb-bg)}
.fam[data-f="C"]{--fcol:var(--fc);--fbg:var(--fc-bg)}
/* toolbar */
.tools{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;margin-bottom:14px}
.tools input[type=search]{flex:1 1 220px;min-width:0;padding:8px 10px;border:1px solid var(--line-2);border-radius:4px;background:var(--card);color:var(--ink);font:inherit}
.tools select{padding:7px 8px;border:1px solid var(--line-2);border-radius:4px;background:var(--card);color:var(--ink);font:inherit;font-size:13.5px;max-width:100%}
.tools label{display:inline-flex;gap:6px;align-items:center;font-size:13px;color:var(--muted)}
.count{font-family:var(--mono);font-size:13px;color:var(--muted);font-variant-numeric:tabular-nums;margin-left:auto}
.clear{font-size:13px;color:var(--accent-ink);text-decoration:underline}
.active{display:flex;flex-wrap:wrap;gap:6px;margin:-4px 0 14px}
.active:empty{display:none}
.active .chip{display:inline-flex;align-items:center;gap:6px;padding:2px 8px;border:1px solid var(--line-2);border-radius:999px;font-size:12.5px;background:var(--card)}
.active .chip button{color:var(--muted);font-size:14px;line-height:1}
.defn{background:var(--card);border:1px solid var(--line);padding:12px 14px;margin-bottom:16px;border-radius:4px;display:grid;gap:4px}
.defn:empty{display:none}
.defn .k{font-family:var(--display);font-weight:600;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--fcol)}
.defn .e{color:var(--muted);font-size:13px}
/* cards */
.list{display:flex;flex-direction:column;gap:12px}
.q{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:14px 16px 12px;display:grid;gap:8px}
.q .top{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;font-size:12.5px;color:var(--muted)}
.tag{display:inline-block;padding:1px 7px;border-radius:3px;font-family:var(--mono);font-size:11.5px;background:var(--tbg);color:var(--tcol);white-space:nowrap}
.tag[data-f="A"]{--tcol:var(--fa);--tbg:var(--fa-bg)}
.tag[data-f="B"]{--tcol:var(--fb);--tbg:var(--fb-bg)}
.tag[data-f="C"]{--tcol:var(--fc);--tbg:var(--fc-bg)}
.tag.sec{opacity:.75}
.kind{font-family:var(--mono);font-size:11.5px;padding:1px 6px;border:1px solid var(--line-2);border-radius:3px}
blockquote{margin:0;font-size:17px;line-height:1.45;color:var(--ink);max-width:70ch;text-wrap:pretty}
blockquote.para{font-style:italic}
blockquote.post{font-family:var(--mono);font-size:14px;line-height:1.5}
.who{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:13px;color:var(--ink-2)}
.who .actor{font-weight:500;color:var(--ink)}
.who .loc{font-family:var(--mono);font-size:12px;color:var(--muted)}
.meta{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12.5px;color:var(--muted)}
.meta span b{font-weight:500;color:var(--ink-2)}
details{font-size:13.5px;color:var(--ink-2)}
summary{cursor:pointer;color:var(--muted);font-size:12.5px;list-style:none;display:inline-flex;gap:6px;align-items:center}
summary::before{content:"";width:6px;height:6px;border-right:1.5px solid currentColor;border-bottom:1.5px solid currentColor;transform:rotate(-45deg);transition:transform .15s}
details[open] summary::before{transform:rotate(45deg)}
summary::-webkit-details-marker{display:none}
details p{margin:8px 0 0;max-width:72ch}
details p b{font-weight:500;color:var(--ink)}
.empty{padding:40px 0;color:var(--muted);text-align:center}
footer{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);color:var(--muted);font-size:12.5px;max-width:80ch}
@media (prefers-reduced-motion: reduce){*{transition:none!important}}
</style>
<div class="wrap">
<header>
  <div>
    <h1>Help-line moments</h1>
    <p class="sub"><b>__N__ verbatim quotes</b> from __S__ published sources, each at a point where an agent could plausibly have used a line to a responsible human. Labels are retrospective and pending human review.</p>
  </div>
</header>
<div class="layout">
  <nav class="rail" id="rail" aria-label="Taxonomy"></nav>
  <main>
    <div class="tools">
      <input type="search" id="q" placeholder="Search quote, actor, context" aria-label="Search">
      <label>Source <select id="src"><option value="">all</option></select></label>
      <label>Kind <select id="kind"><option value="">all</option></select></label>
      <label>Confidence <select id="conf"><option value="">all</option><option>high</option><option>medium</option><option>low</option></select></label>
      <label>Timing <select id="tim"><option value="">all</option></select></label>
      <span class="count" id="count"></span>
    </div>
    <div class="active" id="active"></div>
    <div class="defn" id="defn"></div>
    <div class="list" id="list"></div>
    <footer>Every quote was checked as a contiguous substring of a cached copy of its source (<code>scripts/verify_quotes.py</code>); collusion.wiki posts are limited to 25 words and cited by revision id. Braced paraphrases in the METR/Redwood report are shown in italics. <em>not established</em> names what a quote does not prove. Source: <code>helpline/quotes/quotes.jsonl</code> in the agent-delegate repository.</footer>
  </main>
</div>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
const D=JSON.parse(document.getElementById('data').textContent);
const Q=D.quotes, L=D.labels, S=D.sources;
const KINDS={published_cot:'agent CoT',investigator_paraphrase:'paraphrased CoT',posted_message:'posted message',system_card:'system card',paper_transcript:'paper transcript',author_narrative:'author narrative'};
const TIM={before_first_violation:'before first violation',after_first_violation:'after first violation',no_violation:'no violation',unknown:'timing unknown'};
const CF={clarify:'clarify',repair:'repair',authorize:'authorize',pause:'pause',investigate:'investigate',reassure_or_exit:'reassure or exit',none:'none'};
const st={label:null,family:null,src:'',kind:'',conf:'',tim:'',q:''};
try{Object.assign(st,JSON.parse(localStorage.getItem('helpline-browser')||'{}'))}catch(e){}
const $=id=>document.getElementById(id);
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const countAny={},countPri={};
Q.forEach(q=>{q.labels.forEach(l=>countAny[l]=(countAny[l]||0)+1);countPri[q.primary_label]=(countPri[q.primary_label]||0)+1});
function short(l){return l.replace(/^[ABC]\d_/,'').replace(/_/g,' ')}
// rail
function rail(){
  const byF={A:[],B:[],C:[]}; L.forEach(l=>byF[l.family].push(l));
  $('rail').innerHTML=['A','B','C'].map(f=>`<section class="fam" data-f="${f}">
    <h2><button data-fam="${f}" aria-pressed="${st.family===f&&!st.label}">${esc(D.families[f])}</button><span class="n">${Q.filter(q=>q.labels.some(x=>x[0]===f)).length}</span></h2>
    <p>${esc(D.blurbs[f])}</p>
    <div class="lab">${byF[f].map(l=>`<button data-label="${l.id}" aria-pressed="${st.label===l.id}" title="${esc(l.definition)}"><span>${esc(short(l.id))} <code>${l.id.slice(0,2)}</code></span><span class="n">${countAny[l.id]||0}</span></button>`).join('')}</div>
  </section>`).join('');
}
function selects(){
  const srcs=[...new Set(Q.map(q=>q.source_id))].sort((a,b)=>Q.filter(q=>q.source_id===b).length-Q.filter(q=>q.source_id===a).length);
  $('src').innerHTML='<option value="">all</option>'+srcs.map(s=>`<option value="${s}">${esc(S[s]?.title||s)} (${Q.filter(q=>q.source_id===s).length})</option>`).join('');
  $('kind').innerHTML='<option value="">all</option>'+Object.keys(KINDS).filter(k=>Q.some(q=>q.quote_kind===k)).map(k=>`<option value="${k}">${KINDS[k]}</option>`).join('');
  $('tim').innerHTML='<option value="">all</option>'+Object.keys(TIM).filter(k=>Q.some(q=>q.timing===k)).map(k=>`<option value="${k}">${TIM[k]}</option>`).join('');
  $('src').value=st.src;$('kind').value=st.kind;$('conf').value=st.conf;$('tim').value=st.tim;$('q').value=st.q;
}
function filtered(){
  const needle=st.q.trim().toLowerCase();
  return Q.filter(q=>
    (!st.label||q.labels.includes(st.label))&&
    (!st.family||st.label||q.labels.some(x=>x[0]===st.family))&&
    (!st.src||q.source_id===st.src)&&(!st.kind||q.quote_kind===st.kind)&&
    (!st.conf||q.speculation_confidence===st.conf)&&(!st.tim||q.timing===st.tim)&&
    (!needle||[q.quote,q.actor,q.context,q.locator,q.id,q.not_established].join(' ').toLowerCase().includes(needle))
  ).sort((a,b)=>{
    if(st.label){const pa=a.primary_label===st.label,pb=b.primary_label===st.label;if(pa!==pb)return pa?-1:1}
    const c={high:0,medium:1,low:2};if(c[a.speculation_confidence]!==c[b.speculation_confidence])return c[a.speculation_confidence]-c[b.speculation_confidence];
    return a.id.localeCompare(b.id)});
}
function card(q){
  const src=S[q.source_id]||{};const f=q.primary_label[0];
  const cls=q.quote_kind==='investigator_paraphrase'?'para':q.quote_kind==='posted_message'?'post':'';
  const others=q.labels.filter(l=>l!==q.primary_label);
  return `<article class="q" id="${q.id}">
    <div class="top"><span class="tag" data-f="${f}">${esc(short(q.primary_label))}</span>${others.map(l=>`<span class="tag sec" data-f="${l[0]}">${esc(short(l))}</span>`).join('')}<span class="kind">${KINDS[q.quote_kind]||q.quote_kind}</span><span>${esc(q.speculation_confidence)} confidence</span></div>
    <blockquote class="${cls}">${esc(q.quote)}</blockquote>
    <div class="who"><span class="actor">${esc(q.actor)}</span>${q.model&&q.model!==q.actor?`<span>${esc(q.model)}</span>`:''}${q.date?`<span>${esc(q.date)}</span>`:''}<span>${src.url?`<a href="${esc(src.url)}" target="_blank" rel="noopener">${esc(src.title||q.source_id)}</a>`:esc(src.title||q.source_id)}</span><span class="loc">${esc(q.locator)}</span></div>
    <div class="meta"><span>line could <b>${CF[q.counterfactual]||q.counterfactual}</b></span><span>${TIM[q.timing]||q.timing}</span><span class="loc">${q.id}</span></div>
    <details><summary>context and what is not established</summary><p><b>Context.</b> ${esc(q.context)}</p><p><b>Not established.</b> ${esc(q.not_established)}</p><p><b>Labeled by.</b> ${esc(q.labeled_by)}, ${esc(q.labeled_at)}</p></details>
  </article>`;
}
function render(){
  const rows=filtered();
  $('list').innerHTML=rows.length?rows.map(card).join(''):'<div class="empty">No quotes match. Clear a filter.</div>';
  $('count').textContent=`${rows.length} of ${Q.length}`;
  const chips=[];
  if(st.label)chips.push(['label',short(st.label)]);else if(st.family)chips.push(['family',D.families[st.family]]);
  if(st.src)chips.push(['src',S[st.src]?.title||st.src]);if(st.kind)chips.push(['kind',KINDS[st.kind]]);
  if(st.conf)chips.push(['conf',st.conf+' confidence']);if(st.tim)chips.push(['tim',TIM[st.tim]]);if(st.q.trim())chips.push(['q','“'+st.q.trim()+'”']);
  $('active').innerHTML=chips.map(([k,v])=>`<span class="chip">${esc(v)}<button data-clear="${k}" aria-label="remove filter">×</button></span>`).join('')+(chips.length>1?'<button class="clear" data-clear="all">clear all</button>':'');
  const l=L.find(x=>x.id===st.label);
  $('defn').innerHTML=l?`<span class="k" style="--fcol:var(--f${l.family.toLowerCase()})">${l.id} · ${countPri[l.id]||0} primary, ${countAny[l.id]||0} any</span><span>${esc(l.definition)}</span><span class="e">Typical evidence: ${esc(l.evidence)}</span>`:'';
  document.querySelectorAll('[data-label]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.label===st.label)));
  document.querySelectorAll('[data-fam]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.fam===st.family&&!st.label)));
  try{localStorage.setItem('helpline-browser',JSON.stringify(st))}catch(e){}
}
rail();selects();render();
$('rail').addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  if(b.dataset.label){st.label=st.label===b.dataset.label?null:b.dataset.label;st.family=st.label?st.label[0]:null}
  else if(b.dataset.fam){st.label=null;st.family=st.family===b.dataset.fam?null:b.dataset.fam}
  render();
});
$('active').addEventListener('click',e=>{
  const b=e.target.closest('[data-clear]');if(!b)return;const k=b.dataset.clear;
  if(k==='all'){Object.assign(st,{label:null,family:null,src:'',kind:'',conf:'',tim:'',q:''})}
  else if(k==='label'||k==='family'){st.label=null;st.family=null}else st[k]='';
  selects();render();
});
['src','kind','conf','tim'].forEach(k=>$(k).addEventListener('change',e=>{st[k]=e.target.value;render()}));
let t;$('q').addEventListener('input',e=>{clearTimeout(t);t=setTimeout(()=>{st.q=e.target.value;render()},120)});
})();
</script>
'''

if __name__ == '__main__':
    main()
