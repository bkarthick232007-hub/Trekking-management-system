from flask import Blueprint,render_template,request,url_for,flash,redirect
from flask_login import login_user, logout_user, login_required
from models import db, User, StaffProfile
from extensions import bcrypt

auth = Blueprint('auth', __name__)

@auth.route('/register',methods = ["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        contact = request.form.get('contact')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", 'danger')
            return redirect(url_for('auth.register'))
        
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            name = name,
            email = email,
            password_hash = hashed,
            role = role,
            is_active  = True,
            is_blacklisted = False
        )
        db.session.add(new_user)
        db.session.flush()

        if role == "staff":
            profile = StaffProfile(
                user_id = new_user.id,
                contact = contact,
                approval_status = "Pending"
            )
            db.session.add(profile)

        db.session.commit()
        flash("Registered Successfully. Please Log in,", "Success")

    return render_template('auth/register.html')

@auth.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password_hash,password):
            flash('Invalid email or passoword.','danger')
            return redirect(url_for('auth.login'))
        
        if user.is_blacklisted:
            flash('Your account has been blacklisted.', 'danger')
            return redirect(url_for('auth.login'))
        if user.role == 'staff' and user.staff_profile.approval_status != 'Approved':
            flash('Your account is pending admin approval.', 'warning')
            return redirect(url_for('auth.login'))
        
        login_user(user)

        if user.role == "admin":
            return redirect(url_for('admin.dashboard'))
        elif user.role == "staff":
            return redirect(url_for('staff.dashboard'))
        else:
            return redirect(url_for('user.dashboard'))
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
