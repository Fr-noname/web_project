from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class BookForm(FlaskForm):
    title = StringField('Название книги',
                        validators=[DataRequired(),
                                    Length(min=1, max=100, message='Название должно быть от 1 до 100 символов.')])
    author = StringField("Автор", validators=[DataRequired(message='Автор является обязательным.')])
    content = TextAreaField("Описание", validators=[DataRequired(message='Описание является обязательным.')])
    is_private = BooleanField("Личная книга")
    submit = SubmitField('Сохранить')
