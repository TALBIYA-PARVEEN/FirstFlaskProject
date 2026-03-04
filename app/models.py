# from datetime import datetime
# from flask_login import UserMixin
# from app import db
# from app import bcrypt
# from sqlalchemy import event

# class User(UserMixin, db.Model):
#     __tablename__ = "users"

#     user_id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)


#     role = db.Column(db.String(20), nullable=False)

#     is_active = db.Column(db.Boolean, default=True)
#     is_approved = db.Column(db.Boolean, default=False)
#     is_blacklisted = db.Column(db.Boolean, default=False)

#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

   
#     student = db.relationship("Student",back_populates="user",uselist=False,cascade="all, delete-orphan", passive_deletes=True)

#     company = db.relationship("Company",back_populates="user",uselist=False,cascade="all, delete-orphan",passive_deletes=True)

#     admin = db.relationship("Admin",back_populates="user",uselist=False,cascade="all, delete-orphan",passive_deletes=True)

    
#     # def __init__(self, email, password, role, is_active=True, is_approved=False, is_blacklisted=False):
#     #     self.email = email
#     #     hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     #     self.password = hashed.decode('utf-8')
#     #     self.role = role
#     #     self.is_active = is_active
#     #     self.is_approved = is_approved
#     #     self.is_blacklisted = is_blacklisted

#     def get_id(self):
#         return str(self.user_id)
    
#     def set_password(self, password):
#         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password_hash, password)
    
#     def is_active_user(self):
#         return self.is_active and not self.is_blacklisted
    
#     # def check_password(self, password):
#     #     return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
        

# class Student(db.Model):
#     __tablename__ = "students"

    
#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey("users.user_id", ondelete="CASCADE"),
#         # unique=True,
#         primary_key=True
#     )

#     full_name = db.Column(db.String(100), nullable=False)
#     roll_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
#     graduation_year = db.Column(db.Integer, nullable=False)
#     cgpa = db.Column(db.Float)
#     tenth_marks = db.Column(db.Float) 
#     twelfth_marks = db.Column(db.Float) 
#     dob = db.Column(db.Date)
#     year = db.Column(db.Integer)   
#     resume_filename = db.Column(db.String(200))
#     phone = db.Column(db.String(20))
#     address = db.Column(db.Text)
#     skills = db.Column(db.Text)  
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     course = db.Column(db.String(100))
#     branch = db.Column(db.String(100))

    
#     # applications = db.relationship(
#     #     "Application",
#     #     backref="student",
#     #     cascade="all, delete-orphan"
#     # )
    
#     user = db.relationship(
#         "User",
#         back_populates="student"
#     )


#     # def __init__(self,full_name,roll_number,graduation_year,year=None,cgpa=None,tenth_marks=None,twelfth_marks=None,dob=None,resume_filename=None,phone=None,address=None,skills=None,course=None,branch=None):
#     #     self.full_name = full_name
#     #     self.roll_number = roll_number
#     #     self.graduation_year = graduation_year
#     #     self.year = year
#     #     self.cgpa = cgpa
#     #     self.tenth_marks = tenth_marks
#     #     self.twelfth_marks = twelfth_marks
#     #     self.dob = dob
#     #     self.resume_filename = resume_filename
#     #     self.phone = phone
#     #     self.address = address
#     #     self.skills = skills
#     #     self.course = course
#     #     self.branch = branch

#     def check_password(self,password):
#         pass




# class Company(db.Model):
#     __tablename__ = "companies"

    

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey("users.user_id", ondelete="CASCADE"),
#         primary_key=True
#     )

#     company_name = db.Column(db.String(150), nullable=False)
#     industry = db.Column(db.String(100))
#     location = db.Column(db.String(200))
#     website = db.Column(db.String(200))
#     contact_person = db.Column(db.String(100))
#     contact_phone = db.Column(db.String(20))
#     description = db.Column(db.Text)

#     # One company → many drives
#     # drives = db.relationship(
#     #     "PlacementDrive",
#     #     backref="company",
#     #     cascade="all, delete-orphan"
#     # )
#     user = db.relationship(
#         "User",
#         back_populates="company"
#     )
    
#     # def __init__(self,company_name,contact_person,contact_phone,location,industry,website,description):
#     #     self.company_name=company_name
#     #     self.contact_person=contact_person
#     #     self.contact_phone=contact_phone
#     #     self.location=location
#     #     self.industry=industry
#     #     self.website=website
#     #     self.description=description



# class Admin(db.Model):
#     __tablename__ = "admins"

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey("users.user_id", ondelete="CASCADE"),
#         primary_key=True
#     )

#     name = db.Column(db.String(100), nullable=False)
    
#     # admin = db.relationship('User', backref='actions')
    
#     user = db.relationship(
#         "User",
#         back_populates="admin"
#     )
    
#     def __repr__(self):
#         return f'<AdminAction {self.name} by Admin:{self.user_id}>'
    
    
    



# class PlacementDrive(db.Model):
#     __tablename__ = "placement_drives"

#     drive_id = db.Column(db.Integer, primary_key=True)

#     company_id = db.Column(
#         db.Integer,
#         db.ForeignKey("companies.user_id", ondelete="CASCADE"),
#         nullable=False
#     )

#     job_title = db.Column(db.String(150), nullable=False)
#     job_description = db.Column(db.Text, nullable=False)
#     eligibility = db.Column(db.String(200))
#     application_deadline = db.Column(db.Date)

    
#     status = db.Column(db.String(20), default="Pending")

#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
#     applications = db.relationship(
#         "Application",
#         backref="drive",
#         cascade="all, delete-orphan"
#     )

#     def __init__(self,company_id,job_title,job_description,eligibility,application_deadline,status="Pending"):
#         self.company_id=company_id
#         self.job_title=job_title
#         self.job_description=job_description
#         self.eligibility=eligibility
#         self.application_deadline=application_deadline
#         self.status=status
        


# class Application(db.Model):
#     __tablename__ = "applications"

#     application_id = db.Column(db.Integer, primary_key=True)

#     student_id = db.Column(
#         db.Integer,
#         db.ForeignKey("students.user_id", ondelete="CASCADE"),
#         nullable=False
#     )

#     drive_id = db.Column(
#         db.Integer,
#         db.ForeignKey("placement_drives.drive_id", ondelete="CASCADE"),
#         nullable=False
#     )

#     application_date = db.Column(db.DateTime, default=datetime.utcnow)

    
#     status = db.Column(db.String(20), default="Applied")

    
#     __table_args__ = (
#         db.UniqueConstraint("student_id", "drive_id", name="unique_application"),
#     )
    
#     def __init__(self,student_id,drive_id,status="Applied"):
#         self.student_id=student_id
#         self.drive_id=drive_id
#         self.status=status
        
        
        
        
        
        
        
from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt


# =========================
# USER MODEL
# =========================
class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-one relationships
    student = db.relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    company = db.relationship(
        "Company",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    admin = db.relationship(
        "Admin",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_active_user(self):
        return self.is_active and not self.is_blacklisted


# =========================
# STUDENT MODEL
# =========================
class Student(db.Model):
    __tablename__ = "students"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )

    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    graduation_year = db.Column(db.Integer, nullable=False)

    cgpa = db.Column(db.Float)
    tenth_marks = db.Column(db.Float)
    twelfth_marks = db.Column(db.Float)
    dob = db.Column(db.Date)
    year = db.Column(db.Integer)
    resume_filename = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    skills = db.Column(db.Text)
    course = db.Column(db.String(100))
    branch = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="student")

    applications = db.relationship(
        "Application",
        back_populates="student",
        cascade="all, delete-orphan"
    )


# =========================
# COMPANY MODEL
# =========================
class Company(db.Model):
    __tablename__ = "companies"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )

    company_name = db.Column(db.String(150), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(200))
    website = db.Column(db.String(200))
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    description = db.Column(db.Text)

    user = db.relationship("User", back_populates="company")

    drives = db.relationship(
        "PlacementDrive",
        back_populates="company",
        cascade="all, delete-orphan"
    )


# =========================
# ADMIN MODEL
# =========================
class Admin(db.Model):
    __tablename__ = "admins"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )

    name = db.Column(db.String(100), nullable=False)

    user = db.relationship("User", back_populates="admin")

    def __repr__(self):
        return f"<Admin {self.name}>"


# =========================
# PLACEMENT DRIVE MODEL
# =========================
class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    drive_id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.user_id", ondelete="CASCADE"),
        nullable=False
    )

    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.String(200))
    application_deadline = db.Column(db.Date)

    status = db.Column(db.String(20), default="Pending")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship("Company", back_populates="drives")

    applications = db.relationship(
        "Application",
        back_populates="drive",
        cascade="all, delete-orphan"
    )


# =========================
# APPLICATION MODEL
# =========================
class Application(db.Model):
    __tablename__ = "applications"

    application_id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.user_id", ondelete="CASCADE"),
        nullable=False
    )

    drive_id = db.Column(
        db.Integer,
        db.ForeignKey("placement_drives.drive_id", ondelete="CASCADE"),
        nullable=False
    )

    application_date = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(20), default="Applied")

    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="unique_application"),
    )

    student = db.relationship("Student", back_populates="applications")
    drive = db.relationship("PlacementDrive", back_populates="applications")