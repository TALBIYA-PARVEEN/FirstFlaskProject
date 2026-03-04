# from flask import Blueprint, render_template, redirect, flash, url_for, request, current_app, send_from_directory
# from flask_login import login_required, current_user
# from app.models import Student, Application, PlacementDrive
# from app.utils import role_required, allowed_file
# from app import db
# from datetime import date, datetime
# import os
# from werkzeug.utils import secure_filename

# student_bp = Blueprint('student', __name__, url_prefix='/student')


# # ---------------- DASHBOARD ----------------
# @student_bp.route('/dashboard')
# @login_required
# @role_required('student')
# def dashboard():
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
#     if not profile:
#         flash('Profile not found.', 'danger')
#         return redirect(url_for('auth.login'))

#     # Stats
#     total_apps = Application.query.filter_by(student_id=profile.user_id).count()
#     selected = Application.query.filter_by(student_id=profile.user_id, status='selected').count()
#     pending = Application.query.filter_by(student_id=profile.user_id, status='pending').count()

#     return render_template(
#         'student/dashboard.html',
#         profile=profile,
#         total_applications=total_apps,
#         selected_applications=selected,
#         pending_applications=pending
#     )


# # ---------------- PROFILE ----------------
# @student_bp.route('/profile')
# @login_required
# @role_required('student')
# def profile():
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
#     return render_template('student/profile.html', profile=profile)


# @student_bp.route('/profile/edit', methods=['GET', 'POST'])
# @login_required
# @role_required('student')
# def edit_profile():
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
#     if request.method == 'POST':
#         profile.full_name = request.form.get('full_name')
#         profile.department = request.form.get('department')
#         profile.year = request.form.get('year') or profile.year
#         profile.cgpa = float(request.form.get('cgpa')) if request.form.get('cgpa') else profile.cgpa
#         profile.tenth_marks = float(request.form.get('tenth_marks')) if request.form.get('tenth_marks') else profile.tenth_marks
#         profile.twelfth_marks = float(request.form.get('twelfth_marks')) if request.form.get('twelfth_marks') else profile.twelfth_marks
#         profile.phone = request.form.get('phone')
#         profile.address = request.form.get('address')
#         profile.skills = request.form.get('skills')
#         dob = request.form.get('dob')
#         if dob:
#             profile.dob = datetime.strptime(dob, '%Y-%m-%d').date()
#         db.session.commit()
#         flash('Profile updated successfully.', 'success')
#         return redirect(url_for('student.profile'))
#     return render_template('student/edit_profile.html', profile=profile)


# @student_bp.route('/profile/resume')
# @login_required
# @role_required('student')
# def download_resume():
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
#     if profile and profile.resume_filename:
#         return send_from_directory(current_app.config['UPLOAD_FOLDER'], profile.resume_filename)
#     flash('No resume found.', 'warning')
#     return redirect(url_for('student.profile'))


# @student_bp.route('/profile/upload_resume', methods=['POST'])
# @login_required
# @role_required('student')
# def upload_resume():
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
#     if 'resume' not in request.files:
#         flash('No file part.', 'danger')
#         return redirect(url_for('student.dashboard'))

#     file = request.files['resume']
#     if file.filename == '':
#         flash('No selected file.', 'danger')
#         return redirect(url_for('student.dashboard'))

#     if file and allowed_file(file.filename) and file.filename.lower().endswith('.pdf'):
#         filename = secure_filename(f"{profile.roll_number}_resume.pdf")
#         upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
#         file.save(upload_path)
#         profile.resume_filename = filename
#         db.session.commit()
#         flash('Resume uploaded successfully.', 'success')
#     else:
#         flash('Invalid file type. Only PDF allowed.', 'danger')
#     return redirect(url_for('student.dashboard'))




# @student_bp.route('/drives')
# @login_required
# @role_required('student')
# def drives():
#     today = date.today()
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
    
#     # Only show drives that are approved and not past deadline
#     drives = PlacementDrive.query.filter(
#         PlacementDrive.status == 'Approved',
#         PlacementDrive.application_deadline >= today
#     ).all()

#     # IDs of drives the student has already applied to
#     applied_drive_ids = [
#         app.drive_id for app in Application.query.filter_by(student_id=profile.user_id).all()
#     ]

#     return render_template('student/drives.html', drives=drives, applied_drive_ids=applied_drive_ids)


# @student_bp.route('/drives/<int:drive_id>')
# @login_required
# @role_required('student')
# def drive_detail(drive_id):
#     drive = PlacementDrive.query.get_or_404(drive_id)
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
#     already_applied = Application.query.filter_by(
#         student_id=profile.user_id, drive_id=drive_id
#     ).first() is not None

#     # Only allow viewing if drive is approved
#     if drive.status != 'Approved':
#         flash('This drive is not available.', 'warning')
#         return redirect(url_for('student.drives'))

#     return render_template('student/drive_detail.html', drive=drive, already_applied=already_applied)


# @student_bp.route('/drives/<int:drive_id>/apply', methods=['POST'])
# @login_required
# @role_required('student')
# def apply_drive(drive_id):
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
#     drive = PlacementDrive.query.get_or_404(drive_id)

#     # Check if already applied
#     if Application.query.filter_by(student_id=profile.user_id, drive_id=drive_id).first():
#         flash('Already applied to this drive.', 'warning')
#         return redirect(url_for('student.drives'))

#     # Check if drive is open for applications
#     if drive.status != 'Approved' or (drive.application_deadline and drive.application_deadline < date.today()):
#         flash('Drive not open for applications.', 'danger')
#         return redirect(url_for('student.drives'))

#     # Submit application
#     app_entry = Application(student_id=profile.user_id, drive_id=drive_id, status='pending')
#     db.session.add(app_entry)
#     db.session.commit()
#     flash('Application submitted successfully.', 'success')
#     return redirect(url_for('student.applications'))

# # ---------------- APPLICATIONS ----------------
# @student_bp.route('/applications')
# @login_required
# @role_required('student')
# def applications():
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
#     apps = Application.query.filter_by(student_id=profile.user_id).all()
#     return render_template('student/applications.html', applications=apps)


# @student_bp.route('/applications/<int:app_id>/withdraw', methods=['POST'])
# @login_required
# @role_required('student')
# def withdraw_application(app_id):
#     profile = Student.query.filter_by(user_id=current_user.user_id).first()
#     app_entry = Application.query.get_or_404(app_id)

#     if app_entry.student_id != profile.user_id:
#         flash('Unauthorized action.', 'danger')
#         return redirect(url_for('student.applications'))

#     if app_entry.status != 'pending':
#         flash('Only pending applications can be withdrawn.', 'warning')
#         return redirect(url_for('student.applications'))

#     db.session.delete(app_entry)
#     db.session.commit()
#     flash('Application withdrawn successfully.', 'success')
#     return redirect(url_for('student.applications'))





from flask import Blueprint, render_template, redirect, flash, url_for, request, current_app, send_from_directory
from flask_login import login_required, current_user
from app.models import Student, Application, PlacementDrive,Company
from app.utils import role_required, allowed_file
from app import db
from datetime import date, datetime
import os
from werkzeug.utils import secure_filename

student_bp = Blueprint('student', __name__, url_prefix='/student')


# ---------------- HELPER ----------------
def get_student_profile():
    return Student.query.filter_by(user_id=current_user.user_id).first()


# ---------------- DASHBOARD ----------------
@student_bp.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    profile = get_student_profile()
    if not profile:
        flash('Profile not found.', 'danger')
        return redirect(url_for('auth.logout'))

    total_apps = Application.query.filter_by(student_id=profile.user_id).count()
    selected = Application.query.filter_by(student_id=profile.user_id, status='Selected').count()
    pending = Application.query.filter_by(student_id=profile.user_id, status='Pending').count()
    
    
    # pending = Application.query.filter(Application.student_id==current_user.user_id,
    #                                             Application.status.in_(["Pending", "Applied"])).count()

    return render_template(
        'student/dashboard.html',
        profile=profile,
        total_applications=total_apps,
        selected_applications=selected,
        pending_applications=pending
    )


# ---------------- PROFILE ----------------
# @student_bp.route('/profile')
# @login_required
# @role_required('student')
# def profile():
#     profile = get_student_profile()
#     if not profile:
#         flash('Profile not found.', 'danger')
#         return redirect(url_for('student.dashboard'))

#     return render_template('student/profile.html', profile=profile)


@student_bp.route('/profile')
@login_required
@role_required('student')
def profile():
    profile = current_user.student  # load the related Student record
    if not profile:
        flash('Profile not found.', 'danger')
        return redirect(url_for('student.dashboard'))

    return render_template('student/profile.html', profile=profile)


# ---------------- EDIT PROFILE ----------------
@student_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@role_required('student')
def edit_profile():
    profile = get_student_profile()
    if not profile:
        flash('Profile not found.', 'danger')
        return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        profile.full_name = request.form.get('full_name')
        profile.branch = request.form.get('branch')  # FIXED (was department)
        profile.year = request.form.get('year') or profile.year
        profile.cgpa = float(request.form.get('cgpa')) if request.form.get('cgpa') else profile.cgpa
        profile.tenth_marks = float(request.form.get('tenth_marks')) if request.form.get('tenth_marks') else profile.tenth_marks
        profile.twelfth_marks = float(request.form.get('twelfth_marks')) if request.form.get('twelfth_marks') else profile.twelfth_marks
        profile.phone = request.form.get('phone')
        profile.address = request.form.get('address')
        profile.skills = request.form.get('skills')

        dob = request.form.get('dob')
        if dob:
            profile.dob = datetime.strptime(dob, '%Y-%m-%d').date()

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('student.profile'))

    return render_template('student/edit_profile.html', profile=profile)


# ---------------- DOWNLOAD RESUME ----------------
@student_bp.route('/profile/resume')
@login_required
@role_required('student')
def download_resume():
    profile = get_student_profile()

    if profile and profile.resume_filename:
        upload_folder = os.path.join(
            current_app.root_path,
            'static',
            'uploads',
            'resumes'
        )
        return send_from_directory(upload_folder, profile.resume_filename)

    flash('No resume found.', 'warning')
    return redirect(url_for('student.profile'))


# ---------------- UPLOAD RESUME ----------------
@student_bp.route('/profile/upload_resume', methods=['POST'])
@login_required
@role_required('student')
def upload_resume():
    profile = get_student_profile()

    if not profile:
        flash('Profile not found.', 'danger')
        return redirect(url_for('student.dashboard'))

    if 'resume' not in request.files:
        flash('No file part.', 'danger')
        return redirect(url_for('student.dashboard'))

    file = request.files['resume']

    if file.filename == '':
        flash('No selected file.', 'danger')
        return redirect(url_for('student.dashboard'))

    if file and allowed_file(file.filename) and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(f"{profile.roll_number}_resume.pdf")

        upload_folder = os.path.join(
            current_app.root_path,
            'static',
            'uploads',
            'resumes'
        )
        os.makedirs(upload_folder, exist_ok=True)

        file.save(os.path.join(upload_folder, filename))

        profile.resume_filename = filename
        db.session.commit()

        flash('Resume uploaded successfully.', 'success')
    else:
        flash('Invalid file type. Only PDF allowed.', 'danger')

    return redirect(url_for('student.dashboard'))


# ---------------- DRIVES ----------------
from sqlalchemy import and_
from datetime import date

@student_bp.route('/drives')
@login_required
@role_required('student')
def drives():
    today = date.today()
    profile = get_student_profile()

    drives = PlacementDrive.query.join(Company).filter(
        and_(
            PlacementDrive.status.in_(['Approved', 'Active']),
            PlacementDrive.application_deadline >= today
        )
    ).all()

    applied_drive_ids = [
        app.drive_id for app in
        Application.query.filter_by(student_id=profile.user_id).all()
    ]

    return render_template(
        'student/drives.html',
        drives=drives,
        applied_drive_ids=applied_drive_ids
    )

# ---------------- DRIVE DETAIL ----------------
@student_bp.route('/drives/<int:drive_id>')
@login_required
@role_required('student')
def drive_detail(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    profile = get_student_profile()

    already_applied = Application.query.filter_by(
        student_id=profile.user_id,
        drive_id=drive_id
    ).first() is not None

    if drive.status != 'Approved':
        flash('This drive is not available.', 'warning')
        return redirect(url_for('student.drives'))

    return render_template(
        'student/drive_detail.html',
        drive=drive,
        already_applied=already_applied
    )


# ---------------- APPLY ----------------
@student_bp.route('/drives/<int:drive_id>/apply', methods=['POST'])
@login_required
@role_required('student')
def apply_drive(drive_id):
    profile = get_student_profile()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if Application.query.filter_by(
        student_id=profile.user_id,
        drive_id=drive_id
    ).first():
        flash('Already applied to this drive.', 'warning')
        return redirect(url_for('student.drives'))

    if drive.status != 'Approved' or (
        drive.application_deadline and drive.application_deadline < date.today()
    ):
        flash('Drive not open for applications.', 'danger')
        return redirect(url_for('student.drives'))

    app_entry = Application(
        student_id=profile.user_id,
        drive_id=drive_id,
        status='pending'
    )

    db.session.add(app_entry)
    db.session.commit()

    flash('Application submitted successfully.', 'success')
    return redirect(url_for('student.applications'))


# ---------------- APPLICATIONS ----------------
@student_bp.route('/applications')
@login_required
@role_required('student')
def applications():
    profile = get_student_profile()
    apps = Application.query.filter_by(student_id=current_user.user_id).all()
    return render_template('student/applications.html', applications=apps)


# ---------------- WITHDRAW ----------------
@student_bp.route('/applications/<int:app_id>/withdraw', methods=['POST'])
@login_required
@role_required('student')
def withdraw_application(app_id):
    profile = get_student_profile()
    app_entry = Application.query.get_or_404(app_id)

    if app_entry.student_id != profile.user_id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('student.applications'))

    if app_entry.status != 'pending':
        flash('Only pending applications can be withdrawn.', 'warning')
        return redirect(url_for('student.applications'))

    db.session.delete(app_entry)
    db.session.commit()

    flash('Application withdrawn successfully.', 'success')
    return redirect(url_for('student.applications'))