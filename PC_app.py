from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import url_for
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import flask_login
from datetime import datetime
# from flaskext.mysql import MySQL
import pymysql

from models import User
app = Flask(__name__)
app.secret_key = "test key"
# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'sumesh'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'mayoo'
# app.config['MYSQL_DATABASE_DB'] = 'projectcart'
# app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sumesh:mayoo@127.0.0.1/projectcart'
# mysql.init_app(app)
db = SQLAlchemy(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# try:
# conn = mysql.connect()
# cursor = conn.cursor()
# except:
# raise Exception("DBConnectionFailed> Check If service is runing and credentials are correct")





@login_manager.user_loader
def user_loader(email):
    if not is_email_exists(email):
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if not is_email_exists(email):
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = check_password_for(email, request.form['password'])

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if check_password_for(email, request.form['password']):
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('on_login_success'))

    return 'Bad login'


@app.route('/login_success')
@flask_login.login_required
def on_login_success():
    # if is_privileged(flask_login.current_user.id):
    return redirect(url_for('admin_home'))
    # return redirect('home')


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('home'))


@app.route("/")
@app.route("/index")
@app.route("/home")
def home():
    projects_all = fetch_projects()
    return render_template("index.html", projects=projects_all)


@app.route("/orders")
def orders():
    return render_template("orders.html")


@app.route("/account")
def account():
    return render_template("account.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    new_user = User()
    new_user.userFirstName = request.form['firstname']
    new_user.userLastName = request.form['lastname']
    new_user.userEmail = request.form['email']
    return redirect('/setpassword')


@app.route('/setpassword', methods=['GET', 'POST'])
def setpassword():
    if request.method == "GET":
        return render_template('setpassword.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/admin')
@flask_login.login_required
def admin_home():
    return render_template('admin_home.html')


# custom functions

def is_email_exists(email):
    sql = "SELECT userId from projectcart.users where userEmail='{}'".format(email)

    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False


def check_password_for(email, entered_password):
    sql = "SELECT userPassword from projectcart.users where userEmail='{}' AND userPassword='{}'".format(email,
                                                                                                         entered_password)
    cursor.execute(sql)
    if cursor.fetchone():
        return True
    return False


def is_privileged(id):
    sql = "SELECT privileged from projectcart.users where userEmail='{}'".format(id)
    cursor.execute(sql)
    res = cursor.fetchone()
    if res[0] == 1:
        return True
    return False


def fetch_projects():
    query = """SELECT projectName, projectPrice, projectCategoryMain, projectCategorySub, projectOwner,
     projectDesc FROM projects"""
    cursor.execute(query)
    res = cursor.fetchall()
    projects = []
    for each in res:
        project = {

            "name": each[0],
            "price": each[1],
            "owner": each[4],
            "desc": each[5]
        }
        projects.append(project)
    return projects


if __name__ == '__main__':
    app.run(debug=True)
