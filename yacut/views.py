from flask import abort, flash, redirect, render_template, url_for

from .forms import URLMapForm
from .models import URLMap
from . import app, db


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data or URLMap.get_unique_short_id()
        link = URLMap(original=form.original_link.data, short=short)
        db.session.add(link)
        db.session.commit()
        link = url_for("urlmap_view", short=short, _external=True)
        flash(f'Ваша новая ссылка готова: <a href="{link}">{link}</a>', 'success')

        return render_template('main.html', form=form), 200

    return render_template('main.html', form=form)


@app.route('/<string:short>')
def urlmap_view(short):
    link = URLMap.query.filter_by(short=short).first()
    if link:
        return redirect(link.original)
    else:
        abort(404)
