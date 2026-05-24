from flask import Blueprint, render_template, request, redirect, url_for, flash,session,current_app
from flask_login import login_user, logout_user, login_required 
from app import db
from app.models import User, Student, Company
from app import bcrypt
from datetime import datetime
import requests


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    # Example: only show video once per session
    show_video = not session.get('video_seen', False)
    return render_template('index.html', show_video=show_video)


# =========================
# LOGIN
# =========================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        selected_role = request.form.get('role')   # 👈 role from tab

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

            # 🚨 role mismatch check
            if user.role != selected_role:
                flash("Please login using the correct role tab.", "danger")
                return redirect(url_for('auth.login'))

            if user.is_blacklisted:
                flash("Your account has been blacklisted.", "danger")
                return redirect(url_for('auth.login'))

            if user.role in ['student','company'] and not user.is_approved:
                flash("Your account is pending admin approval.", "warning")
                return redirect(url_for('auth.login'))

            login_user(user)

            # Role redirect
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

        # ----- Handle Resume Upload -----
        resume_file = request.files.get('resume_filename')
        resume_filename = None
        if resume_file and resume_file.filename:
            from werkzeug.utils import secure_filename
            import os

            # Secure the filename
            resume_filename = secure_filename(resume_file.filename)

            # Make sure upload folder exists
            upload_folder = os.path.join(current_app.root_path, 'static/uploads/resumes')
            os.makedirs(upload_folder, exist_ok=True)

            # Save file
            resume_path = os.path.join(upload_folder, resume_filename)
            resume_file.save(resume_path)

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
        address = f"{request.form['address_line']}, {request.form['city']}, {request.form['state']}, {request.form['postal_code']}, {request.form['country']}"
        email = request.form.get('email')
        password = request.form.get('password')
        company_name = request.form.get('company_name')
        industry = request.form.get('industry')
        location = address
        website = request.form.get('website')
        contact_person = request.form.get('contact_person')
        contact_phone = request.form.get('phone')
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




@auth_bp.route("/login/get_google/<role>")
def get_google(role):

    if role not in ["student", "company", "admin"]:
        return "Invalid role"

    session["google_role"] = role   # 🔥 VERY IMPORTANT

    # build Google auth URL
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={current_app.config['GOOGLE_CLIENT_ID']}"
        f"&redirect_uri={current_app.config['GOOGLE_REDIRECT_URI']}"
        "&scope=email profile"
        "&prompt=select_account"
    )

    return redirect(google_auth_url)



@auth_bp.route("/login/google/callback")
def google_callback():

    code = request.args.get("code")

    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": current_app.config["GOOGLE_CLIENT_ID"],
        "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": current_app.config["GOOGLE_REDIRECT_URI"],
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_url, data=data)
    token_json = token_response.json()

    access_token = token_json.get("access_token")

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    userinfo_response = requests.get(
        userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    user_info = userinfo_response.json()
    email = user_info.get("email")

    # 🔥 VERY IMPORTANT: get role from session
    role = session.get("google_role")

    if not role:
        flash("Invalid role.", "danger")
        return redirect(url_for("auth.login"))

    # 🔥 Find user in DB
    user = User.query.filter_by(email=email, role=role).first()

    if not user:
        flash("User not registered for this role.", "danger")
        return redirect(url_for("auth.login"))

    # ✅ Login the user
    login_user(user)

    flash("Logged in successfully via Google!", "success")

    # 🔥 Redirect based on role
    if role == "student":
        return redirect(url_for("student.dashboard"))

    elif role == "company":
        return redirect(url_for("company.dashboard"))

    elif role == "admin":
        return redirect(url_for("admin.dashboard"))

    flash("Invalid role.", "danger")
    return redirect(url_for("auth.login"))
