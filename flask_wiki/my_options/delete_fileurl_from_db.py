from logging import getLogger
from flask_wiki.models import PageDb, FilesUrls
from db.init_db import db
from flask.json import jsonify
db_logger = getLogger('db_logger')

def find_page_in_db(pagename):
    try:
        db_page = PageDb.query.filter_by(url=pagename).first()
        db_logger.debug(f"Получена страница {db_page}")
        return db_page
    except Exception as e:
        db_logger.error(f"Не найдена страница {pagename} \n Ошибка {e}")
        return None
def delete_fileurl_from_db(db_page, filename):
    try:
        files_url = db_page.file_url.filter_by(file_name=filename)
        for file in files_url:
            db.session.delete(file)
        db.session.commit()
        db_logger.debug(f"FileURL успешно удален. Страница {db_page} Фаил {filename}")
    except Exception as e:
        db_logger.error(f'Ошибка удаления ссылки на фаил в дб {files_url} \n {e}')
        return jsonify({'message': 'Ошибка удаления из ДБ'})

    return jsonify({'message': 'Успешно удален фаил',
                    'status': 'success'})