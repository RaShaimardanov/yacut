from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError

from settings import Config
from .utils import is_short_unique


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(
                Config.MIN_ORIGINAL_LINK_LENGTH,
                Config.MAX_ORIGINAL_LINK_LENGTH
            )
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(
                Config.MIN_CUSTOM_ID_LENGTH,
                Config.MAX_CUSTOM_ID_LENGTH
            ),
            Regexp(
                r'^[a-zA-Z0-9]{1,16}$',
                message='Указано недопустимое имя для короткой ссылки'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, custom_id):
        if custom_id.data and is_short_unique(custom_id.data):
            raise ValidationError('Предложенный вариант короткой ссылки уже существует.')
