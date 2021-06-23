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
    username = StringField(label="Логин: ",
                           validators=[DataRequired()], id='username')
    email = StringField(label="Email: ",
                        validators=[Email()]
                        )
    password = PasswordField(label="Пароль: ",
                             validators=[DataRequired(),
                                         Length(min=6, message='Длина пароля должна быть не меньше 6-ти символов.0')],
                             id="password1"
                             )
    confirm_password = PasswordField(label="Повторите пароль: ",
                                     validators=[DataRequired(),
                                                 Length(min=6), EqualTo('password', message="Пароль должны совподать.")]
                                     , id="password2"
                                     )
    remember_me = BooleanField(label="Запомнить меня: ")
    submit = SubmitField('Зарегестрироваться', id='submit')


class LoginForm(FlaskForm):
    login = StringField(label="Логин: ", validators=[DataRequired()], id="username")
    password = PasswordField(label="Пароль: ",
                             validators=[DataRequired(),
                                         Length(min=6, message='Длина пароля должна быть не меньше 6-ти символов.0')],
                             id="password"
                             )
    remember_me = BooleanField(label="Запомнить меня: ")
    submit = SubmitField(label='Войти', id="submit")
