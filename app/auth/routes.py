# from flask import Blueprint,render_template, request , redirect ,url_for,flash,session
# import requests
# from flask import current_app
# from app import db
# from app.models import User,Student,Company
# from flask_login import login_user, logout_user, login_required, current_user
# # from app import Bcrypt
# from app import bcrypt
# from datetime import date,datetime



# auth_bp= Blueprint('auth', __name__)



# # @auth_bp.route('/')
# # def index():
# #     show_video = False
# #     if 'video_seen' not in session:
# #         show_video = True
# #         session['video_seen'] = True
# #     return render_template('index.html', show_video=show_video)

# @auth_bp.route('/')
# def index():
#     return render_template('index.html', show_video=True)






# @auth_bp.route('/student_register', methods=['GET', 'POST'])
# def student_register():
#     if request.method == 'POST':
#         try:
#             # Get form data
#             full_name = request.form.get('full_name')
#             email = request.form.get('email')
#             phone = request.form.get('phone')
#             roll_number = request.form.get('roll_number')
#             course = request.form.get('course')
#             branch = request.form.get('branch')
#             graduation_year = request.form.get('graduation_year', type=int)
#             cgpa = request.form.get('cgpa', type=float)
#             dob = request.form.get('dob')
#             address = request.form.get('address')
#             skills = request.form.get('skills')
#             password = request.form.get('password')
#             tenth_marks = request.form.get('tenth_marks', type=float)
#             twelfth_marks = request.form.get('twelfth_marks', type=float)
#             current_year_input = request.form.get('year', type=int)

#             resume = request.files.get('resume_filename')
            
#             dob_str = request.form.get('dob')  # "2005-08-21"
#             dob = None
#             if dob_str:
#                 dob = datetime.strptime(dob_str, "%Y-%m-%d").date() 

#             # Validations
#             if not password or len(password) < 6:
#                 flash('Password must be at least 6 characters.', 'danger')
#                 return redirect(url_for('auth.student_register'))

#             if User.query.filter_by(email=email).first():
#                 flash('Email already registered.', 'danger')
#                 return redirect(url_for('auth.student_register'))

#             if Student.query.filter_by(roll_number=roll_number).first():
#                 flash('Roll number already exists.', 'danger')
#                 return redirect(url_for('auth.student_register'))

#             # Create User
#             user = User(email=email, role='student', is_active=True, is_approved=True)
#             # user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
#             user.set_password(password)
#             db.session.add(user)
#             db.session.commit()

#             # Determine year of study (assuming 4-year program)
#             current_year = date.today().year
#             year_of_study = 4 - (graduation_year - current_year)
#             year_of_study = max(1, min(4, year_of_study))

#             # Handle resume file upload (optional)
#             resume_filename = None
#             if resume:
#                 resume_filename = resume.filename
#                 # resume.save(f'path/to/resumes/{resume_filename}')
#                 resume.save('student_register') 
                

#             # Create Student profile
#             profile = Student(
#                 user_id=user.user_id,
#                 full_name=full_name,
#                 roll_number=roll_number,
#                 course=course,
#                 branch=branch,
#                 graduation_year=graduation_year,
#                 year=year_of_study,
#                 cgpa=cgpa,
#                 dob=dob,
#                 address=address,
#                 skills=skills,
#                 tenth_marks=tenth_marks,
#                 twelfth_marks=twelfth_marks,
#                 phone=phone,
#                 resume_filename=resume_filename
#             )

#             user.student = profile 
#             db.session.add(profile)
#             db.session.commit()

#             flash('Registration successful. Please login.', 'success')
#             return redirect(url_for('auth.login'))

#         except Exception as e:
#             db.session.rollback()
#             flash(f'An error occurred: {str(e)}', 'danger')
#             return redirect(url_for('auth.student_register'))

#     # GET request
#     return render_template('student_register.html')







# # @auth_bp.route('/company_register', methods=['GET', 'POST'])
# # def company_register():
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         password = request.form['password']
# #         company_name = request.form['company_name']
# #         # Validate password length
# #         if len(password) < 6:
# #             flash('Password must be at least 6 characters.', 'danger')
# #             return redirect(url_for('auth.company_register'))
# #         if User.query.filter_by(email=email).first():
# #             flash('Email already registered.', 'danger')
# #             return redirect(url_for('auth.company_register'))
# #         user = User(email=email,password_hash=password, role='company', is_active=True, is_approved=False)
# #         user.set_password(password)
# #         db.session.add(user)
# #         db.session.flush()  
# #         db.session.commit()
# #         profile = Company(user_id=user.user_id, company_name=company_name)
# #         db.session.add(profile)
# #         db.session.commit()
# #         flash('Registration successful. Await admin approval.', 'info')
# #         return redirect(url_for('auth.login'))
# #     return render_template('company_register.html')



# @auth_bp.route('/company_register', methods=['GET', 'POST'])
# def company_register():
#     if request.method == 'POST':
#         address = f"{request.form['address_line']}, {request.form['city']}, {request.form['state']}, {request.form['postal_code']}, {request.form['country']}"
#         email = request.form['email']
#         password = request.form['password']
#         company_name = request.form['company_name']
#         industry=request.form['industry']
#         location=address
#         contact_person=request.form['contact_person']
#         phone=request.form['phone']
#         website=request.form['website']
#         description=request.form['description']

#         # Validate password length
#         if len(password) < 6:
#             flash('Password must be at least 6 characters.', 'danger')
#             return redirect(url_for('auth.company_register'))

#         # Check if email already exists
#         if User.query.filter_by(email=email).first():
#             flash('Email already registered.', 'danger')
#             return redirect(url_for('auth.company_register'))

#         # Create user
#         user = User(
#             email=email,
#             role='company',
#             password_hash=password,
#             is_active=True,
#             is_approved=False
#         )
#         user.set_password(password)

#         # Create company profile
#         profile = Company(
#             company_name=company_name,
#             location=location,
#             industry=industry,
#             contact_person=contact_person,
#             contact_phone=phone,
#             website=website,
#             description=description
            
#         )

#         # Assign relationship (SQLAlchemy sets user_id automatically)
#         user.company = profile

#         # Add and commit both at once
#         db.session.add(user)
#         db.session.commit()

#         flash('Registration successful. Await admin approval.', 'info')
#         return redirect(url_for('auth.login'))

#     return render_template('company_register.html')

# # @auth_bp.route('/login',methods=['GET','POST'])
# # def login():
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         password = request.form['password']
# #         user = User.query.filter_by(email=email).first()
# #         if user and check_password_hash(user.password, password):
            
# #             if user.is_blacklisted or not user.is_active:
# #                 flash('Account is deactivated or blacklisted.', 'danger')
# #                 return redirect(url_for('auth.login'))
            
# #             if user.role == 'company' and not user.is_approved:
# #                 flash('Company account pending admin approval.', 'warning')
# #                 return redirect(url_for('auth.login'))
# #             login_user(user)
# #             session['role'] = user.role
# #             session['is_approved'] = user.is_approved
# #             return redirect(url_for(f'{user.role}.dashboard'))
# #         flash('Invalid credentials.', 'danger')
# #         return redirect(url_for('auth.login'))
# #     return render_template('login.html')

# # @auth_bp.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         email = request.form['email']
# #         password = request.form['password']

# #         user = User.query.filter_by(email=email).first()

# #         # ✅ USE BCRYPT HERE
# #         if user and bcrypt.check_password_hash(user.password_hash, password):
             
# #             if user.is_blacklisted or not user.is_active:
# #                 flash('Account is deactivated or blacklisted.', 'danger')
# #                 return redirect(url_for('auth.login'))

# #             if user.role == 'company' and not user.is_approved:
# #                 flash('Company account pending admin approval.', 'warning')
# #                 return redirect(url_for('auth.login'))

# #             login_user(user)
# #             session['role'] = user.role
# #             session['is_approved'] = user.is_approved
           
# #             flash('Logged in ', 'success')
# #             return redirect(url_for(f'{user.role}.dashboard'))
# #             # return redirect(url_for('auth.student_register'))

# #         flash('Invalid credentials.', 'danger')
# #         return redirect(url_for('auth.login'))

# #     return render_template('login.html')
    

# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         role = request.form.get('role')  # NEW: read role from hidden input

#         user = User.query.filter_by(email=email, role=role).first()  # check both email + role

#         if user and bcrypt.check_password_hash(user.password_hash, password):

#             if user.is_blacklisted or not user.is_active:
#                 flash('Account is deactivated or blacklisted.', 'danger')
#                 return redirect(url_for('auth.login'))

#             if user.role == 'company' and not user.is_approved:
#                 flash('Company account pending admin approval.', 'warning')
#                 return redirect(url_for('auth.login'))

#             login_user(user)
#             session['role'] = user.role
#             session['is_approved'] = user.is_approved

#             # redirect based on role
#             if user.role == 'student':
#                 # flash('Logged in ', 'success')
#                 return redirect(url_for('student.dashboard'))
#             elif user.role == 'company':
#                 # flash('Logged in ', 'success')
#                 return redirect(url_for('company.dashboard'))
#             elif user.role == 'admin':
#                 # flash('Logged in ', 'success')
#                 return redirect(url_for('admin.dashboard'))  # must match blueprint endpoint
#             else:
#                 flash('Invalid role.', 'danger')
#                 return redirect(url_for('auth.login'))

#         flash('Invalid credentials.', 'danger')
#         return redirect(url_for('auth.login'))

#     return render_template('login.html')




# # @auth_bp.route("/login/get_google/<role>")
# # def login_with_google(role):

# #     if role not in ["student", "company","admin"]:
# #         return "Invalid role", 400
    
# #     google_auth_url = (
# #         "https://accounts.google.com/o/oauth2/v2/auth"
# #         "?response_type=code"
# #         f"&client_id={current_app.config['GOOGLE_CLIENT_ID']}"
# #         f"&redirect_uri={current_app.config['GOOGLE_REDIRECT_URI']}"
# #         "&scope=openid%20email%20profile"
# #         "&prompt=select_account"
# #     )

# #     return redirect(google_auth_url)

# @auth_bp.route("/login/get_google/<role>")
# def get_google(role):

#     if role not in ["student", "company", "admin"]:
#         return "Invalid role"

#     session["google_role"] = role   # 🔥 VERY IMPORTANT

#     # build Google auth URL
#     google_auth_url = (
#         "https://accounts.google.com/o/oauth2/v2/auth"
#         "?response_type=code"
#         f"&client_id={current_app.config['GOOGLE_CLIENT_ID']}"
#         f"&redirect_uri={current_app.config['GOOGLE_REDIRECT_URI']}"
#         "&scope=email profile"
#         "&prompt=select_account"
#     )

#     return redirect(google_auth_url)

# # @auth_bp.route("/login/google/callback")
# # def google_callback():
# #     code = request.args.get("code")

# #     token_url = "https://oauth2.googleapis.com/token"

    
# #     data = {
# #         "code": code,
# #         "client_id": current_app.config["GOOGLE_CLIENT_ID"],
# #         "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
# #         "redirect_uri": current_app.config["GOOGLE_REDIRECT_URI"],
# #         "grant_type": "authorization_code",
# #     }

# #     token_response = requests.post(token_url, data=data)
# #     token_json = token_response.json()

# #     access_token = token_json.get("access_token")

# #     userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
# #     userinfo_response = requests.get(
# #         userinfo_url,
# #         headers={"Authorization": f"Bearer {access_token}"}
# #     )

# #     user_info = userinfo_response.json()

# #     # return f"User Email: {user_info.get('email')}"
# #     # return redirect()
# #     if current_user.role == 'student':
# #         return redirect(url_for('student.dashboard'))
# #     elif current_user.role == 'company':
# #         return redirect(url_for('company.dashboard'))
# #     elif current_user.role == 'admin':
# #         return redirect(url_for('admin.dashboard'))  # must match blueprint endpoint
# #     else:
# #         flash('Invalid role.', 'danger')
# #         return redirect(url_for('auth.login'))


# @auth_bp.route("/login/google/callback")
# def google_callback():

#     code = request.args.get("code")

#     token_url = "https://oauth2.googleapis.com/token"

#     data = {
#         "code": code,
#         "client_id": current_app.config["GOOGLE_CLIENT_ID"],
#         "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
#         "redirect_uri": current_app.config["GOOGLE_REDIRECT_URI"],
#         "grant_type": "authorization_code",
#     }

#     token_response = requests.post(token_url, data=data)
#     token_json = token_response.json()

#     access_token = token_json.get("access_token")

#     userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
#     userinfo_response = requests.get(
#         userinfo_url,
#         headers={"Authorization": f"Bearer {access_token}"}
#     )

#     user_info = userinfo_response.json()
#     email = user_info.get("email")

#     # 🔥 VERY IMPORTANT: get role from session
#     role = session.get("google_role")

#     if not role:
#         flash("Invalid role.", "danger")
#         return redirect(url_for("auth.login"))

#     # 🔥 Find user in DB
#     user = User.query.filter_by(email=email, role=role).first()

#     if not user:
#         flash("User not registered for this role.", "danger")
#         return redirect(url_for("auth.login"))

#     # ✅ Login the user
#     login_user(user)

#     flash("Logged in successfully via Google!", "success")

#     # 🔥 Redirect based on role
#     if role == "student":
#         return redirect(url_for("student.dashboard"))

#     elif role == "company":
#         return redirect(url_for("company.dashboard"))

#     elif role == "admin":
#         return redirect(url_for("admin.dashboard"))

#     flash("Invalid role.", "danger")
#     return redirect(url_for("auth.login"))


# @auth_bp.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     session.clear()
#     flash('You are now Logged out', 'info')
#     return redirect(url_for('auth.login'))





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





from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User, Student, Company
from app import bcrypt
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


# @auth_bp.route('/')
# def home():
#     return render_template('index.html',show_video=True)

@auth_bp.route('/')
def index():
    # Example: only show video once per session
    show_video = not session.get('video_seen', False)
    return render_template('index.html', show_video=show_video)

# @auth_bp.route('/')
# def index():
#     show_video = False
#     if 'video_seen' not in session:
#         show_video = True
#         session['video_seen'] = True
#     return render_template('index.html', show_video=show_video)



# =========================
# LOGIN
# =========================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            if user.is_blacklisted:
                flash("Your account has been blacklisted.", "danger")
                return redirect(url_for('auth.login'))

            if user.role in ['student', 'company'] and not user.is_approved:
                flash("Your account is pending admin approval.", "warning")
                return redirect(url_for('auth.login'))

            login_user(user)

            # Role-based redirect
            if user.role == 'student':
                return redirect(url_for('student.dashboard'))
            elif user.role == 'company':
                return redirect(url_for('company.dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.dashboard'))

        flash("Invalid email or password.", "danger")

    return render_template('login.html')


# =========================
# LOGOUT
# =========================
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth.login'))


# =========================
# STUDENT REGISTER
# =========================
# 




# =========================
# STUDENT REGISTER
# =========================
@auth_bp.route('/student_register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        # ----- Form Data -----
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        roll_number = request.form.get('roll_number')
        graduation_year = request.form.get('graduation_year')

        # Optional fields
        cgpa = request.form.get('cgpa')
        tenth_marks = request.form.get('tenth_marks')
        twelfth_marks = request.form.get('twelfth_marks')
        dob = request.form.get('dob')
        year = request.form.get('year')
        address = request.form.get('address')
        skills = request.form.get('skills')
        course = request.form.get('course')
        branch = request.form.get('branch')
        phone = request.form.get('phone')
        resume_filename = request.form.get('resume_filename')  # If file upload, handle separately

        # ----- Check duplicates -----
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for('auth.student_register'))

        if Student.query.filter_by(roll_number=roll_number).first():
            flash("Roll number already registered.", "danger")
            return redirect(url_for('auth.student_register'))

        # ----- Create User -----
        user = User(
            email=email,
            role='student',
            is_active=True,
            is_approved=True,  # Auto-approved
            is_blacklisted=False
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # Generate user_id without committing

        # ----- Create Student Profile -----
        student = Student(
            user_id=user.user_id,
            full_name=full_name,
            roll_number=roll_number,
            graduation_year=int(graduation_year),
            cgpa=float(cgpa) if cgpa else None,
            tenth_marks=float(tenth_marks) if tenth_marks else None,
            twelfth_marks=float(twelfth_marks) if twelfth_marks else None,
            dob=datetime.strptime(dob, '%Y-%m-%d') if dob else None,
            year=int(year) if year else None,
            address=address,
            skills=skills,
            course=course,
            branch=branch,
            phone=phone,
            resume_filename=resume_filename
        )
        db.session.add(student)

        try:
            db.session.commit()
            flash("Registration successful.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {str(e)}", "danger")
            return redirect(url_for('auth.student_register'))

    return render_template('student_register.html')


# =========================
# COMPANY REGISTER
# =========================
@auth_bp.route('/company_register', methods=['GET', 'POST'])
def company_register():
    if request.method == 'POST':
        # ----- Form Data -----
        email = request.form.get('email')
        password = request.form.get('password')
        company_name = request.form.get('company_name')
        industry = request.form.get('industry')
        location = request.form.get('location')
        website = request.form.get('website')
        contact_person = request.form.get('contact_person')
        contact_phone = request.form.get('contact_phone')
        description = request.form.get('description')

        # ----- Check duplicates -----
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for('auth.company_register'))

        if Company.query.filter_by(company_name=company_name).first():
            flash("Company name already registered.", "danger")
            return redirect(url_for('auth.company_register'))

        # ----- Create User -----
        user = User(
            email=email,
            role='company',
            is_active=True,
            is_approved=False,  # Needs admin approval
            is_blacklisted=False
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # Generate user_id without committing

        # ----- Create Company Profile -----
        company = Company(
            user_id=user.user_id,
            company_name=company_name,
            industry=industry,
            location=location,
            website=website,
            contact_person=contact_person,
            contact_phone=contact_phone,
            description=description
        )
        db.session.add(company)

        try:
            db.session.commit()
            flash("Registration successful. Await admin approval.", "info")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {str(e)}", "danger")
            return redirect(url_for('auth.company_register'))

    return render_template('company_register.html')