const express = require("express");
const httpContext = require("express-http-context");
const puppeteer = require('puppeteer');
const log4js = require('log4js');

// initializing express.js server
const app = express();
const port = 3000;

app.use(httpContext.middleware);

// logging configuration
log4js.configure({
    appenders: {ss: {type: 'file', filename: `screenshotjs.log`}},
    categories: {default: {appenders: ['ss'], level: 'debug'}}
});

const logger = log4js.getLogger('ss');

// parsing hostname from url for using it on file name
function parse_url(url){
    var a = document.createElement("a");
    a.href = url;
    return a.hostname.split(".")[0];
}

// screenshot function
async function ss(url){
    const browser = await puppeteer.launch({defaultViewport: null, args: ['--no-sandbox', '--disable-setuid-sandbox']});
    const page = await browser.newPage();

    logger.debug(`url=${url}`);

    await page.setViewport({width: 1920, height: 1080});
    try {
        await page.goto(url, {waitUntil: 'networkidle0'});
        return await page.screenshot({fullPage: true, type: 'jpeg'});
    } catch (ERR_CERT_COMMON_NAME_INVALID) {
        logger.warn('This URL is not valid!');
    } finally {
        await browser.close();
        logger.debug("Browser has closed!")
    }
};

// html function
async function html(url){
    const browser = await puppeteer.launch({defaultViewport: null, args: ['--no-sandbox', '--disable-setuid-sandbox']});
    const page = await browser.newPage();
    
    logger.info(`url=${url}`);

    await page.setViewport({width: 1920, height: 1080});
    try {
        await page.goto(url, {waitUntil: 'networkidle0'});
        let html = page.evaluate(() => document.documentElement.outerHTML);
        return await html
    } catch (ERR_CERT_COMMON_NAME_INVALID) {
        logger.warn('This URL is not valid!');
    } finally {
        await browser.close();
        logger.debug("Browser has closed!")
    }
};

// rest function for screenshot
app.get(`/jpeg/:url(https?:\/\/?[\da-z\.-]+\.[a-z\.]{2,6}\/?)`, function(req, res){
    logger.debug(`req.params=${req.params}`);
    let bytes = ss(req.params.url);
    bytes.then(function (result) {
        res.send(result);
    })
});

// rest function for html
app.get(`/html/:url(https?:\/\/?[\da-z\.-]+\.[a-z\.]{2,6}\/?)`, function(req, res){
    logger.debug(`req.params=${req.params}`);
    let bytes = html(req.params.url);
    bytes.then(function (result) {
        res.send(result);
    })
});

app.listen(port, () => logger.info(`Example app listening on port ${port}!`));