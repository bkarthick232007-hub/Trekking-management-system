from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, Trek, Booking, StaffProfile
from datetime import datetime
admin = Blueprint('admin', __name__)


@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role='user').count()
    total_staff = User.query.filter_by(role='staff').count()
    total_bookings = Booking.query.count()

    return render_template('admin/dashboard.html',
                            total_treks=total_treks,
                            total_users=total_users,
                            total_staff=total_staff,
                            total_bookings=total_bookings)

@admin.route('/staff')
@login_required
def manage_staff():
    if current_user.role != 'admin':
        flash("Access denied. Admins only.", 'danger')
        return redirect(url_for('auth.login'))
    
    pending_staff = StaffProfile.query.filter_by(approval_status = "Pending").all()
    all_staff = StaffProfile.query.all()
    return render_template('admin/staff.html',
                           pending_staff=pending_staff,
                           all_staff=all_staff)

@admin.route('/staff/approve/<int:staff_id>',methods = ["POST"])
@login_required
def approve_staff(staff_id):
    if current_user.role != "admin":
        flash("Access denied. Admins only.", 'danger')
        return redirect(url_for('auth.login'))
    
    staff = StaffProfile.query.get(staff_id)
    if staff:
        staff.approval_status = 'Approved'
        db.session.commit()
        flash("Staff approved successfully.", 'success')
    else:
        flash("Staff not found.",'danger')

    return redirect(url_for('admin.manage_staff'))

@admin.route('/staff/reject/<int:staff_id>', methods=['POST'])
@login_required
def reject_staff(staff_id):
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    staff = StaffProfile.query.get(staff_id)
    if staff:
        staff.approval_status = 'Rejected'
        db.session.commit()
        flash('Staff rejected.', 'warning')
    else:
        flash('Staff not found.', 'danger')

    return redirect(url_for('admin.manage_staff'))

# Trek management routes
@admin.route('/treks/create', methods = ["GET","POST"])
@login_required
def create_trek():
    if current_user.role != "admin":
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))
    if request.method=="POST":
        name = request.form.get("name")
        location = request.form.get('location')
        difficulty = request.form.get('difficulty')
        duration = request.form.get('duration')
        total_slots = request.form.get('total_slots')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()

        new_trek = Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration=int(duration),
            total_slots=int(total_slots),
            available_slots=int(total_slots),
            status='Pending',
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_trek)
        db.session.commit()
        flash("Trek created successfully.", 'success')
        return redirect(url_for('admin.manage_treks'))
    return render_template('admin/create_trek.html')

@admin.route('/treks')
@login_required
def manage_treks():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    all_treks = Trek.query.all()
    approved_staff = StaffProfile.query.filter_by(approval_status='Approved').all()

    return render_template('admin/treks.html',
                            all_treks=all_treks,
                            approved_staff=approved_staff)

@admin.route('/treks/edit/<int:trek_id>', methods=['GET', 'POST'])
@login_required
def edit_trek(trek_id):
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    trek = Trek.query.get(trek_id)
    if not trek:
        flash('Trek not found.', 'danger')
        return redirect(url_for('admin.manage_treks'))

    if request.method == 'POST':
        trek.name = request.form.get('name')
        trek.location = request.form.get('location')
        trek.difficulty = request.form.get('difficulty')
        trek.duration = int(request.form.get('duration'))
        trek.total_slots = int(request.form.get('total_slots'))
        trek.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        trek.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        trek.status = request.form.get('status')

        db.session.commit()
        flash('Trek updated successfully.', 'success')
        return redirect(url_for('admin.manage_treks'))

    return render_template('admin/edit_trek.html', trek=trek)

@admin.route('/treks/delete/<int:trek_id>', methods=['POST'])
@login_required
def delete_trek(trek_id):
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    trek = Trek.query.get(trek_id)
    if trek:
        if trek.bookings:
            flash('Cannot delete trek with existing bookings.', 'danger')
        else:
            db.session.delete(trek)
            db.session.commit()
            flash('Trek deleted successfully.', 'success')
    else:
        flash('Trek not found.', 'danger')

    return redirect(url_for('admin.manage_treks'))

@admin.route('/treks/assign/<int:trek_id>', methods=['POST'])
@login_required
def assign_staff(trek_id):
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    trek = Trek.query.get(trek_id)
    staff_id = request.form.get('staff_id')

    if trek and staff_id:
        trek.assigned_staff_id = int(staff_id)
        db.session.commit()
        flash('Staff assigned successfully.', 'success')
    else:
        flash('Could not assign staff.', 'danger')

    return redirect(url_for('admin.manage_treks'))

@admin.route('/bookings')
@login_required
def view_bookings():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    all_bookings = Booking.query.all()
    return render_template('admin/bookings.html', all_bookings=all_bookings)

@admin.route('/search')
@login_required
def search():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    query = request.args.get('q', '')
    category = request.args.get('category', 'users')

    results = []
    if query:
        if category == 'users':
            results = User.query.filter(User.role == 'user', User.name.contains(query)).all()
        elif category == 'staff':
            results = User.query.filter(User.role == 'staff', User.name.contains(query)).all()
        elif category == 'treks':
            results = Trek.query.filter(Trek.name.contains(query)).all()

    return render_template('admin/search.html', results=results, query=query, category=category)


@admin.route('/blacklist/<int:user_id>', methods=['POST'])
@login_required
def toggle_blacklist(user_id):
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    if user:
        user.is_blacklisted = not user.is_blacklisted
        db.session.commit()
        status = 'blacklisted' if user.is_blacklisted else 'unblacklisted'
        flash(f'User {status} successfully.', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('admin.dashboard'))

