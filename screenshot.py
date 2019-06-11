import json
import time
import os
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
        chrome_options = Options()
        chrome_options.add_argument("headless")
        chrome_options.add_argument(f"--window-size=1920,{height}")
        chrome_options.add_argument("--hide-scrollbars")
        logger.debug(f'chrome_options: {chrome_options.arguments}')
        logger.info('initializing browser instance..')
        browser = webdriver.Remote(command_executor=CHROMEDRIVER, options=chrome_options)
        return browser

    def get_height(self, browser, url):
        browser.get(url)
        query_list = ['document.body.scrollHeight', 'document.documentElement.scrollHeight',
                      'document.body.offsetHeight', 'document.documentElement.offsetHeight',
                      'document.body.clientHeight', 'document.documentElement.clientHeight']
        last_height = browser.execute_script(f'return Math.max( {", ".join(query_list)} );')
        while True:
            browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            # browser.implicitly_wait(1)
            time.sleep(2)
            new_height = browser.execute_script(f'return document.documentElement.scrollHeight;')
            logger.debug(f'last_height: {last_height}')
            logger.debug(f'new_height: {new_height}')
            if new_height == last_height:
                break
            last_height = new_height
        logger.info(f'height: {last_height}')
        return last_height

    def get_file_name(self, browser):
        url = browser.current_url
        splitted_url = tldextract.extract(url)
        domain = splitted_url.domain
        return domain + '.png'

    def get_screenshot(self, browser, file_name):
        if not os.path.exists('output'):
            os.makedirs('output')
        time.sleep(10)
        browser.save_screenshot(os.path.join('output', file_name))
        logger.info('screenshot has been saved.')

    def check_hub_status(self):
        try:
            response = requests.get(CHROMEDRIVER + '/status')
            status_json = json.loads(response.text)
            logger.debug(f"status_json['value']['ready'] = {status_json['value']['ready'] == 'true'}")
            return status_json['value']['ready']
        except requests.exceptions.ConnectionError as err:
            logger.warning(f'{err} occurred. Calling the func after one second..')
            time.sleep(.5)
            return self.check_hub_status()

    def main(self, url):
        url_list = url
        if type(url_list) != list:
            url_list = [url]

        while not self.check_hub_status():
            time.sleep(.1)

        for url in url_list:
            start = time.time()
            browser = self.prepare_browser()
            try:
                logger.info(url)
                browser.get(url)
                height = self.get_height(browser, url)
                browser.quit()
                browser = self.prepare_browser(height)
                browser.get(url)
                file_name = self.get_file_name(browser)
                self.get_screenshot(browser, file_name)
            finally:
                browser.quit()
                logger.info(f'timelapse: {time.time() - start:.2f}s')
