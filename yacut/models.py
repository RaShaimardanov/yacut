import re
from datetime import datetime

import shortuuid

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.short,
        )

    @staticmethod
    def is_valid_short(short):
        return re.match(r'^[a-zA-Z0-9]{1,16}$', short)

    @staticmethod
    def is_short_unique(short):
        return URLMap.query.filter_by(short=short).first() is None

    @classmethod
    def get_unique_short_id(cls):
        while True:
            key = shortuuid.ShortUUID().random(length=6)
            if cls.is_short_unique(key):
                break
        return key
