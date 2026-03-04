# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from config import Config
# from flask_migrate import Migrate
# from flask_login import LoginManager 
# from flask_bcrypt import Bcrypt     
# import os
 
        
# db = SQLAlchemy() 
# migrate=Migrate()
# login_manager = LoginManager()
# bcrypt = Bcrypt()

# def create_app():
#     base_dir = os.path.abspath(os.path.dirname(__file__))
#     # app = Flask(__name__,static_folder="static",template_folder='templates')
#     app = Flask(__name__,template_folder=os.path.join(base_dir, "templates"))
#     app.config.from_object(Config)
   
#     login_manager.init_app(app)
#     login_manager.login_view = 'auth.login'
#     db.init_app(app)
#     bcrypt.init_app(app)
   
#     from app.auth.routes import auth_bp
#     app.register_blueprint(auth_bp)
   
#     from app.student.routes import student_bp
#     app.register_blueprint(student_bp)
    
#     from app.company.routes import company_bp
#     app.register_blueprint(company_bp)
    
#     from app.admin.routes import admin_bp
#     app.register_blueprint(admin_bp)
   
#     @login_manager.user_loader
#     def load_user(user_id):
#         from app.models import User
#         return User.query.get(int(user_id))
   
#     from app.utils import create_default_admin
#     with app.app_context():
#         db.create_all()
#         create_default_admin()
   
#     from app import models
#     migrate.init_app(app,db)
    


#     print(app.template_folder)
#     return app



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
import os


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates")
    )

    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'

    # Register Blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.student.routes import student_bp
    app.register_blueprint(student_bp)

    from app.company.routes import company_bp
    app.register_blueprint(company_bp)

    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp)

    # Import models BEFORE creating tables
    from app import models

    # Create tables + default admin
    with app.app_context():
        db.create_all()

        from app.utils import create_default_admin
        create_default_admin()

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    return app