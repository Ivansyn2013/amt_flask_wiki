#from examples.app import app
import os

from examples.app import create_app
import logging
from dotenv import load_dotenv
from flask_wiki.context_processor import inject_quiz_nums_context
#возможно gunicorn не выполняет код ниже, а просто берет app из верхней строчки

load_dotenv()
logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import logging
import traceback
import socket

# Перехватываем все исключения
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, socket.gaierror):
        logging.error("DNS resolution failed (gaierror):")
        logging.error("".join(traceback.format_tb(exc_traceback)))
    else:
        logging.error("Uncaught exception:", exc_info=(exc_type, exc_value, exc_traceback))

import sys
sys.excepthook = handle_exception




if os.getenv("TESTING") == 'True':
    logger.info('Testing True')
    logging.basicConfig(level=logging.DEBUG)
    app = create_app(test_config=True)
else:
    logging.basicConfig(level=logging.INFO)
    logger.info('Testing False')
    app = create_app()



if __name__ == '__main__':
    app.run()
