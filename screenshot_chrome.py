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


class ScreenShotChrome(object):

    @classmethod
    def prepare_browser(cls, height=600):
        opt = Options()
        opt.add_argument("headless")
        opt.add_argument(f"--window-size=1920,{height}")
        opt.add_argument("--hide-scrollbars")
        logger.debug(f'chrome_options: {opt.arguments}')
        logger.info('initializing browser instance..')
        driver = webdriver.Remote(command_executor=CHROMEDRIVER, options=opt)
        return driver

    @classmethod
    def get_height(cls, driver, url):
        driver.get(url)
        query_list = ['document.body.scrollHeight', 'document.documentElement.scrollHeight',
                      'document.body.offsetHeight', 'document.documentElement.offsetHeight',
                      'document.body.clientHeight', 'document.documentElement.clientHeight']
        last_height = driver.execute_script(f'return Math.max( {", ".join(query_list)} );')
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script(f'return document.documentElement.scrollHeight;')
            logger.debug(f'last_height: {last_height}')
            logger.debug(f'new_height: {new_height}')
            if new_height == last_height:
                break
            last_height = new_height
        logger.info(f'height: {last_height}')
        return last_height

    @classmethod
    def get_file_name(cls, driver):
        url = driver.current_url
        url_part = tldextract.extract(url)
        domain = url_part.domain
        return domain + '.png'

    @classmethod
    def get_screenshot(cls, browser, file_name):
        if not os.path.exists('output'):
            os.makedirs('output')
        time.sleep(3)
        browser.save_screenshot(os.path.join('output', file_name))
        logger.info('screenshot has been saved.')

    @classmethod
    def check_hub_status(cls):
        try:
            response = requests.get(CHROMEDRIVER + '/status')
            status_json = json.loads(response.text)
            logger.debug(f"status_json['value']['ready'] = {status_json['value']['ready'] == 'true'}")
            return status_json['value']['ready']
        except requests.exceptions.ConnectionError as err:
            logger.warning(f'{err} occurred. Calling the func after one second..')
            time.sleep(.5)
            return cls.check_hub_status()
