from flask import Flask, render_template, request, send_from_directory, redirect, logging
from passlib.hash import sha256_crypt
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from models import db, User, Admin
from views import RegistrationForm, LoginForm

import os
from sqlalchemy.orm.exc import NoResultFound


# NOTE: Admin Part Needs work




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sumesh:mayoo@127.0.0.1/projectcart'
app.secret_key = b'e\x02X\xa7w\xd7\x87\x96C\x96\xaf\xfd(}\xd7\x06'

# SQLAlchemy Database
db.init_app(app)



# FLASK LOGIN

login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(email):
    try:
        user = User.query.filter_by(userEmail = email).one()
    except NoResultFound as e:
        user = None
    if user:
        try:
            __admin__ = Admin.query.filter_by(userId = user.userId).one()
            user.admin = True
            del(__admin__)
        except:
            return
        user.id = user.userEmail
        return user
    else:
        return None
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
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User()
        new_user.userEmail = form.email.data
        new_user.userFirstName = form.firstname.data
        new_user.userLastName = form.lastname.data
        new_user.userPhone = form.phone.data
        new_user.userCountry = form.country.data
        new_user.userIp = request.remote_addr
        if form.password.data == form.confirm.data:
            new_user.userPassword = sha256_crypt.encrypt(form.password.data)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect("/registrationSuccess")

    return render_template('register.html', form=form)

@app.route("/registrationSuccess")
def registration_success():
    return render_template("registrationSuccess.html",)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        print(email)
        user = user_loader(email)
        if user:
            if sha256_crypt.verify(request.form['password'], user.userPassword):
                login_user(user)
                # This part need work. Not finished
                if user.admin:
                    return redirect('/account')
                return redirect('/')
            else:
                return "bad login"
        else:
            return render_template('login.html',form=form,error_msg="Invalid Credentials.. Try again")

    else:
        return render_template('login.html',form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/project')
def projects():
    return render_template('project.html')

if __name__ == '__main__':
    app.run(debug=True)

