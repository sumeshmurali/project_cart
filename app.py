from flask import Flask, render_template, request, send_from_directory, redirect, logging
from models import db, User, Users
from passlib.hash import sha256_crypt
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager, login_user, current_user, login_required


import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sumesh:mayoo@127.0.0.1/projectcart'
app.secret_key = b'e\x02X\xa7w\xd7\x87\x96C\x96\xaf\xfd(}\xd7\x06'

# FLASK LOGIN

login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(email):
    if User.query.filter_by(userEmail = email).one():
        user = User.query.filter_by(userEmail = email).one()
        user.id = user.userEmail
        return user
    else:
        return None


# SQLAlchemy Database
db.init_app(app)

# Some Variables
tokens = {

}

# Custom Functions


# SERVING STATIC FILES

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

# HANDLING ERRORS

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
# SERVING WEBSITE

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User()
        new_user.userEmail = request.form['email']
        new_user.userFirstName = request.form['firstname']
        new_user.userLastName = request.form['lastname']
        new_user.userPhone = request.form['phone']
        new_user.userCountry = request.form['country']
        new_user.userIp = request.remote_addr
        if request.form['password'] == request.form['confirmpassword']:
            new_user.userPassword = sha256_crypt.encrypt(request.form['password'])
        
        db.session.add(new_user)
        db.session.commit()
        return redirect("/registrationSuccess")

    return render_template('register.html')

@app.route("/registrationSuccess")
def registration_success():
    return render_template("registrationSuccess.html",)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = user_loader(email)
        if user:
            if sha256_crypt.verify(request.form['password'], user.userPassword):
                login_user(user)
                return redirect('/')
            else:
                return "bad login"
        else:
            return "invalid email or password"

    else:
        return render_template('login.html')

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

if __name__ == '__main__':
    app.run()

