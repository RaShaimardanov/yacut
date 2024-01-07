from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError

from yacut.models import URLMap


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 128)
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16),
            Regexp(
                r'^[a-zA-Z0-9]{1,16}$',
                message='Указано недопустимое имя для короткой ссылки'
            ),
            Optional()
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, custom_id):
        if custom_id.data and not URLMap.is_short_unique(custom_id.data):
            raise ValidationError('Предложенный вариант короткой ссылки уже существует.')
