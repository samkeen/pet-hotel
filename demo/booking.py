from flask import (
    Blueprint, render_template, request, redirect, url_for)

from demo.admin import login_required
from demo.db import get_db
from demo.forms.booking import BookingForm
from demo.models import insert_model, get_all, get_model_by_id, ObjectView, update_model, delete_model

bp = Blueprint('booking', __name__, url_prefix='/booking')


@bp.route('/')
def index():
    return render_template('booking/index.html', bookings=get_all('booking'))


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form = BookingForm(request.form)
    form.owner_id.choices = [(pet['id'], f'{pet["last_name"]}, {pet["first_name"]}') for pet in get_owners()]
    form.pet_id.choices = [(pet['id'], pet['name']) for pet in get_pets()]
    if request.method == 'POST' and form.validate():
        fields = form.data
        fields.pop('owner_id')
        insert_model('booking', fields)
        return redirect(url_for('booking.index'))
    return render_template('booking/create.html', title='New Booking', form=form)

@bp.route('/<string:booking_id>/update', methods=('GET', 'POST'))
@login_required
def update(booking_id):
    booking = get_model_by_id('booking', booking_id)
    form = BookingForm(request.form, ObjectView(booking))
    form.owner_id.choices = [(pet['id'], f'{pet["last_name"]}, {pet["first_name"]}') for pet in get_owners()]
    form.pet_id.choices = [(pet['id'], pet['name']) for pet in get_pets()]
    if request.method == 'POST' and form.validate():
        fields = form.data
        fields.pop('owner_id')
        update_model('booking', booking_id, fields)
        return redirect(url_for('booking.index'))
    return render_template('booking/update.html', form=form)


@bp.route('/<string:booking_id>/delete', methods=('POST',))
@login_required
def delete(booking_id):
    booking = get_model_by_id('booking', booking_id)
    if booking is not None:
        delete_model('booking', booking_id)
    return redirect(url_for('booking.index'))

def get_pets():
    cur = get_db().cursor()
    cur.execute('SELECT id, name FROM pet order by name')
    return cur.fetchall()


def get_owners():
    cur = get_db().cursor()
    cur.execute('SELECT id, first_name, last_name FROM owner order by last_name')
    return cur.fetchall()
