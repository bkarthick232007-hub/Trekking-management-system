🏔️ Trekking Management App
A role-based web application for managing trekking events — built with Flask, SQLAlchemy, SQLite, and Bootstrap/Jinja2.
Developed as part of the IIT Madras BS Data Science & Programming project (Roll: 24f2007244).
---
📋 Table of Contents
Overview
Roles & Features
Tech Stack
Project Structure
Data Model
Setup & Installation
Environment Variables
Running the App
License
---
Overview
The Trekking Management App is a multi-role web platform that handles the full lifecycle of a trekking event — from trek creation and staff assignment by admins, to booking and history tracking by trekkers, with staff managing trek status and slots in between.
Key design decisions:
Single `User` table with a `role` column (`admin` / `staff` / `trekker`) for a unified auth system
Separate `StaffProfile` table for staff-only attributes (approval status, specialization)
Many-to-many Trek ↔ Staff relationship via a `TrekStaffAssignment` join table
Role-gated access enforced via custom Flask decorators, not inline checks
Application Factory + Blueprints pattern for clean separation of concerns
---
Roles & Features
🔐 Admin
Pre-existing superuser (seeded at DB creation)
Add, edit, and remove treks
Approve or blacklist trek staff
Assign one or more staff members to a trek
View all users, staff, and treks
Search treks, staff, or users by name or ID
Blacklist trekkers or staff
🧭 Trek Staff
Register and log in
Requires admin approval before dashboard access
View treks assigned to them
Update trek details: available slots, trek status (Open / Closed)
View list of trekkers registered for their assigned treks
🥾 Trekker (User)
Register and log in
Browse approved and open treks
Search and filter treks by difficulty or location
Book treks
View booking status and trekking history
---
Tech Stack
Layer	Technology
Frontend	HTML5, CSS3, Bootstrap 5, Jinja2
Backend	Python 3, Flask
ORM	Flask-SQLAlchemy
Database	SQLite
Auth	Flask-Login, Werkzeug password hashing
Forms	Flask-WTF, WTForms
Config	python-dotenv
---
Project Structure
```
trekking_app/
│
├── app/
│   ├── __init__.py          # Application factory: create_app()
│   ├── models.py            # All db.Model classes
│   ├── extensions.py        # db, login_manager (initialized here)
│   │
│   ├── auth/                # Shared: register, login, logout
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── admin/               # Admin-only routes
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── staff/               # Staff-only routes
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── trekker/             # Trekker-only routes
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
├── run.py                   # Entry point
├── .env                     # Secret keys (not committed)
├── .gitignore
└── requirements.txt
```
---
Data Model
```
User
  id, name, email, password_hash, role, is_blacklisted, created_at

StaffProfile  (1:1 with User where role='staff')
  id, user_id (FK), contact_details, approval_status, specialization, created_at

Trek
  id, name, location, difficulty, duration_days, available_slots,
  status, start_date, end_date, description, created_at

TrekStaffAssignment  (many-to-many: Trek ↔ Staff)
  id, trek_id (FK), staff_id (FK), role_on_trek, assigned_date

Booking
  id, user_id (FK), trek_id (FK), booking_date, status, created_at
```
Trek status flow: `Pending → Approved → Open → Closed → Completed`
Booking status: `Booked / Cancelled / Completed`
Staff approval status: `Pending → Approved` (or blacklisted via User.is_blacklisted)
---
Setup & Installation
Prerequisites: Python 3.10+, pip, virtualenv
```bash
# 1. Clone the repository
git clone https://github.com/bkarthick232007-hub/trekking-app.git
cd trekking-app

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```
---
Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///trekking.db
FLASK_ENV=development
```
---
Running the App
```bash
# Initialize the database and seed the admin user
flask shell
>>> from app.extensions import db
>>> db.create_all()
>>> exit()

# Run the development server
python run.py
```
App runs at `http://127.0.0.1:5000`
Default admin credentials (change immediately after first login):
```
Email:    admin@trek.com
Password: admin123
```
---

License
This project is submitted as academic coursework for the IIT Madras BS in Data Science & Programming program. Not licensed for commercial use.
---
Built by Karthick B — bkarthick232007-hub - bkarthick232007@gmail.com