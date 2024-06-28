from examples.app import create_app
import logging
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)
    app = create_app()
    app.run()
