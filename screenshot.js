const puppeteer = require('puppeteer');
const log4js = require('log4js');

log4js.configure({
    appenders: {ss: { type: 'file', filename: `screenshotjs.log` } },
    categories: { default: { appenders: ['ss'], level: 'debug' } }
});

const logger = log4js.getLogger('ss');

(async () => {
    const browser = await puppeteer.launch({defaultViewport: null});
    const page = await browser.newPage();

    let argv = require('minimist')(process.argv.slice(2));
    let queryUrl = argv['url'];
    let fileName = argv['filename'];

    logger.info("URL: ", queryUrl);
    logger.debug("File Name: ", fileName);

    await page.setViewport({width: 1920, height: 1080});
    try {
        await page.goto(queryUrl, {waitUntil: 'networkidle0'});
        await page.screenshot({path: fileName, fullPage: true});
        logger.info("Screenshot has saved!")
    } catch (ERR_CERT_COMMON_NAME_INVALID) {
        logger.warn('This URL is not valid!');
    } finally {
        await browser.close();
        logger.debug("Browser has closed!")
    }
})();