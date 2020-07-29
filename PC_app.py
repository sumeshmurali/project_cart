from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import url_for
from flask import redirect
import flask_login
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = "test key"
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mayoo'
app.config['MYSQL_DATABASE_DB'] = 'project_cart'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
try:
    conn = mysql.connect()
    cursor = conn.cursor()
except:
    raise Exception("DBConnectionFailed> Check If service is runing and credentials are correct")


class User(flask_login.UserMixin):
    pass


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
    if is_privileged(flask_login.current_user.id):
        return redirect(url_for('admin_home'))
    return redirect('home')


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
    return render_template("index.html")


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
    sql = "SELECT id from project_cart.users where email='{}'".format(email)

    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False


def check_password_for(email, entered_password):
    sql = "SELECT password from project_cart.users where email='{}' AND password='{}'".format(email,entered_password)
    cursor.execute(sql)
    if cursor.fetchone():
        return True
    return False


def is_privileged(id):
    sql = "SELECT privileged from project_cart.users where email='{}'".format(id)
    cursor.execute(sql)
    res = cursor.fetchone()
    if res[0] == 1:
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
