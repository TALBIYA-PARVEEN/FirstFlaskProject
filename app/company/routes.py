# """
# Company routes for Placement Portal
# Profile, drive management, and application review
# """
# from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
# from flask_login import login_required, current_user
# from app.utils import role_required
# from app import db
# from app.models import User, Company, PlacementDrive, Application, Student
# from datetime import date, datetime

# company_bp = Blueprint('company', __name__, url_prefix='/company')


# # ---------------------------
# # Company Dashboard
# # ---------------------------
# @company_bp.route('/dashboard')
# @login_required
# @role_required('company')
# def dashboard():
#     profile = Company.query.filter_by(user_id=current_user.user_id).first()
#     drives = PlacementDrive.query.filter_by(company_id=profile.user_id).all() if profile else []

#     stats = {
#         'total_drives': len(drives),
#         'total_applications': Application.query.join(PlacementDrive).filter(PlacementDrive.company_id == profile.user_id).count() if profile else 0
#     }
#     return render_template('company/dashboard.html', profile=profile, drives=drives, stats=stats)


# # ---------------------------
# # Company Profile
# # ---------------------------
# @company_bp.route('/profile')
# @login_required
# @role_required('company')
# def profile():
#     profile = Company.query.filter_by(user_id=current_user.user_id).first()
#     return render_template('company/profile.html', profile=profile)


# @company_bp.route('/profile/edit', methods=['GET', 'POST'])
# @login_required
# @role_required('company')
# def edit_profile():
#     profile = Company.query.filter_by(user_id=current_user.user_id).first()
#     if request.method == 'POST':
#         profile.company_name = request.form['company_name']
#         profile.industry = request.form.get('industry')
#         profile.location = request.form.get('location')
#         profile.website = request.form.get('website')
#         profile.contact_person = request.form.get('contact_person')
#         profile.contact_phone = request.form.get('contact_phone')
#         profile.description = request.form.get('description')
#         db.session.commit()
#         flash('Profile updated successfully.', 'success')
#         return redirect(url_for('company.profile'))
#     return render_template('company/edit_profile.html', profile=profile)


# # ---------------------------
# # Create Placement Drive
# # ---------------------------
# @company_bp.route('/drives/create', methods=['GET', 'POST'])
# @login_required
# @role_required('company')
# def create_drive():
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         eligibility_criteria = request.form['eligibility_criteria']
#         application_deadline_str = request.form['application_deadline']

#         try:
#             application_deadline = datetime.strptime(application_deadline_str, '%Y-%m-%d').date()
#         except ValueError:
#             flash('Invalid date format for deadline.', 'danger')
#             return redirect(url_for('company.create_drive'))

#         if application_deadline < date.today():
#             flash('Application deadline cannot be in the past.', 'danger')
#             return redirect(url_for('company.create_drive'))

#         drive = PlacementDrive(
#             company_id=current_user.company.user_id,
#             job_title=title,
#             job_description=description,
#             eligibility=eligibility_criteria,
#             application_deadline=application_deadline,
#             status="Pending"
#         )
#         db.session.add(drive)
#         db.session.commit()
#         flash('Drive created successfully.', 'success')
#         return redirect(url_for('company.drives'))

#     return render_template('company/create_drive.html')


# # ---------------------------
# # List Drives
# # ---------------------------
# @company_bp.route('/drives')
# @login_required
# @role_required('company')
# def drives():
#     drives = PlacementDrive.query.filter_by(company_id=current_user.company.user_id).all()
#     return render_template('company/drives.html', drives=drives)


# # ---------------------------
# # Edit Drive
# # ---------------------------
# @company_bp.route('/drives/<int:drive_id>/edit', methods=['GET', 'POST'])
# @login_required
# @role_required('company')
# def edit_drive(drive_id):
#     drive = PlacementDrive.query.get_or_404(drive_id)
#     if drive.company_id != current_user.company.user_id:
#         flash('Unauthorized.', 'danger')
#         return redirect(url_for('company.drives'))

#     if request.method == 'POST':
#         drive.job_title = request.form['title']
#         drive.job_description = request.form['description']
#         drive.eligibility = request.form['eligibility_criteria']
#         try:
#             drive.application_deadline = datetime.strptime(request.form['application_deadline'], '%Y-%m-%d').date()
#         except ValueError:
#             flash('Invalid date format.', 'danger')
#             return redirect(url_for('company.edit_drive', drive_id=drive_id))

#         db.session.commit()
#         flash('Drive updated successfully.', 'success')
#         return redirect(url_for('company.drives'))

#     return render_template('company/edit_drive.html', drive=drive)


# # ---------------------------
# # Close Drive
# # ---------------------------
# @company_bp.route('/drives/<int:drive_id>/close', methods=['POST'])
# @login_required
# @role_required('company')
# def close_drive(drive_id):
#     drive = PlacementDrive.query.get_or_404(drive_id)
#     if drive.company_id != current_user.company.user_id:
#         flash('Unauthorized.', 'danger')
#         return redirect(url_for('company.drives'))

#     # Instead of is_active (not in model), you can use status or delete if needed
#     drive.status = "Closed"
#     db.session.commit()
#     flash('Drive closed.', 'info')
#     return redirect(url_for('company.drives'))


# # ---------------------------
# # View Applications
# # ---------------------------
# @company_bp.route('/drives/<int:drive_id>/applications')
# @login_required
# @role_required('company')
# def drive_applications(drive_id):
#     drive = PlacementDrive.query.get_or_404(drive_id)
#     if drive.company_id != current_user.company.user_id:
#         flash('Unauthorized.', 'danger')
#         return redirect(url_for('company.drives'))

#     applications = Application.query.filter_by(drive_id=drive_id).all()
#     return render_template('company/drive_applications.html', drive=drive, applications=applications)


# # ---------------------------
# # Update Application Status
# # ---------------------------
# @company_bp.route('/applications/<int:app_id>/update', methods=['POST'])
# @login_required
# @role_required('company')
# def update_application(app_id):
#     app = Application.query.get_or_404(app_id)
#     drive = PlacementDrive.query.get(app.drive_id)
#     if drive.company_id != current_user.company.user_id:
#         flash('Unauthorized.', 'danger')
#         return redirect(url_for('company.drives'))

#     status = request.form['status']
#     if status.lower() in ['applied', 'pending', 'shortlisted', 'selected', 'rejected']:
#         app.status = status.capitalize()
#         db.session.commit()
#         flash('Application status updated.', 'success')
#     else:
#         flash('Invalid status.', 'danger')

#     return redirect(url_for('company.drive_applications', drive_id=app.drive_id))


# # ---------------------------
# # Download Student Resume
# # ---------------------------
# @company_bp.route('/resume/<int:student_id>')
# @login_required
# @role_required('company')
# def download_resume(student_id):
#     student = Student.query.get_or_404(student_id)
#     # Security: Verify student applied to this company's drive
#     profile = current_user.company
#     app_exists = Application.query.join(PlacementDrive).filter(
#         Application.student_id == student_id,
#         PlacementDrive.company_id == profile.user_id
#     ).first()

#     if not app_exists:
#         flash('Unauthorized access to resume.', 'danger')
#         return redirect(url_for('company.drives'))

#     if student.resume_filename:
#         return send_from_directory(current_app.config['UPLOAD_FOLDER'], student.resume_filename)
#     flash('Resume not found.', 'warning')
#     return redirect(url_for('company.drives'))




"""
Company routes for Placement Portal
Profile, drive management, and application review
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from app.utils import role_required
from app import db
from app.models import Company, PlacementDrive, Application, Student
from datetime import date, datetime
import os

company_bp = Blueprint('company', __name__, url_prefix='/company')


# ---------------- HELPER ----------------
def get_company_profile():
    return Company.query.filter_by(user_id=current_user.user_id).first()


# ---------------- DASHBOARD ----------------
@company_bp.route('/dashboard')
@login_required
@role_required('company')
def dashboard():
    profile = get_company_profile()
    if not profile:
        flash('Profile not found.', 'danger')
        return redirect(url_for('auth.logout'))

    drives = PlacementDrive.query.filter_by(company_id=profile.user_id).all()

    total_apps = Application.query.join(PlacementDrive).filter(
        PlacementDrive.company_id == profile.user_id
    ).count()

    stats = {
        'total_drives': len(drives),
        'total_applications': total_apps
    }

    return render_template(
        'company/dashboard.html',
        profile=profile,
        drives=drives,
        stats=stats
    )


# ---------------- PROFILE ----------------
@company_bp.route('/profile')
@login_required
@role_required('company')
def profile():
    profile = get_company_profile()
    return render_template('company/profile.html', profile=profile)


@company_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@role_required('company')
def edit_profile():
    profile = get_company_profile()
    if not profile:
        flash('Profile not found.', 'danger')
        return redirect(url_for('company.dashboard'))

    if request.method == 'POST':
        profile.company_name = request.form['company_name']
        profile.industry = request.form.get('industry')
        profile.location = request.form.get('location')
        profile.website = request.form.get('website')
        profile.contact_person = request.form.get('contact_person')
        profile.contact_phone = request.form.get('contact_phone')
        profile.description = request.form.get('description')

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('company.profile'))

    return render_template('company/edit_profile.html', profile=profile)


# ---------------- CREATE DRIVE ----------------
@company_bp.route('/drives/create', methods=['GET', 'POST'])
@login_required
@role_required('company')
def create_drive():
    profile = get_company_profile()
    if not profile:
        flash('Profile not found.', 'danger')
        return redirect(url_for('company.dashboard'))

    if request.method == 'POST':
        # Get form values safely
        job_title = request.form.get('title')
        job_description = request.form.get('description')
        eligibility = request.form.get('eligibility_criteria')
        application_deadline_str = request.form.get('application_deadline')

        # Validate required fields
        if not job_title or not job_description or not application_deadline_str:
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('company.create_drive'))

        # Parse date
        try:
            application_deadline = datetime.strptime(application_deadline_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('company.create_drive'))

        if application_deadline < date.today():
            flash('Application deadline cannot be in the past.', 'danger')
            return redirect(url_for('company.create_drive'))

        # Create drive
        drive = PlacementDrive(
            company_id=profile.user_id,
            job_title=job_title,
            job_description=job_description,
            eligibility=eligibility,
            application_deadline=application_deadline,
            status="Pending"  # admin will approve later
        )

        db.session.add(drive)
        db.session.commit()

        flash('Drive created successfully.', 'success')
        return redirect(url_for('company.drives'))

    return render_template('company/create_drive.html')


# ---------------- LIST DRIVES ----------------
@company_bp.route('/drives')
@login_required
@role_required('company')
def drives():
    profile = get_company_profile()
    drives = PlacementDrive.query.filter_by(company_id=profile.user_id).all()
    return render_template('company/drives.html', drives=drives)


# ---------------- EDIT DRIVE ----------------
@company_bp.route('/drives/<int:drive_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('company')
def edit_drive(drive_id):
    profile = get_company_profile()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != profile.user_id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('company.drives'))

    if request.method == 'POST':
        drive.job_title = request.form['title']
        drive.job_description = request.form['description']
        drive.eligibility = request.form['eligibility_criteria']

        try:
            drive.application_deadline = datetime.strptime(
                request.form['application_deadline'],
                '%Y-%m-%d'
            ).date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('company.edit_drive', drive_id=drive_id))

        db.session.commit()
        flash('Drive updated successfully.', 'success')
        return redirect(url_for('company.drives'))

    return render_template('company/edit_drive.html', drive=drive)


# ---------------- CLOSE DRIVE ----------------
@company_bp.route('/drives/<int:drive_id>/close', methods=['POST'])
@login_required
@role_required('company')
def close_drive(drive_id):
    profile = get_company_profile()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != profile.user_id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('company.drives'))

    drive.status = "Closed"
    db.session.commit()

    flash('Drive closed.', 'info')
    return redirect(url_for('company.drives'))


# ---------------- VIEW APPLICATIONS ----------------
@company_bp.route('/drives/<int:drive_id>/applications')
@login_required
@role_required('company')
def drive_applications(drive_id):
    profile = get_company_profile()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != profile.user_id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('company.drives'))

    applications = Application.query.filter_by(drive_id=drive_id).all()

    return render_template(
        'company/drive_applications.html',
        drive=drive,
        applications=applications
    )


# ---------------- UPDATE APPLICATION STATUS ----------------
# @company_bp.route('/applications/<int:app_id>/update', methods=['POST'])
# @login_required
# @role_required('company')
# def update_application(app_id):
#     profile = get_company_profile()
#     app_entry = Application.query.get_or_404(app_id)
#     drive = PlacementDrive.query.get(app_entry.drive_id)

#     if drive.company_id != profile.user_id:
#         flash('Unauthorized.', 'danger')
#         return redirect(url_for('company.drives'))

#     status = request.form['status'].capitalize()

#     allowed_statuses = ['Pending', 'Shortlisted', 'Selected', 'Rejected']

#     if status in allowed_statuses:
#         app_entry.status = status
#         db.session.commit()
#         flash('Application status updated.', 'success')
#     else:
#         flash('Invalid status.', 'danger')

#     return redirect(url_for('company.drive_applications', drive_id=app_entry.drive_id))


# ---------------- DOWNLOAD STUDENT RESUME ----------------
@company_bp.route('/resume/<int:student_id>')
@login_required
@role_required('company')
def download_resume(student_id):
    profile = get_company_profile()
    student = Student.query.get_or_404(student_id)

    # Verify student applied to this company
    app_exists = Application.query.join(PlacementDrive).filter(
        Application.student_id == student_id,
        PlacementDrive.company_id == profile.user_id
    ).first()

    if not app_exists:
        flash('Unauthorized access to resume.', 'danger')
        return redirect(url_for('company.drives'))

    if student.resume_filename:
        upload_folder = os.path.join(
            current_app.root_path,
            'static',
            'uploads',
            'resumes'
        )
        return send_from_directory(upload_folder, student.resume_filename)

    flash('Resume not found.', 'warning')
    return redirect(url_for('company.drives'))



# ---------------- REOPEN DRIVE ----------------
@company_bp.route('/drives/<int:drive_id>/reopen', methods=['POST'])
@login_required
@role_required('company')
def reopen_drive(drive_id):
    profile = get_company_profile()
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != profile.user_id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('company.drives'))

    if drive.status != 'Closed':
        flash('Drive is not closed.', 'warning')
        return redirect(url_for('company.drives'))

    drive.status = 'Active'
    db.session.commit()
    flash('Drive reopened successfully.', 'success')
    return redirect(url_for('company.drives'))



@company_bp.route('/applications/<int:app_id>/update', methods=['POST'])
@login_required
@role_required('company')
def update_application(app_id):
    application = Application.query.get_or_404(app_id)

    # Make sure the company owns the drive
    if application.drive.company_id != current_user.user_id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('company.drives'))

    # Get status from form
    new_status = request.form.get('status', 'pending').capitalize()  # Always store capitalized
    application.status = new_status

    db.session.commit()  # ← critical step

    flash(f"Application status updated to {new_status}.", "success")
    return redirect(url_for('company.drive_applications', drive_id=application.drive_id))