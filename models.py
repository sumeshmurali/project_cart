from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import flask_login
db = SQLAlchemy()


class User(db.Model, flask_login.UserMixin):
    userId = db.Column(db.Integer, primary_key=True, auto_increment=True)
    userFirstName = db.Column(db.String(50),)
    userLastName = db.Column(db.String(50),)
    userEmail = db.Column(db.String(500), unique=True)
    userEmailVerified = db.Column(db.SmallInteger, default=0)
    userRegisteredOn = db.Column(db.DATETIME, default=datetime.utcnow)
    userPhone = db.Column(db.String(20), unique=True)
    userIp = db.Column(db.String(50), unique=True)
    userCountry = db.Column(db.String(20),)
    userType = db.Column(db.SmallInteger, default=2)

    def __repr__(self):
        return '<UserEmail: {}'.format( self.userEmail)
