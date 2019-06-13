const puppeteer = require('puppeteer');
const log4js = require('log4js');
const fs = require('fs');
const readline = require('readline');

// I/O variables
const inputFile = 'domains.txt';
const outputDir = 'output';

// Logging variables
const logFile = 'app.log';
const logLevel = 'info';


log4js.configure({
    appenders: {ss: {type: 'file', filename: logFile}},
    categories: {default: {appenders: ['ss'], level: logLevel}}
});

const logger = log4js.getLogger('ss');

async function* processLineByLine() {
    const fileStream = fs.createReadStream(inputFile);
  
    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity
    });
    // Note: we use the crlfDelay option to recognize all instances of CR LF
    // ('\r\n') in input.txt as a single line break.
  
    for await (const line of rl) {
      // Each line in input.txt will be successively available here as `line`.
      // console.log(`Line from file: ${line}`);
      yield line;
    }
  }  

(async () => {
    for await (const domain of processLineByLine()) {
        const browser = await puppeteer.launch({defaultViewport: null, args: ['--no-sandbox', '--disable-setuid-sandbox']});
        const page = await browser.newPage();

        let queryUrl = 'https://www.' + domain;
        let fileName = domain + '.png';
        let filePath = outputDir + '/' + fileName;

        // Check for output directory, create if does not exist.
        if (!fs.existsSync(outputDir)){
            fs.mkdirSync(outputDir);
        }

        logger.info("URL: ", queryUrl);
        logger.debug("File Name: ", fileName);

        await page.setViewport({width: 1920, height: 1080});
        try {
            await page.goto(queryUrl, {waitUntil: 'networkidle0'});
            await page.screenshot({ path: filePath, fullPage: true });
            logger.info("Screenshot has saved!");
        } catch (ERR_CERT_COMMON_NAME_INVALID) {
            logger.warn('This URL is not valid!');
        } finally {
            await browser.close();
            logger.debug("Browser has closed!")
        }
    }
})();
