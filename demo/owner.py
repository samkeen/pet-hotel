from flask import (
    Blueprint, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from demo.admin import login_required
from demo.db import get_db, build_update, build_delete
from demo.forms.owner import OwnerForm
from demo.models import get_all, insert_model, get_model_by_id, ObjectView, update_model, delete_model

bp = Blueprint('owner', __name__)


@bp.route('/owner')
def index():
    return render_template('owner/index.html', owners=get_all('owner'))


@bp.route('/owner/create', methods=('GET', 'POST'))
@login_required
def create():
    form = OwnerForm(request.form)
    if request.method == 'POST' and form.validate():
        fields = form.data
        insert_model('owner', fields)
        return redirect(url_for('owner.index'))
    return render_template('owner/create.html', form=form)


@bp.route('/owner/<owner_id>/update', methods=('GET', 'POST'))
@login_required
def update(owner_id):
    owner = get_model_by_id('owner', owner_id)
    form = OwnerForm(request.form, ObjectView(owner))
    if request.method == 'POST' and form.validate():
        update_model('owner', owner_id, form.data)
        return redirect(url_for('owner.index'))
    return render_template('owner/update.html', form=form)


@bp.route('/owner/<owner_id>/delete', methods=('POST',))
@login_required
def delete(owner_id):
    owner = get_model_by_id('owner', owner_id)
    if owner is not None:
        delete_model('owner', owner_id)
    return redirect(url_for('owner.index'))
