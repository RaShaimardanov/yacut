
import re

from shortuuid import ShortUUID

from settings import Config
from .models import URLMap


def is_valid_short(short):
    return re.match(r'^[a-zA-Z0-9]{1,16}$', short)


def is_short_unique(short):
    return URLMap.query.filter_by(short=short).first()


def get_unique_short_id(length=Config.LENGTH_SHORT_ID):
    while True:
        key = ShortUUID().random(length)
        if not is_short_unique(key):
            break
    return key
