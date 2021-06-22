from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, TextField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import email_validator


def chars_validate(form, field):
    excluded_chars = " *?/\\!@&%^+()[]{}=''\"\";:#№$"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Имя пользователся не должно содержать {excluded_chars}.")


class RegistrationForm(FlaskForm):
    username = StringField("Name: ", validators=[DataRequired(), chars_validate()])
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=6,
                                                                              message='Длина пароля должна быть не меньше 6-ти символов.0')])
    confirm_password = PasswordField("Password: ", validators=[DataRequired(), Length(min=6), EqualTo('password',
                                                                                                      message="Пароль должны совподать.")])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    login = StringField("Login: ", validators=[DataRequired(), ])
    # Дописать