from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, EmailField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
import variables
from variables import ALLOWED_EXTENSIONS_PHOTOS


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired('Это поле необходимо заполнить.')])
    surname = StringField('Фамилия', validators=[DataRequired('Это поле необходимо заполнить.')])
    nickname = StringField('Ник', validators=[DataRequired('Это поле необходимо заполнить.')])
    about = StringField('О себе')
    email = EmailField('Почта', validators=[DataRequired('Это поле необходимо заполнить.')])
    password = PasswordField('Пароль', validators=[DataRequired('Это поле необходимо заполнить.')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired('Это поле необходимо заполнить.')])
    avatar = FileField('Аватар', validators=[FileAllowed(variables.photos, f'Только картинки! ('
                                                                           f'{", ".join(list(ALLOWED_EXTENSIONS_PHOTOS))})')])
    submit = SubmitField('Зарегистрироваться')
