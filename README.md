Trekking Management Application

A role-based web application for managing trekking events, built with Flask, SQLAlchemy, SQLite, and Bootstrap with Jinja2 templating.

Developed as part of the IIT Madras BS in Data Science and Programming programme (Roll No: 24f2007244).

Table of Contents
Overview
Roles and Features
Tech Stack
Project Structure
Data Model
Setup and Installation
Environment Variables
Running the Application
Screenshots
License
Overview

The Trekking Management Application is a multi-role web platform that handles the complete lifecycle of a trekking event — from creation and staff assignment by administrators, to status management by trek staff, to browsing and booking by trekkers.

Key architectural decisions:

A single User table with a role column (admin, staff, trekker) provides a unified authentication system across all three roles.
A separate StaffProfile table holds staff-specific attributes such as approval status and specialization, linked 1-to-1 with the User table.
A TrekStaffAssignment join table models the many-to-many relationship between treks and staff members, with an optional role_on_trek field to designate lead guides.
Role-based access control is enforced through custom Flask decorators applied at the route level, rather than inline conditional checks.
The Application Factory pattern with Blueprints separates concerns cleanly across roles and prevents circular imports.
Roles and Features
Administrator
Pre-existing superuser, seeded at database initialisation.
Add, edit, and remove treks.
Approve or blacklist trek staff members.
Assign one or more staff members to a trek.
View all registered users, staff, and treks.
Search treks, staff, or users by name or ID.
Blacklist trekkers or staff as required.
Trek Staff
Self-registration and login.
Dashboard access requires prior approval from the administrator.
View treks assigned by the administrator.
Update trek details: available slots and trek status (Open or Closed).
View the list of trekkers registered for their assigned treks.
Trekker (User)
Self-registration and login.
Browse all approved and open treks.
Search and filter treks by difficulty level or location.
Book available treks.
View current booking status and full trekking history.
Tech Stack
Layer	Technology
Frontend	HTML5, CSS3, Bootstrap 5, Jinja2
Backend	Python 3, Flask
ORM	Flask-SQLAlchemy
Database	SQLite
Auth	Flask-Login, Werkzeug password hashing
Forms	Flask-WTF, WTForms
Config	python-dotenv
Project Structure
trekking_app/
│
├── app/
│   ├── __init__.py          # Application factory: create_app()
│   ├── models.py            # All db.Model classes
│   ├── extensions.py        # db, login_manager (initialised here)
│   │
│   ├── auth/                # Shared blueprint: register, login, logout
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── admin/               # Admin-only blueprint
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── staff/               # Staff-only blueprint
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── trekker/             # Trekker-only blueprint
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── admin/
│   │   ├── staff/
│   │   └── trekker/
│   │
│   └── static/
│       ├── css/
│       └── js/
│
├── config.py                # Config class reading from .env
├── run.py                   # Application entry point
├── .env                     # Environment secrets (not committed)
├── .gitignore
└── requirements.txt
Data Model
User
  id, name, email, password_hash, role, is_blacklisted, created_at

StaffProfile  (1:1 with User where role = 'staff')
  id, user_id (FK), contact_details, approval_status, specialization, created_at

Trek
  id, name, location, difficulty, duration_days, available_slots,
  status, start_date, end_date, description, created_at

TrekStaffAssignment  (many-to-many: Trek and Staff)
  id, trek_id (FK), staff_id (FK), role_on_trek, assigned_date

Booking
  id, user_id (FK), trek_id (FK), booking_date, status, created_at

Trek status progression: Pending -> Approved -> Open -> Closed -> Completed

Booking status values: Booked, Cancelled, Completed

Staff approval status: Pending -> Approved (blacklisting is managed via User.is_blacklisted)

Setup and Installation

Prerequisites: Python 3.10 or above, pip, virtualenv

bash
# Clone the repository
git clone https://github.com/bkarthick232007-hub/trekking-app.git
cd trekking-app

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Environment Variables

Create a .env file in the project root with the following contents:

SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///trekking.db
FLASK_ENV=development

Note: The .env file must never be committed to version control. It is included in .gitignore by default.

Running the Application
bash
# Initialise the database
flask shell
>>> from app.extensions import db
>>> db.create_all()
>>> exit()

# Start the development server
python run.py

The application will be available at http://127.0.0.1:5000.

Default administrator credentials (update immediately after first login):

Email:    admin@trek.com
Password: admin123

License

This project is submitted as academic coursework for the IIT Madras BS in Data Science and Programming programme. It is not licensed for commercial use.

Developed by Karthick B — bkarthick232007-hub | bkarthick232007@gmail.com