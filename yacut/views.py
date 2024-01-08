from http import HTTPStatus

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .models import URLMap
from .forms import URLMapForm
from .utils import get_unique_short_id, is_short_unique


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()
        url_map = URLMap(original=form.original_link.data, short=short)
        db.session.add(url_map)
        db.session.commit()
        link = url_for("urlmap_view", short=short, _external=True)
        flash(f'Ваша новая ссылка готова: <a href="{link}">{link}</a>', 'success')

        return render_template('main.html', form=form), HTTPStatus.OK

    return render_template('main.html', form=form)


@app.route('/<string:short>')
def urlmap_view(short):
    url_map = is_short_unique(short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
