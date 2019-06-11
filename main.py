import time
import logging
from screenshot import ScreenShot


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] [(%(funcName)s)(%(lineno)d)] %(message)s',
                    datefmt='%Y-%b-%d %H:%M:%S')
logger = logging.getLogger(__name__)


urls = ['https://dofo.com/', 'https://www.blogger.com/', 'https://www.apple.com/',
        'https://www.adobe.com/', 'https://play.google.com/store', 'https://www.youtube.com/',
        'https://www.microsoft.com/tr-tr/', 'https://wordpress.org/', 'https://www.sahibinden.com/',
        'https://www.mozilla.org/tr/', 'https://www.linkedin.com/', 'https://vimeo.com/',
        'https://creativecommons.org/', 'https://github.com/',
        'https://www.bbc.com/', 'https://vk.com/', 'https://www.amazon.com/', 'https://www.dailymotion.com/tr',
        'https://outlook.live.com/', 'https://www.istockphoto.com/', 'https://medium.com/',
        'https://www.facebook.com/', 'https://www.reuters.com/', 'https://www.dropbox.com/', 'https://www.uol.com.br/',
        'https://www.paypal.com/tr/home', 'https://www.nytimes.com/']


urls = ['https://dofo.com/', 'https://www.apple.com/', 'https://www.blogger.com/', 'https://www.dailymotion.com/tr',
        'https://medium.com/', 'https://vimeo.com/', 'https://vk.com/', 'https://www.youtube.com/']

if __name__ == '__main__':
    start = time.time()
    ScreenShot().main(urls)
    logger.info(f'TIMELAPSE: {time.time()-start:.2f}')