from flask_wtf import FlaskForm
from wtforms import Form, ValidationError
from wtforms import StringField, SubmitField, TextField, BooleanField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed
import email_validator


def chars_validate(form, field):
    excluded_chars = " *?/\\!@&%^+()[]{}=''\"\";:#№$"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Имя пользователся не должно содержать {excluded_chars}.")


def check_tags(form, field):
    if not field.data:
        return
    list_ = field.data.split(" ")
    for tag in list_:
        if tag[0] != '#':
            raise ValidationError("Теги должны содержать в начале знак #.\n Например: '#Море #Природа #Семья'")


def check_main_tag(form, field):
    if len(field.data.split(" ")) > 1:
        raise ValidationError("Главный тэг должен состоять из одного слова.")


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
                                                 Length(min=6), EqualTo('password', message="Пароли должны совподать.")]
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


class NextImg(FlaskForm):
    tag_name = HiddenField(label="Название тега")
    imgs_id = HiddenField(label="Загруженные изображения")

    def __init__(self, tag, imgs_id: list):
        self.tag_name.data = tag
        self.imgs_id.data = imgs_id


class UploadForm(FlaskForm):
    main_tag = StringField(label="Основной тег:", validators=[DataRequired(), check_tags, check_main_tag], id="filename")
    other_tags = StringField(label="Еще теги:", validators=[check_tags])
    file = FileField(label="Выберите файл", id="file", validators=[DataRequired(), FileAllowed(['png', 'jpg', 'svg'])])
    submit = SubmitField(label='Загрузить файл', id="submit")