# from flask_login import current_user
# from flask import session, redirect, url_for, flash, abort
# from functools import wraps
# from app import db
# from app.models import User,Admin

# def role_required(required_role):
#     """Decorator to ensure user has the required role"""
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if not current_user.is_authenticated:
#                 abort(401)
#             if current_user.role != required_role:
#                 abort(403)
#             if required_role == 'company' and not current_user.is_approved:
#                 abort(403)
#             if not current_user.is_active_user():
#                 abort(403)
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator



# def get_current_user():
#     """
#     Retrieves the current logged-in user from database
#     Returns None if no user is logged in
#     """
#     if 'user_id' in session:
#         return User.query.get(session['user_id'])
#     return None


# def check_application_deadline(deadline_date):
#     """
#     Checks if application deadline has passed
#     Returns True if deadline is still valid, False otherwise
#     """
#     from datetime import date
#     return deadline_date >= date.today()


# def allowed_file(filename):
#     """
#     Checks if uploaded file has an allowed extension
#     Used for resume upload validation
#     """
#     from flask import current_app
#     ALLOWED_EXTENSIONS = current_app.config['ALLOWED_EXTENSIONS']
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def log_admin_action(admin_id, action_type, target_id=None, target_type=None, remarks=None):
#     """
#     Logs an admin action to the audit trail
#     Creates entry in admin_actions table for accountability
#     """
#     from app.models import Admin
    
#     action = Admin(
#         admin_id=admin_id,
#         action_type=action_type,
#         target_id=target_id,
#         target_type=target_type,
#         remarks=remarks
#     )
    
#     try:
#         db.session.add(action)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         print(f"Error logging admin action: {e}")
        
        
# # def create_default_admin():
# #     admin_exists = User.query.filter_by(role='admin').first()

# #     if not admin_exists:
# #         admin_user = User(
# #             email='admin@placement.com',
# #             role='admin',
# #             is_active=True,
# #             is_approved=True,
# #             is_blacklisted=False
# #         )

# #         admin_user.set_password('admin123')

# #         db.session.add(admin_user)
# #         db.session.commit()

# #         admin_entry = Admin(
# #             user_id=admin_user.user_id,
# #             name="Default Admin"
# #         )

# #         db.session.add(admin_entry)
# #         db.session.commit()

# #         print("✓ Default admin created")



# def create_default_admin():
#     from app.models import User, Admin
#     from app import db

#     admin_exists = User.query.filter_by(role='admin').first()

#     if not admin_exists:
#         print("Creating default admin...")

#         admin_user = User(
#             email='admin@placement.com',
#             role='admin',
#             is_active=True,
#             is_approved=True,
#             is_blacklisted=False
#         )

#         admin_user.set_password('admin123')

#         db.session.add(admin_user)
#         db.session.commit()   # FIRST COMMIT (to generate user_id)

#         print("User created with ID:", admin_user.user_id)

#         admin_entry = Admin(
#             user_id=admin_user.user_id,
#             name="Default Admin"
#         )

#         db.session.add(admin_entry)
#         db.session.commit()   # SECOND COMMIT

#         print("Admin table entry created")



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
def create_default_admin():
    from app.models import User, Admin
    from app import db

    admin_exists = User.query.filter_by(role='admin').first()

    if not admin_exists:
        admin_user = User(
            email='admin@placement.com',
            role='admin',
            is_active=True,
            is_approved=True,
            is_blacklisted=False
        )

        admin_user.set_password('admin123')

        db.session.add(admin_user)
        db.session.commit()  # generate user_id

        admin_entry = Admin(
            user_id=admin_user.user_id,
            name="Default Admin"
        )

        db.session.add(admin_entry)
        db.session.commit()
        
        
        
# import os
# from datetime import date
# from werkzeug.utils import secure_filename
# from flask import current_app
# from app import db
# from app.models import User, Student, Company


# # =========================
# # PASSWORD UTIL (OPTIONAL)
# # =========================
# def create_user(email, password, role, is_active=True, is_approved=False):
#     """
#     Creates and returns a new user.
#     """
#     user = User(
#         email=email,
#         role=role,
#         is_active=is_active,
#         is_approved=is_approved
#     )
#     user.set_password(password)
#     db.session.add(user)
#     db.session.commit()
#     return user


# # =========================
# # YEAR OF STUDY CALCULATOR
# # =========================
# def calculate_year_of_study(graduation_year):
#     """
#     Calculates student current year (1–4)
#     """
#     current_year = date.today().year
#     year = 4 - (graduation_year - current_year)
#     return max(1, min(4, year))


# # =========================
# # RESUME FILE SAVE
# # =========================
# def save_resume_file(file):
#     """
#     Saves resume file securely and returns filename.
#     """
#     if not file or file.filename == "":
#         return None

#     filename = secure_filename(file.filename)

#     upload_folder = os.path.join(
#         current_app.root_path,
#         "static",
#         "uploads",
#         "resumes"
#     )

#     os.makedirs(upload_folder, exist_ok=True)

#     file_path = os.path.join(upload_folder, filename)
#     file.save(file_path)

#     return filename


# # =========================
# # STUDENT PROFILE CREATION
# # =========================
# def create_student_profile(user, form_data, resume_file=None):
#     """
#     Creates student profile linked to user.
#     """

#     resume_filename = save_resume_file(resume_file)

#     student = Student(
#         user_id=user.user_id,
#         full_name=form_data.get("full_name"),
#         roll_number=form_data.get("roll_number"),
#         course=form_data.get("course"),
#         branch=form_data.get("branch"),
#         graduation_year=form_data.get("graduation_year"),
#         year=calculate_year_of_study(form_data.get("graduation_year")),
#         cgpa=form_data.get("cgpa"),
#         dob=form_data.get("dob"),
#         address=form_data.get("address"),
#         skills=form_data.get("skills"),
#         tenth_marks=form_data.get("tenth_marks"),
#         twelfth_marks=form_data.get("twelfth_marks"),
#         phone=form_data.get("phone"),
#         resume_filename=resume_filename
#     )

#     user.student = student
#     db.session.add(student)
#     db.session.commit()

#     return student


# # =========================
# # COMPANY PROFILE CREATION
# # =========================
# def create_company_profile(user, form_data):
#     """
#     Creates company profile linked to user.
#     """

#     address = f"{form_data.get('address_line')}, " \
#               f"{form_data.get('city')}, " \
#               f"{form_data.get('state')}, " \
#               f"{form_data.get('postal_code')}, " \
#               f"{form_data.get('country')}"

#     company = Company(
#         company_name=form_data.get("company_name"),
#         location=address,
#         industry=form_data.get("industry"),
#         contact_person=form_data.get("contact_person"),
#         contact_phone=form_data.get("phone"),
#         website=form_data.get("website"),
#         description=form_data.get("description")
#     )

#     user.company = company
#     db.session.add(company)
#     db.session.commit()

#     return company


# # =========================
# # GOOGLE USER FETCH
# # =========================
# def get_user_by_email_and_role(email, role):
#     """
#     Fetch user for Google login.
#     """
#     return User.query.filter_by(email=email, role=role).first()