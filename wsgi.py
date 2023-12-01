from examples.app import app
from db.db_config import Develop, Deploy

if __name__ == '__main__':
    app.config.from_object(Deploy)
    app.run()