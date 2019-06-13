import click
from call_js import *

logger = logging.getLogger(__name__)


@click.command()
@click.option('--outputdir', default='output', help='Output directory.')
@click.option('--domainfile', default='domains.txt', help='Domain file.')
def cli(outputdir, domainfile):
    with open(domainfile) as f:
        for line in f:
            # Creating required variables
            domain = line.strip('\n')
            url = CallJS.url_from_domain(domain)
            filename = CallJS.create_filename(domain)
            filepath = CallJS.get_filepath(filename, outputdir)

            # Calling node.js for screen shot
            CallJS.call_puppeteer(url, filepath)

            # Checking for hanging Chromium instances
            pid_list = CallJS.get_pid('chromium')
            CallJS.kill_process(pid_list)


if __name__ == '__main__':
    cli()
