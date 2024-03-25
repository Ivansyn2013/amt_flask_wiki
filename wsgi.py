from examples.app import app
from db.db_config import Develop, Deploy
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run()
    print(app.config)
