from flask import (
    Blueprint, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from demo.admin import login_required
from demo.db import get_db, get_uuid, build_insert, build_update, build_delete
from demo.forms.owner import OwnerForm
from demo.util import ObjectView

bp = Blueprint('owner', __name__)


@bp.route('/owner')
def index():
    return render_template('owner/index.html', owners=get_owners())


@bp.route('/owner/create', methods=('GET', 'POST'))
@login_required
def create():
    form = OwnerForm(request.form)
    if request.method == 'POST' and form.validate():
        fields = form.data
        insert_owner(fields)
        return redirect(url_for('owner.index'))
    return render_template('owner/create.html', form=form)


@bp.route('/owner/<owner_id>/update', methods=('GET', 'POST'))
@login_required
def update(owner_id):
    owner = get_owner(owner_id)
    form = OwnerForm(request.form, ObjectView(owner))
    if request.method == 'POST' and form.validate():
        update_owner(owner_id, form.data)
        return redirect(url_for('owner.index'))
    return render_template('owner/update.html', form=form)


@bp.route('/owner/<owner_id>/delete', methods=('POST', 'GET'))
@login_required
def delete(owner_id):
    owner = get_owner(owner_id)
    if owner is not None:
        delete_owner(owner_id)
    return redirect(url_for('owner.index'))


def get_owner(owner_id):
    cur = get_db().cursor()
    cur.execute('SELECT * FROM `OWNER` WHERE `id` = %s', (owner_id,))
    owner = cur.fetchone()
    if owner is None:
        abort(404, "Owner id {0} doesn't exist.".format(owner_id))
    return owner


def get_owners():
    cur = get_db().cursor()
    cur.execute('SELECT * FROM owner')
    return cur.fetchall()


def insert_owner(attributes):
    """

    :param attributes:
    :type attributes: dict
    :return:
    :rtype:
    """
    attributes.pop('csrf_token', None)
    cur = get_db().cursor()
    insert_query = build_insert('owner', attributes)
    values = tuple(n for n in [get_uuid()] + list(attributes.values()))
    cur.execute(insert_query, values)
    get_db().commit()


def update_owner(owner_id, attributes):
    """

    :param owner_id:
    :type owner_id: str
    :param attributes:
    :type attributes: dict
    :return:
    :rtype:
    """
    attributes.pop('csrf_token', None)
    attributes.pop('id', None)
    cur = get_db().cursor()
    update_query = build_update('owner', attributes)
    values = tuple(n for n in list(attributes.values()) + [owner_id])
    cur.execute(update_query, values)
    get_db().commit()


def delete_owner(owner_id):
    cur = get_db().cursor()
    cur.execute(build_delete('owner'), (owner_id,))
    get_db().commit()
