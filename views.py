from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField

class RegistrationForm(Form):
    firstname = StringField('First Name', [validators.Length(min=4, max=25)])
    lastname = StringField('First Name', [validators.Length(min=1, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    phone = StringField('Phone Number', [validators.Length(min=10, max=10)])
    country = SelectField('Country', choices=['India','America'])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LoginForm(Form):
    email = StringField('Email', [validators.Email(message="Email is not valid"),validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])