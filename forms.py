from flask_wtf import Form, FlaskForm, RecaptchaField
from wtforms import Form, BooleanField, StringField, validators, SubmitField, PasswordField, SelectField, DateField, \
    TextField
from wtforms.validators import DataRequired, Email, EqualTo, URL, Length


class GroupForm(FlaskForm):
    groupName = StringField('Group Name')
    groupSize = StringField('Group Size')
    startCity = StringField('Starting City')
    distance = StringField('Max Travel Distance in Miles')
    duration = StringField('Trip Duration in Days')
    driveTime = StringField('Maximum Time Spent Driving Each Day (in Hours)')
    submit = SubmitField('Submit')

class Individual(FlaskForm):
    memberName = StringField('Name')
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    body = TextField('Message')
    submit = SubmitField('Submit')