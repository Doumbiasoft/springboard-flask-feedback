from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,TextAreaField,BooleanField
from wtforms.validators import InputRequired,Length


class RegisterForm(FlaskForm):
    """Form for user registration."""

    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30, message='The first name must not be longer than 30 characters.')])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30, message='The last name must not be longer than 30 characters.')])
    username = StringField("Username", validators=[InputRequired(), Length(max=20, message='The username must not be longer than 20 characters.')])
    email = EmailField("Email", validators=[InputRequired(), Length(max=50, message='The email must not be longer than 50 characters.')])
    password = PasswordField("Password", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form for user authentication."""
    username = StringField("Username", validators=[InputRequired(), Length(max=20, message='The username must not be longer than 20 characters.')])
    password = PasswordField("Password", validators=[InputRequired()])
   
class FeedbackForm(FlaskForm):
    """Form for adding feedback."""

    title = StringField("Title", validators=[InputRequired(), Length(max=30, message='The title must not be longer than 30 characters.')])
    content = TextAreaField("Content",validators=[InputRequired()])

class EditFeedbackForm(FlaskForm):
    """Form for editing feedback."""

    title = StringField("Title", validators=[InputRequired(), Length(max=30, message='The title must not be longer than 30 characters.')])
    content = TextAreaField("Content",validators=[InputRequired()])

class EditUserForm(FlaskForm):
    """Form for user edition."""

    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30, message='The first name must not be longer than 30 characters.')])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30, message='The last name must not be longer than 30 characters.')])
    email = EmailField("Email", validators=[InputRequired(), Length(max=50, message='The email must not be longer than 50 characters.')])
    is_admin = BooleanField("Is Admin")

class EditPasswordForm(FlaskForm):
    """Form for user password edition."""
    password_old = PasswordField("Old Password", validators=[InputRequired()])
    password_new = PasswordField("New Password", validators=[InputRequired()])
    password_new_confirm = PasswordField("Confirm New Password", validators=[InputRequired()])

    