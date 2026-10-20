from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Trek, Booking

staff = Blueprint('staff', __name__)


@staff.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'staff':
        flash('Access denied. Staff only.', 'danger')
        return redirect(url_for('auth.login'))

    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()

    return render_template('staff/dashboard.html', assigned_treks=assigned_treks)

@staff.route('/trek/<int:trek_id>/participants')
@login_required
def view_participants(trek_id):
    if current_user.role != 'staff':
        flash('Access denied. Staff only.', 'danger')
        return redirect(url_for('auth.login'))

    trek = Trek.query.get(trek_id)

    if not trek or trek.assigned_staff_id != current_user.id:
        flash('You are not authorized to view this trek.', 'danger')
        return redirect(url_for('staff.dashboard'))

    bookings = Booking.query.filter_by(trek_id=trek_id).all()

    return render_template('staff/participants.html', trek=trek, bookings=bookings)

@staff.route('/trek/<int:trek_id>/update', methods=['GET', 'POST'])
@login_required
def update_trek(trek_id):
    if current_user.role != 'staff':
        flash('Access denied. Staff only.', 'danger')
        return redirect(url_for('auth.login'))

    trek = Trek.query.get(trek_id)

    if not trek or trek.assigned_staff_id != current_user.id:
        flash('You are not authorized to manage this trek.', 'danger')
        return redirect(url_for('staff.dashboard'))

    if request.method == 'POST':
        trek.available_slots = int(request.form.get('available_slots'))
        trek.status = request.form.get('status')
        db.session.commit()
        flash('Trek updated successfully.', 'success')
        return redirect(url_for('staff.dashboard'))

    return render_template('staff/update_trek.html', trek=trek)

@staff.route('/trek/<int:trek_id>/complete', methods=['POST'])
@login_required
def complete_trek(trek_id):
    if current_user.role != 'staff':
        flash('Access denied. Staff only.', 'danger')
        return redirect(url_for('auth.login'))

    trek = Trek.query.get(trek_id)

    if not trek or trek.assigned_staff_id != current_user.id:
        flash('You are not authorized to manage this trek.', 'danger')
        return redirect(url_for('staff.dashboard'))

    trek.status = 'Completed'

    for booking in trek.bookings:
        if booking.status == 'Booked':
            booking.status = 'Completed'

    db.session.commit()
    flash('Trek marked as completed.', 'success')
    return redirect(url_for('staff.dashboard'))

