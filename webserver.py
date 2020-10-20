import argparse
import asyncio
import logging
import os
import warnings
import sys

from aiohttp.web import Application, AppRunner, TCPSite
from aiohttp_jinja2 import setup as jinja_setup
from jinja2 import FileSystemLoader

import website

# Set up loggers
logging.basicConfig(format='%(asctime)s:%(name)s:%(levelname)s: %(message)s', stream=sys.stdout)
logger = logging.getLogger(os.getcwd().split(os.sep)[-1].split()[-1].lower())
logger.setLevel(logging.INFO)

# Filter warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("config_file", help="The configuration for the webserver.")
parser.add_argument("--host", type=str, default='0.0.0.0', help="The host IP to run the webserver on.")
parser.add_argument("--port", type=int, default=8080, help="The port to run the webserver on.")
args = parser.parse_args()

# Create website object - don't start based on argv
app = Application(loop=asyncio.get_event_loop())
app['static_root_url'] = '/static'
app.router.add_routes(website.routes)
app.router.add_static('/static', os.getcwd() + '/website/static', append_version=True)

jinja_setup(app, loader=FileSystemLoader(os.getcwd() + '/website/templates'))

# Add our loggers
app['logger'] = logger.getChild("route")


if __name__ == '__main__':
    """Starts the webserver and runs forever"""

    loop = app.loop

    # HTTP server
    logger.info("Creating webserver...")
    application = AppRunner(app)
    loop.run_until_complete(application.setup())
    webserver = TCPSite(application, host=args.host, port=args.port)

    # Start server
    loop.run_until_complete(webserver.start())
    logger.info(f"Server started - http://{args.host}:{args.port}/")

    # This is the forever loop
    try:
        logger.info("Running webserver")
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Clean up our shit
    logger.info("Closing webserver")
    loop.run_until_complete(application.cleanup())
    logger.info("Closing asyncio loop")
    loop.close()
