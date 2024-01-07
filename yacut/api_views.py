from flask import jsonify, request

from yacut.error_handlers import InvalidAPIUsage
from .models import URLMap

from . import app, db


@app.route('/api/id/', methods=['POST'])
def create_id_rec():
    data = request.get_json() or {}

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    original_url = data.get('url')
    custom_id = data.get('custom_id') or URLMap.get_unique_short_id()

    if not original_url:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if not URLMap.is_short_unique(custom_id):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

    if not URLMap.is_valid_short(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    url_map = URLMap(original=original_url, short=custom_id)
    db.session.add(url_map)
    db.session.commit()

    short_url = request.host_url + custom_id

    return jsonify({'url': original_url, 'short_link': short_url}), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is not None:
        return jsonify({'url': url_map.original}), 200
    else:
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)
