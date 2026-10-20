from flask import Flask,redirect,url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import db, User
from config import Config
from extensions import bcrypt,login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        db.create_all()
        seed_admin(bcrypt)

    from auth import auth
    app.register_blueprint(auth , url_prefix = '/auth')

    from admin import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from staff import staff
    app.register_blueprint(staff, url_prefix='/staff')

    from user import user
    app.register_blueprint(user, url_prefix = '/user')

    @app.route('/')
    def home():
        from flask_login import current_user
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'staff':
                return redirect(url_for('staff.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))
        return redirect(url_for('auth.login'))

    return app


def seed_admin(bcrypt):
    admin = User.query.filter_by(role = "admin").first()
    if not admin:
        hashed = bcrypt.generate_password_hash("admin123").decode("utf-8")
        admin = User(
            name = "Admin",
            email = "admin@trek.com",
            password_hash = hashed,
            role = "admin",
            is_active = True,
            is_blacklisted = False)
        db.session.add(admin)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)