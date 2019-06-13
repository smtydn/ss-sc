import os
import signal
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='calljs.log',
                    filemode='w',
                    format='[%(asctime)s] [%(levelname)s] [(%(funcName)s)(%(lineno)d)] %(message)s',
                    datefmt='%Y-%b-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class CallJS(object):

    @classmethod
    def url_from_domain(cls, domain):
        url = 'https://www.' + domain
        logger.debug(f"URL: {url}")
        return url

    @classmethod
    def create_filename(cls, domain):
        host = domain.split('.')[0]
        filename = host + '.png'
        logger.debug(f"Filename: {filename}")
        return filename

    @classmethod
    def get_filepath(cls, filename, output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
            logger.debug("Output directory did not exist. It is now created!")
        return os.path.join(output_dir, filename)

    @classmethod
    def call_puppeteer(cls, url, filepath):
        try:
            process = subprocess.Popen(['node', 'screenshot.js', f'--url={url}', f'--filename={filepath}'])
            process.wait(10)
            logger.info(f'{url}\'s screen shot has taken with no problem!')
        except subprocess.TimeoutExpired as err:
            logger.warning(f"{err}!")

    @classmethod
    def get_pid(cls, name):
        try:
            result = subprocess.check_output(["pidof", name])
            pid_list = list(map(int, result.split()))
            logger.debug(f'PID List: {pid_list}')
            return pid_list
        except subprocess.CalledProcessError:
            logger.debug(f"There's no process exist that includes '{name}' in its name!")
            return list()

    @classmethod
    def kill_process(cls, pid_list):
        for pid in pid_list:
            os.kill(pid, signal.SIGTERM)
            logger.debug(f"Process {pid} has terminated!")