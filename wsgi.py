from examples.app import create_app
import logging
from dotenv import load_dotenv
from flask_wiki.context_processor import inject_quiz_nums_context


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)
    app = create_app(test_config='test_mode')
    app.context_processor(inject_quiz_nums_context)
    app.run()
