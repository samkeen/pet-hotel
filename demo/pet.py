from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from demo.admin import login_required
from demo.db import get_db, get_uuid

bp = Blueprint('pet', __name__)

@bp.route('/pet')
def index():
    cur = get_db().cursor()
    cur.execute(
        ' SELECT *'
        ' FROM pet'
    )
    pets = cur.fetchall()
    # .fetchall()
    return render_template('pet/index.html', pets=pets)


@bp.route('/pet/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            cur = get_db().cursor()
            cur.execute(
                'INSERT INTO pet (id, name, date_of_birth, owner_id)'
                ' VALUES (%s, %s, %s, %s)',
                (get_uuid(), name, dob, g.admin['id'])
            )
            get_db().commit()
            return redirect(url_for('pet.index'))

    return render_template('pet/create.html')


def get_pet(pet_id):
    cur = get_db().cursor()
    cur.execute(
        'SELECT p.*'
        ' FROM pet p '
        ' JOIN owner o ON p.owner_id = o.id'
        ' WHERE p.id = %s',
        (pet_id,)
    )
    pet = cur.fetchone()
    if pet is None:
        abort(404, "Pet id {0} doesn't exist.".format(pet_id))
    return pet


@bp.route('/pet/<string:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    pet = get_pet(id)

    if request.method == 'POST':
        name = request.form['name']
        date_of_birth = request.form['date_of_birth']
        error = None

        if not name:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            cur = get_db().cursor()
            cur.execute(
                'UPDATE pet SET name = %s, date_of_birth = %s'
                ' WHERE id = %s',
                (name, date_of_birth, id)
            )
            get_db().commit()
            return redirect(url_for('pet.index'))

    return render_template('pet/update.html', pet=pet)


@bp.route('/pet/<string:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_pet(id)
    cur = get_db().cursor()
    cur.execute('DELETE FROM pet WHERE id = %s', (id,))
    get_db().commit()
    return redirect(url_for('pet.index'))
