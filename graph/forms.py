from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
	# def __init__(self, csrf_enabled=False, *args, **kwargs):
	# 	super(LoginForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)
	email = StringField('email', validators=[DataRequired(), Email()])
	password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=25)])

class AddUserForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(max=25)], render_kw={"placeholder": "John Doe", "class": "texti"})
	email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "johndoe@example.com", "class": "texti"})
	pass1 = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=25), EqualTo('pass2', message='Passwords must match.')], render_kw={"class": "texti"})
	pass2 = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"class": "texti"})
	submit = SubmitField('submit', render_kw={'value':'Add!'})