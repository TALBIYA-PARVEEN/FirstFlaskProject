# 
















from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required
from app.utils import role_required
from app import db
from app.models import User, Company, Student, PlacementDrive, Application
from sqlalchemy import func
from io import StringIO
import csv

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# =========================
# DASHBOARD
# =========================
@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    stats = {
        'students': User.query.filter_by(role='student').count(),
        'companies': User.query.filter_by(role='company').count(),
        'pending_companies': User.query.filter_by(role='company', is_approved=False).count(),
        'pending_drives': PlacementDrive.query.filter_by(status='Pending').count(),
        'active_drives': PlacementDrive.query.filter_by(status='Approved').count(),
        'applications': Application.query.count(),
    }
    return render_template('admin/dashboard.html', stats=stats)


# =========================
# COMPANIES
# =========================
@admin_bp.route('/companies')
@login_required
@role_required('admin')
def companies():
    q = request.args.get('q', '')
    query = User.query.filter_by(role='company')

    if q:
        query = query.join(Company).filter(Company.company_name.ilike(f'%{q}%'))

    companies = query.all()
    return render_template('admin/companies.html', companies=companies, q=q)


@admin_bp.route('/companies/pending')
@login_required
@role_required('admin')
def pending_companies():
    companies = User.query.filter_by(role='company', is_approved=False).all()
    return render_template('admin/pending_companies.html', companies=companies)


@admin_bp.route('/companies/<int:user_id>/approve', methods=['POST'])
@login_required
@role_required('admin')
def approve_company(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash('Company approved.', 'success')
    return redirect(url_for('admin.pending_companies'))


@admin_bp.route('/companies/<int:user_id>/reject', methods=['POST'])
@login_required
@role_required('admin')
def reject_company(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Company rejected and deleted.', 'info')
    return redirect(url_for('admin.pending_companies'))


@admin_bp.route('/companies/<int:user_id>/blacklist', methods=['POST'])
@login_required
@role_required('admin')
def blacklist_company(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = not user.is_blacklisted
    db.session.commit()
    flash('Company blacklist status changed.', 'info')
    return redirect(url_for('admin.companies'))


# =========================
# DRIVES
# =========================
@admin_bp.route('/drives')
@login_required
@role_required('admin')
def drives():
    q = request.args.get('q', '')
    query = PlacementDrive.query

    if q:
        query = query.filter(PlacementDrive.job_title.ilike(f'%{q}%'))

    drives = query.all()
    return render_template('admin/drives.html', drives=drives, q=q)


@admin_bp.route('/drives/pending')
@login_required
@role_required('admin')
def pending_drives():
    drives = PlacementDrive.query.filter_by(status='Pending').all()
    return render_template('admin/pending_drives.html', drives=drives)


@admin_bp.route('/drives/<int:drive_id>/approve', methods=['POST'])
@login_required
@role_required('admin')
def approve_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "Approved"
    db.session.commit()
    flash('Drive approved.', 'success')
    return redirect(url_for('admin.pending_drives'))


@admin_bp.route('/drives/<int:drive_id>/reject', methods=['POST'])
@login_required
@role_required('admin')
def reject_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    db.session.delete(drive)
    db.session.commit()
    flash('Drive rejected and deleted.', 'info')
    return redirect(url_for('admin.pending_drives'))


# =========================
# STUDENTS
# =========================
# @admin_bp.route('/students')
# @login_required
# @role_required('admin')
# def students():
#     q = request.args.get('q', '')
#     query = User.query.filter_by(role='student')

#     if q:
#         query = query.join(Student).filter(Student.full_name.ilike(f'%{q}%'))

#     students = query.all()
#     return render_template('admin/students.html', students=students, q=q)

@admin_bp.route('/students')
@login_required
@role_required('admin')
def students():
    q = request.args.get('q', '').strip()
    
    query = User.query.filter_by(role='student').join(Student)

    if q:
        query = query.filter(Student.full_name.ilike(f'%{q}%'))

    students = query.all()
    return render_template('admin/students.html', students=students, q=q)


@admin_bp.route('/students/<int:user_id>/blacklist', methods=['POST'])
@login_required
@role_required('admin')
def blacklist_student(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blacklisted = not user.is_blacklisted
    db.session.commit()
    flash('Student blacklist status changed.', 'info')
    return redirect(url_for('admin.students'))


# =========================
# EXPORT STUDENTS CSV
# =========================
@admin_bp.route('/export/students')
@login_required
@role_required('admin')
def export_students():
    students = Student.query.all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['User ID', 'Full Name', 'Roll Number', 'Branch', 'CGPA', 'Email', 'Phone'])

    for s in students:
        user = User.query.get(s.user_id)
        writer.writerow([
            s.user_id,
            s.full_name,
            s.roll_number,
            s.branch or '',
            s.cgpa or '',
            user.email if user else '',
            s.phone or ''
        ])

    output = si.getvalue()
    return Response(output, mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment;filename=students.csv'})
    
    
# =========================
# APPLICATIONS
# =========================
@admin_bp.route('/applications')
@login_required
@role_required('admin')
def applications():
    applications = Application.query.all()
    return render_template('admin/applications.html', applications=applications)




# @admin_bp.route('/statistics')
# @login_required
# @role_required('admin')
# def statistics():
#     stats = {
#         "total_students": User.query.filter_by(role='student').count(),
#         "total_companies": User.query.filter_by(role='company').count(),
#         "approved_companies": User.query.filter_by(role='company', is_approved=True).count(),
#         "pending_companies": User.query.filter_by(role='company', is_approved=False).count(),
#         "total_drives": PlacementDrive.query.count(),
#         "approved_drives": PlacementDrive.query.filter_by(status="Approved").count(),
#         "pending_drives": PlacementDrive.query.filter_by(status="Pending").count(),
#         "total_applications": Application.query.count(),
#     }

#     return render_template("admin/statistics.html", stats=stats)

# from app.models import Student, Company, PlacementDrive, Application

@admin_bp.route('/statistics')
@login_required
@role_required('admin')
def statistics():
    total_applications = Application.query.count()
    stats = {
        "total_students": Student.query.count(),
        "total_companies": Company.query.count(),
        "active_drives": PlacementDrive.query.filter_by(status="Active").count(),
        "selected": Application.query.filter_by(status="Selected").count(),
        "rejected": Application.query.filter_by(status="Rejected").count(),
        "pending": Application.query.filter_by(status="Pending").count(),
        "shortlisted": Application.query.filter_by(status="Shortlisted").count(),
        "total_applications": total_applications,
        "success_rate": round(
            (Application.query.filter_by(status="Selected").count() / total_applications * 100)
            if total_applications > 0 else 0, 2
        )
    }
    return render_template("admin/statistics.html", stats=stats)


# =========================
# STUDENT DETAIL
# =========================
@admin_bp.route('/students/<int:user_id>')
@login_required
@role_required('admin')
def student_detail(user_id):
    student = Student.query.get_or_404(user_id)
    user = User.query.get_or_404(user_id)

    return render_template(
        'admin/student_detail.html',
        student=student,
        user=user
    )
    








# =========================
# COMPANY DETAIL
# =========================
@admin_bp.route('/companies/<int:user_id>')
@login_required
@role_required('admin')
def company_detail(user_id):
    company = Company.query.get_or_404(user_id)
    user = User.query.get_or_404(user_id)

    return render_template(
        'admin/company_detail.html',
        company=company,
        user=user
    )
    
    


# =========================
# EXPORT APPLICATIONS (CSV)
# =========================
@admin_bp.route('/export_applications')
@login_required
@role_required('admin')
def export_applications():
    import csv
    from flask import Response

    applications = Application.query.all()

    def generate():
        data = []
        header = ['Application ID', 'Student ID', 'Drive ID', 'Status']
        data.append(header)

        for app in applications:
            row = [
                app.application_id,
                app.student_id,
                app.drive_id,
                app.status
            ]
            data.append(row)

        for row in data:
            yield ','.join(map(str, row)) + '\n'

    return Response(
        generate(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=applications.csv"}
    )
    
    
# =========================
# EXPORT COMPANIES (CSV)
# =========================
@admin_bp.route('/export_companies')
@login_required
@role_required('admin')
def export_companies():
    import csv
    from flask import Response

    companies = Company.query.all()

    def generate():
        data = []
        header = ['User ID', 'Company Name', 'Email', 'Approved']
        data.append(header)

        for company in companies:
            user = User.query.get(company.user_id)

            row = [
                company.user_id,
                company.company_name,
                user.email if user else '',
                user.is_approved if user else ''
            ]
            data.append(row)

        for row in data:
            yield ','.join(map(str, row)) + '\n'

    return Response(
        generate(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=companies.csv"}
    )