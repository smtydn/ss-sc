import time
import logging
from screenshot_chrome import ScreenShotChrome


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] [(%(funcName)s)(%(lineno)d)] %(message)s',
                    datefmt='%Y-%b-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def gen_url():
    with open('domains.txt') as f:
        for url in f:
            url = url.strip('\n')
            yield 'https://www.' + url + '/'


if __name__ == '__main__':
    start = time.time()

    while not ScreenShotChrome.check_hub_status():
        time.sleep(.1)

    for url in gen_url():
        url_start = time.time()
        driver = ScreenShotChrome.prepare_browser()
        try:
            logger.info(url)
            driver.get(url)
            height = ScreenShotChrome.get_height(driver, url)
            driver.quit()
            driver = ScreenShotChrome.prepare_browser(height)
            driver.get(url)

            file_name = ScreenShotChrome.get_file_name(driver)
            ScreenShotChrome.get_screenshot(driver, file_name)
        finally:
            driver.quit()

    logger.info(f'TIMELAPSE: {time.time()-start:.2f}')