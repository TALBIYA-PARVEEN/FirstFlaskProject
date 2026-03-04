from flask import Flask , render_template , request , redirect 
import requests
from config import Config

app=Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/student_register',methods=['GET','POST'])
def student_register():
    if request.method=='POST':
        # handle request
        pass
    return render_template('student_register.html')


@app.route('/company_register',methods=['GET','POST'])
def company_register():
    if request.method=='POST':
        # handle request
        pass
    return render_template('company_register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        # handle request
        pass
    return render_template('login.html')

@app.route("/login/get_google/<role>")
def login_with_google(role):

    if role not in ["student", "company"]:
        return "Invalid role", 400
    
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={app.config['GOOGLE_CLIENT_ID']}"
        f"&redirect_uri={app.config['GOOGLE_REDIRECT_URI']}"
        "&scope=openid%20email%20profile"
        "&prompt=select_account"
    )

    return redirect(google_auth_url)

@app.route("/login/google/callback")
def google_callback():
    code = request.args.get("code")

    token_url = "https://oauth2.googleapis.com/token"

    
    data = {
        "code": code,
        "client_id": app.config["GOOGLE_CLIENT_ID"],
        "client_secret": app.config["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": app.config["GOOGLE_REDIRECT_URI"],
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

    return f"User Email: {user_info.get('email')}"

if __name__=='__main__':
    app.run(host='localhost',port=5000,debug=True)