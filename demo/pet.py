from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from demo.admin import login_required
from demo.forms.pet import PetForm
from demo.models import get_all, insert_model, get_model_by_id, ObjectView, update_model, delete_model

bp = Blueprint('pet', __name__, url_prefix='/pet')

@bp.route('/')
def index():
    return render_template('pet/index.html', pets=get_all('pet'))


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = PetForm(request.form)
    if request.method == 'POST' and form.validate():
        fields = form.data
        insert_model('pet', fields)
        return redirect(url_for('owner.index'))
    return render_template('pet/create.html', form=form)



@bp.route('/<string:pet_id>/update', methods=('GET', 'POST'))
@login_required
def update(pet_id):
    owner = get_model_by_id('pet', pet_id)
    form = PetForm(request.form, ObjectView(owner))
    if request.method == 'POST' and form.validate():
        update_model('pet', pet_id, form.data)
        return redirect(url_for('pet.index'))
    return render_template('pet/update.html', form=form)


@bp.route('/<string:pet_id>/delete', methods=('POST',))
@login_required
def delete(pet_id):
    pet = get_model_by_id('pet', pet_id)
    if pet is not None:
        delete_model('pet', pet_id)
    return redirect(url_for('pet.index'))
