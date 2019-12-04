from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField ,SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app import databaseModule


class LoginForm(FlaskForm):
    account = StringField('Account', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    account = StringField('Account', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4,max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validateAccountname(self, accountname):
        return databaseModule.verify_account(accountname)


class ApplicationUploadForm(FlaskForm):
    application = StringField('Application', validators=[DataRequired(), Length(min=4, max=100)])

    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['prop'])
    ])

    submit = SubmitField('Upload')

class ApplicationSelection(FlaskForm):
    application = SelectField('Current Application')
    submit = SubmitField('Go')


class ResourceSelection(FlaskForm):
    application = SelectField('Current Application')
    node = SelectField('Current Node')
    metric = SelectField('Current Meric')
    submit = SubmitField('Launch')

class addUser(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username= StringField('Account', validators=[DataRequired(), Length(min=4, max=100)])
    password= PasswordField('Password', validators=[DataRequired(), Length(min=4,max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    access_level = SelectField('Current Access Level',choices=[('1','Reader'),('2','Creator'),('3','Administrator')])
    submit = SubmitField('Save')
    remove = SubmitField('Delete')





