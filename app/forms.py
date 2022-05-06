from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf.file import FileField
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Password')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class AddCatForm(FlaskForm):
    name = StringField('Name')
    color = StringField('Color')
    birthdate = DateField('Date of birth')
    mother = SelectField('Mother', choices=[('None', None)])
    father = SelectField('Father', choices=[('None', None)])
    description = TextAreaField('Description')
    sex = RadioField('Sex', choices=[('male', 'male'), ('female', 'female')])
    forsale = BooleanField('For sale?')
    sold = BooleanField('Sold?')
    photo = FileField('Image')
    breeder = BooleanField('Is this a breeding cat?')
    submit = SubmitField('Create Cat')

class UpdateCatForm(FlaskForm):
    name = StringField('Name')
    color = StringField('Color')
    birthdate = DateField('Date of birth')
    mother = SelectField('Mother', choices=[('None', None)])
    father = SelectField('Father', choices=[('None', None)])
    description = TextAreaField('Description')
    sex = RadioField('Sex', choices=[('male', 'male'), ('female', 'female')])
    forsale = BooleanField('For sale?')
    sold = BooleanField('Sold?')
    photo = FileField('Image')
    breeder = BooleanField('Is this a breeding cat?')
    submit = SubmitField('Update Cat')

class DeleteCatForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Delete Cat?')

class AddLitterForm(FlaskForm):
    mother = SelectField('Mother', choices=[('None', None)])
    father = SelectField('Father', choices=[('None', None)])
    duedate = DateField('Due date')
    birthdate = DateField('Birth date')
    born = BooleanField('Are they born yet?')
    public = BooleanField('Public?')
    submit = SubmitField('Create Litter')

class UpdateLitterForm(FlaskForm):
    mother = SelectField('Mother', choices=[('None', None)])
    father = SelectField('Father', choices=[('None', None)])
    duedate = DateField('Due date')
    birthdate = DateField('Birth date')
    born = BooleanField('Are they born yet?')
    public = BooleanField('Public?')
    submit = SubmitField('Update Litter')

class DeleteLitterForm(FlaskForm):
    mother = SelectField('Mother', choices=[('None', None)])
    father = SelectField('Father', choices=[('None', None)])
    duedate = DateField('Due date')
    submit = SubmitField('Delete litter?')

class AddKittenForm(FlaskForm):
    litter = SelectField('Litter', choices=[('None', None)])
    kitten = SelectField('Kitten', choices=[('None', None)])
    submit = SubmitField('Add kitten')

class RemoveKittenForm(FlaskForm):
    litter = SelectField('Litter', choices=[('None', None)])
    kitten = SelectField('Kitten', choices=[('None', None)])
    submit = SubmitField('Remove kitten')