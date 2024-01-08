from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .utils import get_unique_short_id, is_short_unique, is_valid_short


@app.route('/api/id/', methods=['POST'])
def create_id_rec():
    data = request.get_json() or {}

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    original_url = data.get('url')
    custom_id = data.get('custom_id') or get_unique_short_id()

    if not original_url:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if is_short_unique(custom_id):
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

    if not is_valid_short(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    url_map = URLMap(original=original_url, short=custom_id)
    db.session.add(url_map)
    db.session.commit()

    short_url = request.host_url + custom_id

    return jsonify({'url': original_url, 'short_link': short_url}), HTTPStatus.CREATED


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = is_short_unique(short)
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
