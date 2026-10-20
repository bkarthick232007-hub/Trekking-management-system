from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Trek, Booking
from datetime import date

user = Blueprint('user', __name__)


@user.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'user':
        flash('Access denied. Users only.', 'danger')
        return redirect(url_for('auth.login'))

    open_treks = Trek.query.filter_by(status='Open').all()
    my_bookings = Booking.query.filter_by(user_id=current_user.id).all()

    return render_template('user/dashboard.html',
                            open_treks=open_treks,
                            my_bookings=my_bookings)

@user.route('/search')
@login_required
def search_treks():
    if current_user.role != 'user':
        flash('Access denied. Users only.', 'danger')
        return redirect(url_for('auth.login'))

    difficulty = request.args.get('difficulty', '')
    location = request.args.get('location', '')

    query = Trek.query.filter_by(status='Open')

    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
    if location:
        query = query.filter(Trek.location.contains(location))

    results = query.all()

    return render_template('user/search.html', results=results, difficulty=difficulty, location=location)

@user.route('/book/<int:trek_id>', methods=['POST'])
@login_required
def book_trek(trek_id):
    if current_user.role != 'user':
        flash('Access denied. Users only.', 'danger')
        return redirect(url_for('auth.login'))

    trek = Trek.query.get(trek_id)

    if not trek:
        flash('Trek not found.', 'danger')
        return redirect(url_for('user.dashboard'))

    if trek.status != 'Open':
        flash('This trek is not open for booking.', 'danger')
        return redirect(url_for('user.dashboard'))

    if trek.available_slots <= 0:
        flash('No slots available for this trek.', 'danger')
        return redirect(url_for('user.dashboard'))

    existing_booking = Booking.query.filter_by(user_id=current_user.id, trek_id=trek_id).first()
    if existing_booking:
        flash('You have already booked this trek.', 'warning')
        return redirect(url_for('user.dashboard'))

    new_booking = Booking(
        user_id=current_user.id,
        trek_id=trek_id,
        booking_date=date.today(),
        status='Booked'
    )
    trek.available_slots -= 1

    db.session.add(new_booking)
    db.session.commit()
    flash('Trek booked successfully!', 'success')
    return redirect(url_for('user.dashboard'))

@user.route('/history')
@login_required
def history():
    if current_user.role != 'user':
        flash('Access denied. Users only.', 'danger')
        return redirect(url_for('auth.login'))

    completed_bookings = Booking.query.filter_by(user_id=current_user.id, status='Completed').all()

    return render_template('user/history.html', completed_bookings=completed_bookings)

@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'user':
        flash('Access denied. Users only.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.email = request.form.get('email')
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user.dashboard'))

    return render_template('user/profile.html')

