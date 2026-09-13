// Local PDF rendering and pagination checks for the paper mockup.
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require(process.argv[3] || 'playwright');
const output = path.resolve(__dirname, '../../web/paper-draft');

(async () => {
  const browser = await chromium.launch({executablePath:process.argv[2],headless:true,args:['--no-sandbox']});
  try {
    const page = await browser.newPage();
    await page.goto(pathToFileURL(path.join(output, 'index.html')).href, {timeout:15000});
    await page.emulateMedia({media:'print'});
    await page.evaluate(() => document.fonts.ready);
    const fit = await page.locator('.page').evaluateAll(nodes => nodes.map((node, i) => {
      const content = node.querySelector('.page-content').getBoundingClientRect();
      const footer = node.querySelector('footer').getBoundingClientRect();
      return {page:i+1, clearance:footer.top-content.bottom, overflow:node.scrollHeight>node.clientHeight};
    }));
    console.log(JSON.stringify(fit));
    if (fit.length !== 7 || fit.some(p => p.clearance < 12 || p.overflow)) throw Error('Review paper pagination before publication.');
    await page.locator('a[href]').evaluateAll(links => {
      for (const a of links) a.href = new URL(a.getAttribute('href'), 'https://mpodeley.github.io/agent-delegate-sprint-2026/paper-draft/').href;
    });
    await page.pdf({path:path.join(output,'paper-draft.pdf'),preferCSSPageSize:true,printBackground:true,timeout:15000});
    console.log('PDF exported: seven pages; public links; no footer overlap.');
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error);process.exitCode=1});
