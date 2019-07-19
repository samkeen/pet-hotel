import functools

from flask import (
    Blueprint, flash, redirect, render_template, url_for,
    session, g, request)
from werkzeug.security import generate_password_hash, check_password_hash

from demo.db import get_db, get_uuid
from demo.forms.admin_register import AdminRegisterForm
from demo.forms.login import LoginForm

bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('admin.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    form = AdminRegisterForm(request.form)
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


# registers a function that runs before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    admin_id = session.get('user_id')
    if admin_id is None:
        g.admin = None
    else:
        g.admin = get_admin_by('id', admin_id)


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
