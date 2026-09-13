// Export the working paper with short Apart prompts visible; full prompts remain on the web.
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.argv[3]||'playwright');
const out=path.resolve(__dirname,'../../web/paper-draft-en');
(async()=>{
  const browser=await chromium.launch({executablePath:process.argv[2],headless:true,args:['--no-sandbox']});
  try{
    const page=await browser.newPage();
    await page.goto(pathToFileURL(path.join(out,'index.html')).href,{timeout:15000});
    await page.emulateMedia({media:'print'});
    await page.evaluate(()=>document.fonts.ready);
    const fits=await page.locator('.page').evaluateAll(nodes=>nodes.map((n,i)=>({page:i+1,
      clearance:n.querySelector('footer').getBoundingClientRect().top-n.querySelector('.page-content').getBoundingClientRect().bottom,
      overflow:n.scrollHeight>n.clientHeight})));
    console.log(JSON.stringify(fits));
    if(fits.length!==6||fits.some(p=>p.clearance<12||p.overflow))throw Error('Adjust working-draft pagination before publishing.');
    await page.locator('a[href]').evaluateAll(links=>{for(const a of links)a.href=new URL(a.getAttribute('href'),'https://mpodeley.github.io/agent-delegate-sprint-2026/paper-draft-en/').href});
    await page.pdf({path:path.join(out,'paper-draft.pdf'),preferCSSPageSize:true,printBackground:true,timeout:15000});
    console.log('Exported six-page English PDF; section prompts and original vector figure included.');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
