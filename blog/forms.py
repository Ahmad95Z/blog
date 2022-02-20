import email
from logging.config import valid_ident
from unittest import TextTestResult
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField ,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
import email_validator
from flask_wtf.file import  FileField, FileAllowed
from blog.models import User
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Это поле обязательно!'),  Email("Не правильный email!")])
    password = PasswordField('Пароль', validators=[DataRequired('Это поле обязательно!')])
    confirm_password = PasswordField ('Подтвердите пароль',validators=[DataRequired('Это поле обязательно!'), EqualTo('password')])
    submit = SubmitField('Регистрация')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationErr('Такой email существует')


class PostForm(FlaskForm):
    title = StringField ('Заголовок', validators=[DataRequired()])
    content = TextAreaField ('Контент', validators=[DataRequired()])
    image = FileField('Изображение поста', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField ('Создать пост')