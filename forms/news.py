from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class NewsForm(FlaskForm):
    title = StringField('Заголовок',
                        validators=[DataRequired(), Length(min=1, max=100, message='Заголовок должен быть от 1 до 100 символов.')])
    content = TextAreaField("Содержание", validators=[DataRequired(message='Содержание является обязательным.')])
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')