from examples.app import app
#from examples.app import create_app
import logging
from dotenv import load_dotenv
from flask_wiki.context_processor import inject_quiz_nums_context
#возможно gunicorn не выполняет код ниже, я просто берет app из верхней строчки

if __name__ == '__main__':
    load_dotenv()
    #logging.basicConfig(level=logging.DEBUG)
    #app = create_app()
    app.run()
