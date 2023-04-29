from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import BooleanField, SubmitField, StringField, MultipleFileField, FieldList
from wtforms.validators import DataRequired
from variables import ALLOWED_EXTENSIONS_FILES
import variables


class AddPostForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired('Это поле необходимо заполнить.')])
    description = StringField('Описание', validators=[DataRequired('Это поле необходимо заполнить.')])
    files = MultipleFileField('Файлы', validators=[FileAllowed(variables.files, f'Только допустимые файлы! ('
                                                                                f'{", ".join(list(ALLOWED_EXTENSIONS_FILES))})')])
    tags = StringField('Тэги', validators=[DataRequired('Выберите хотя бы один тэг.')])
    is_opened = BooleanField('Сделать публичной?')
    invited_users = StringField('Приглашённые пользователи')
    submit = SubmitField('Опубликовать')
