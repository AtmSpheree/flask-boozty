from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddTagForm(FlaskForm):
    title = StringField('Тэг', validators=[DataRequired()])
    submit = SubmitField('Отправить')
