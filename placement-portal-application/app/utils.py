from flask_login import current_user
from flask import session, abort, current_app
from functools import wraps
from app.models import User


# =========================
# ROLE REQUIRED DECORATOR
# =========================
def role_required(required_role):
    """
    Decorator to ensure user:
    - is logged in
    - has correct role
    - is approved (if student/company)
    - is not blacklisted
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if not current_user.is_authenticated:
                abort(401)

            if current_user.role != required_role:
                abort(403)

            # Only student and company require approval
            if required_role in ["student", "company"] and not current_user.is_approved:
                abort(403)

            # Block blacklisted users
            if current_user.is_blacklisted:
                abort(403)

            return f(*args, **kwargs)

        return decorated_function
    return decorator


# =========================
# GET CURRENT USER
# =========================
def get_current_user():
    """
    Retrieves the current logged-in user from database
    Returns None if no user is logged in
    """
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


# =========================
# CHECK APPLICATION DEADLINE
# =========================
def check_application_deadline(deadline_date):
    """
    Returns True if deadline has not passed
    """
    from datetime import date
    return deadline_date >= date.today()


# =========================
# FILE VALIDATION
# =========================
def allowed_file(filename):
    """
    Checks if uploaded file has an allowed extension
    Used for resume upload validation
    """
    ALLOWED_EXTENSIONS = current_app.config.get("ALLOWED_EXTENSIONS", set())

    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# =========================
# CREATE DEFAULT ADMIN
# =========================
# def create_default_admin():
#     from app.models import User, Admin
#     from app import db

#     admin_exists = User.query.filter_by(role='admin').first()

#     if not admin_exists:
#         admin_user = User(
#             email='admin@placement.com',
#             role='admin',
#             is_active=True,
#             is_approved=True,
#             is_blacklisted=False
#         )

#         admin_user.set_password('admin123')

#         db.session.add(admin_user)
#         db.session.commit()  # generate user_id

#         admin_entry = Admin(
#             user_id=admin_user.user_id,
#             name="Default Admin"
#         )

#         db.session.add(admin_entry)
#         db.session.commit()


import os

def create_default_admin():
    from app.models import User, Admin
    from app import db

    admin_exists = User.query.filter_by(role='admin').first()

    if not admin_exists:

        admin_email = os.environ.get("DEFAULT_ADMIN_EMAIL")
        admin_password = os.environ.get("DEFAULT_ADMIN_PASSWORD")
        admin_name = os.environ.get("DEFAULT_ADMIN_NAME", "Admin")

        # Prevent creation if variables missing
        if not admin_email or not admin_password:
            print("Admin environment variables not set.")
            return

        admin_user = User(
            email=admin_email,
            role='admin',
            is_active=True,
            is_approved=True,
            is_blacklisted=False
        )

        admin_user.set_password(admin_password)

        db.session.add(admin_user)
        db.session.commit()

        admin_entry = Admin(
            user_id=admin_user.user_id,
            name=admin_name
        )

        db.session.add(admin_entry)
        db.session.commit()

        print("Default admin created successfully.")