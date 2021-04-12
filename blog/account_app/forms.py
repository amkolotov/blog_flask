from flask_wtf.file import FileRequired, FileAllowed
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, FileField, BooleanField, SelectMultipleField, \
    TextAreaField
from wtforms.validators import DataRequired

from ..app import images
from ..main_app.models import Category, Tag


class ArticleForm(FlaskForm):
    """Форма для написания статьи"""
    category_id = SelectField('Категория',
                              choices=[(c.id, c.name) for c in Category.query.filter_by(draft=False).order_by('name')])
    title = StringField('Название', validators=[DataRequired()])
    poster = FileField('Постер', validators=[FileRequired(), FileAllowed(images, 'Только изображения!')])
    short_desc = StringField('Краткое описание', validators=[DataRequired()])
    text = TextAreaField('Текст', validators=[DataRequired()])
    tags = SelectMultipleField('Теги', choices=[(t.name, t.name) for t in Tag.query.order_by('name')],
                               validate_choice=False)
    draft = BooleanField('Черновик', default=False)


class ArticleEditForm(FlaskForm):
    """Форма для редактирования статьи"""
    category_id = SelectField('Категория',
                              choices=[(c.id, c.name) for c in Category.query.filter_by(draft=False).order_by('name')])
    title = StringField('Название', validators=[DataRequired()])
    poster = FileField('Изменить постер', validators=[FileAllowed(images, 'Только изображения!')])
    short_desc = StringField('Краткое описание', validators=[DataRequired()])
    text = TextAreaField('Текст', validators=[DataRequired()])
    tags = SelectMultipleField('Теги', choices=[(t.name, t.name) for t in Tag.query.order_by('name')],
                               validate_choice=False)
    draft = BooleanField('Черновик', default=False)
