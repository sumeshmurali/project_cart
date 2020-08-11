from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

import flask_login
db = SQLAlchemy()


class User(db.Model,flask_login.UserMixin):
    __tablename__ = 'users'
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
    userPassword = db.Column(db.String(500))

    def __repr__(self):
        return '<UserEmail: {}>'.format( self.userEmail)

class Admin(db.Model):
    __tablename__ = "admin"

    adminId = db.Column(db.Integer, primary_key=True, auto_increment=True)
    userId = db.Column(db.Integer, unique=True)
    adminPassword = db.Column(db.String(500))
    adminSecondaryPassword = db.Column(db.String(500))
    active = db.Column(db.SmallInteger, default=0)
    loggedIn = db.Column(db.SmallInteger, default=0)
    currentIP = db.Column(db.String(50), default='127.0.0.1')
    prevIP = db.Column(db.String(50), default='127.0.0.1')
    lastLoggedOn = db.Column(db.DATETIME, default=datetime.utcnow)

    def __repr__(self):
        return '<admin active from {}>'.format(self.currentIP)
