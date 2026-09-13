// Render and check the local wireframe. No external page or model requests.
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require(process.argv[3] || 'playwright');
const output = path.resolve(__dirname, '../../web/wireframe');

(async () => {
  const browser = await chromium.launch({
    executablePath: process.argv[2], headless: true, args: ['--no-sandbox'],
  });
  try {
    const page = await browser.newPage();
    await page.goto(pathToFileURL(path.join(output, 'index.html')).href, { timeout: 15000 });
    await page.emulateMedia({ media: 'print' });
    await page.evaluate(() => document.fonts.ready);
    const pages = await page.locator('.page').evaluateAll(nodes => nodes.map(node => {
      const content = node.children[node.children.length - 2].getBoundingClientRect();
      const footer = node.querySelector('footer').getBoundingClientRect();
      return { fits: content.bottom < footer.top, overflows: node.scrollHeight > node.clientHeight };
    }));
    if (pages.length !== 5 || pages.some(p => !p.fits || p.overflows)) {
      throw new Error(`Wireframe overflow: ${JSON.stringify(pages)}`);
    }
    // PDF annotations must open public documents, not local file:// paths.
    await page.locator('a[href]').evaluateAll(links => {
      const base = 'https://mpodeley.github.io/agent-delegate-sprint-2026/wireframe/';
      for (const link of links) link.href = new URL(link.getAttribute('href'), base).href;
    });
    await page.pdf({ path: path.join(output, 'wireframe.pdf'), preferCSSPageSize: true,
      printBackground: true, timeout: 15000 });
    console.log('PDF: five pages; no content overlaps the footers.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
