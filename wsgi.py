from examples.app import app
from db.db_config import Develop, Deploy
import logging
from dotenv import load_dotenv
import os


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    app.run()
