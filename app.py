from flask import Flask, render_template, request, send_from_directory
from project_cart.models import db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sumesh:mayoo@127.0.0.1/projectcart'

# SQLAlchemy Datbase
db.init_app(app)


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


# SERVING WEBSITE

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = User()

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
