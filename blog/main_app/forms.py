from flask_security.forms import Required
from flask_wtf import FlaskForm
from wtforms import TextAreaField


class ReviewForm(FlaskForm):
    """Форма для написания отзыва"""
    text = TextAreaField('Отзыв', validators=[Required()])

