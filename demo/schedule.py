from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from demo.db import get_db
from demo.admin import login_required

bp = Blueprint('schedule', __name__)


@bp.route('/')
def index():
    cur = get_db().cursor()
    cur.execute(
        'SELECT pf.*, ft.*, p.*, dow.`order`, dow.name AS day_name'
        ' FROM pet_feeding pf'
        ' INNER JOIN pet p ON pf.pet_id = p.id'
        ' INNER JOIN food_type ft ON pf.food_type_id = ft.id'
        ' INNER JOIN day_of_week dow ON pf.day_of_week_id = dow.id'
        ' ORDER BY dow.`order`'
    )
    schedule = cur.fetchall()
    payload = {
        'sunday': [],
        'monday': [],
        'tuesday': [],
        'wednesday': [],
        'thursday': [],
        'friday': [],
        'saturday': []
    }
    # <class 'dict'>: {'id': '397b0250-a388-11e9-a83a-f21898781639',
    # 'pet_id': 'fea2e2b6-a368-11e9-a83a-f21898781639',
    # 'food_type_id': '4e3c8cae-a388-11e9-a83a-f21898781639',
    # 'day_of_week_id': 1, 'time_of_day': datetime.timedelta(seconds=21600),
    # 'food_amount_in_grams': 40, 'ft.id': '4e3c8cae-a388-11e9-a83a-f21898781639',
    # 'label': 'Salmon Pate', 'p.id': 'fea2e2b6-a368-11e9-a83a-f21898781639',
    # 'name': 'Fido', 'date_of_birth': datetime.date(2015, 7, 18),
    # 'user_id': '78473fbe-a296-11e9-84fa-6ea907249eaf',
    # 'order': 0, 'day_name': 'sunday'}
    for item in schedule:
        payload[item['day_name']].append(item)

    return render_template('schedule/index.html', schedule=payload)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.admin['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, name'
        ' FROM post p JOIN admin u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.admin['id']:
        abort(403)

    return post


@bp.route('/<string:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
