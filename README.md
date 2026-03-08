# Placement PORTAL APPLICATION

## Project Description

This project is a **Placement PORTAL APPLICATION** developed using the Flask web framework and SQLAlchemy. It provides a centralized platform where **students, companies, and administrators** can manage the campus placement process. The system allows companies to create job drives, students to apply for opportunities, and administrators to monitor and manage the overall workflow.

---

## Main Features

### Student
* Register and login
* Create and edit profile
* Upload resume
* View available placement drives
* Apply for drives
* Track application status

### Company
* Register company account
* Create placement drives
* View student applications
* Download student resumes
* Update application status

### Admin
* Approve or reject company registrations
* Approve placement drives
* Manage students and companies
* View all applications
* Export data as CSV

**Predefined Admin Account:**  
* **Email:** `admin@placement.com`  
* **Password:** `admin123`  
> You can use this account to log in as an administrator immediately without registering.

---

## Technologies Used
* Python  
* Flask  
* SQLAlchemy  
* Flask-Login  
* Flask-Migrate  
* HTML  
* CSS  
* Bootstrap  

---

## How to Run the Project

### Step 1: Extract the ZIP file
Unzip the project folder.

### Step 2: Open terminal in the project directory
Navigate to the project folder:

```bash
cd placement-portal-application

Step 3: Create a virtual environment
python -m venv .venv

Step 4: Activate the virtual environment

Windows:
venv\Scripts\activate

Linux / Mac:
source venv/bin/activate


Step 5: Install required dependencies
pip install -r requirements.txt

Step 6: Setup the database
flask db upgrade

Step 7: Run the application
python run.py

or

flask run


Step 8: Open in browser
http://127.0.0.1:5000




Project Structure
project_folder/
│
├── app/
│   ├── admin/
│   ├── student/
│   ├── company/
│   ├── auth/
│   ├── templates/
│   ├── static/
│   └── models.py
│
├── config.py
├── api.yaml
├── Project Report.pdf
├── requirements.txt
├── run.py
└── README.md


Author

Talbiya Parveen (24f2001644)
IIT Madras BS Degree Student


---
### Quick Login Accounts

| Role     | Email                  | Password     |
|----------|-----------------------|-------------|
| Admin    | admin@placement.com    | admin123    |
| Student  | student@example.com   | student123  |
| Company  | company@example.com   | company123  |
---

> Use these accounts to quickly test the system without registering new users.