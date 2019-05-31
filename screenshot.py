import json
import time

import requests
import tldextract
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] [(%(funcName)s)(%(lineno)d)] %(message)s',
                    datefmt='%Y-%b-%d %H:%M:%S')
logger = logging.getLogger(__name__)

CHROMEDRIVER = 'http://172.17.0.1:4444/wd/hub'


class ScreenShot(object):

    def prepare_browser(self, height=600):
        """Creates a headless webdriver"""
        chrome_options = Options()
        chrome_options.add_argument("headless")
        chrome_options.add_argument(f"--window-size=1920,{height}")
        chrome_options.add_argument("--hide-scrollbars")
        # browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
        logger.info('creating browser..')
        browser = webdriver.Remote(command_executor=CHROMEDRIVER, options=chrome_options)
        logger.info('browser created.')
        return browser

    def get_height_and_width(self, browser, url):
        browser.get(url)
        height = browser.execute_script("return document.documentElement.offsetHeight")
        logger.info(f'height: {height}')
        return height

    def get_file_name(self, browser):
        url = browser.current_url
        splitted_url = tldextract.extract(url)
        domain = splitted_url.domain
        logger.info(f'domain: {domain}')
        return domain + '.png'

    def get_screenshot(self, browser, file_name):
        time.sleep(3)
        browser.save_screenshot(file_name)
        logger.info('screenshot has been saved.')

    def check_hub_status(self):
        try:
            response = requests.get(CHROMEDRIVER + '/status')
            status_json = json.loads(response.text)
            logger.info(f"status_json['value']['ready'] = {status_json['value']['ready'] == 'true'}")
            return status_json['value']['ready']
        except ConnectionError as err:
            logger.warning(f'{err} occurred. Calling the func after one second..')
            time.sleep(1)
            return self.check_hub_status()


if __name__ == '__main__':
    url = 'https://dofo.com'

    inst = ScreenShot()

    while not inst.check_hub_status():
        logger.info('waiting for chromedriver..')
        time.sleep(1)

    browser = inst.prepare_browser()

    try:
        browser.get(url)
        height = inst.get_height_and_width(browser, url)
        browser.quit()
        time.sleep(3)
        browser = inst.prepare_browser(height)
        browser.get(url)
        file_name = inst.get_file_name(browser)
        inst.get_screenshot(browser, file_name)
    finally:
        browser.quit()
