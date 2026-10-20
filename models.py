from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    password_hash = db.Column(db.String, nullable = False)
    role = db.Column(db.String, nullable = False)
    is_active = db.Column(db.Boolean, nullable = False)
    is_blacklisted = db.Column(db.Boolean, nullable = False)
    staff_profile = db.relationship('StaffProfile', backref = 'user', uselist = False)
    bookings = db.relationship('Booking',backref = 'user')
    assigned_treks = db.relationship('Trek',backref = "assigned_staff")
    

class Trek(db.Model):
    __tablename__ = "treks"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    location = db.Column(db.String, nullable = False)
    difficulty = db.Column(db.String, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    available_slots = db.Column(db.Integer, nullable = False)
    total_slots = db.Column(db.Integer, nullable = False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.String, nullable = False)
    start_date = db.Column(db.Date, nullable = False)
    end_date = db.Column(db.Date, nullable = False)
    bookings = db.relationship('Booking', backref = 'trek')

class Booking (db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"))
    booking_date = db.Column(db.Date, nullable = False)
    status = db.Column(db.String , nullable = False)

class StaffProfile(db.Model):
    __tablename__ = "staffprofiles"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    contact = db.Column(db.String, nullable = False)
    approval_status = db.Column(db.String, nullable = False)
