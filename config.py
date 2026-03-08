import os

class Config:
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "iit_madras_mad1_project_development-secret-key")
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    
    if FLASK_ENV == "production":
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:  # development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---------------- GOOGLE AUTH ----------------
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    if os.environ.get("FLASK_ENV") == "production":
        GOOGLE_REDIRECT_URI = os.environ.get(
            "GOOGLE_REDIRECT_URI",
            "https://talbiyaparveen.pythonanywhere.com/login/google/callback"
        )
    else:
        GOOGLE_REDIRECT_URI = os.environ.get(
            "GOOGLE_REDIRECT_URI",
            "http://localhost:5000/login/google/callback"
        )

    # ---------------- FILE UPLOAD SETTINGS ----------------
    
    # Upload folder inside static
    UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads")

    # Allowed resume extensions
    ALLOWED_EXTENSIONS = {"pdf"}

    # Maximum file size (2 MB)
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024