from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

hashed_password = bcrypt.generate_password_hash("1234567").decode('utf-8')
print(hashed_password)