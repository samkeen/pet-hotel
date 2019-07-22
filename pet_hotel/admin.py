import functools

from flask import (
    Blueprint, flash, redirect, render_template, url_for,
    session, g, request)
from werkzeug.security import generate_password_hash, check_password_hash

from pet_hotel.db import get_db, get_uuid
from pet_hotel.forms.admin_register import AdminForm
from pet_hotel.forms.login import LoginForm
from pet_hotel.models import ObjectView, get_model_by_id, update_model, delete_model, get_all

bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('admin.login'))
        return view(**kwargs)

    return wrapped_view


@bp.route('/')
def index():
    return render_template('admin/index.html', admins=get_all('admin'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    # allow register to render if there are no existing admins
    if existing_admins() and g.admin is None:
        return redirect(url_for('admin.login'))
    form = AdminForm(request.form)
    username = form.username.data
    password = form.password.data
    if request.method == 'POST' and form.validate():
        if get_admin_by('username', username) is not None:
            flash(f'The username: "{username}" is not available"')
        else:
            register_new_admin(username, password)
            return redirect(url_for('admin.login'))
    return render_template('admin/register.html', title='Register Admin', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        admin = get_admin_by('username', form.username.data)
        error = None
        if admin is None or not check_password_hash(admin['password'], form.password.data):
            error = 'name and/or password incorrect'
        else:
            session.clear()
            session['user_id'] = admin['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('admin/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/<admin_id>/update', methods=('GET', 'POST'))
@login_required
def update(admin_id):
    admin = get_model_by_id('admin', admin_id)
    form = AdminForm(request.form, ObjectView(admin))
    if request.method == 'POST' and form.validate():
        update_admin(admin_id, form.username.data, form.password.data)
        return redirect(url_for('admin.index'))
    return render_template('admin/update.html', form=form)


@bp.route('/<admin_id>/delete', methods=('POST',))
@login_required
def delete(admin_id):
    admin = get_model_by_id('admin', admin_id)
    if admin is not None:
        delete_model('admin', admin_id)
    return redirect(url_for('admin.index'))


# registers a function that runs before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    admin_id = session.get('user_id')
    if admin_id is None:
        g.admin = None
    else:
        g.admin = get_admin_by('id', admin_id)


def update_admin(admin_id, username, password):
    cur = get_db().cursor()
    cur.execute(
        'UPDATE admin SET username = %s, password=%s WHERE id=%s',
        (username, generate_password_hash(password), admin_id)
    )
    get_db().commit()


def register_new_admin(username, password):
    cur = get_db().cursor()
    cur.execute(
        'INSERT INTO admin (id, username, password) VALUES (%s, %s, %s)',
        (get_uuid(), username, generate_password_hash(password))
    )
    get_db().commit()


def get_admin_by(field_name, field_value):
    cur = get_db().cursor()
    cur.execute(
        f'SELECT * FROM admin WHERE {field_name} = %s', (field_value,)
    )
    return cur.fetchone()


def existing_admins():
    return len(get_admins()) > 0


def get_admins():
    cur = get_db().cursor()
    cur.execute(f'SELECT * FROM admin')
    return cur.fetchall()
