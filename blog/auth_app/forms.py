from flask_security.forms import Required, RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DateTimeField, FileField
from wtforms.validators import Optional


class ExtendedRegisterForm(RegisterForm):
    """Расширение формы регистрации пользователя"""
    username = StringField('Имя пользователя', [Required()])


class UserProfileForm(FlaskForm):
    """Форма заполнения профиля пользователя"""
    first_name = StringField('Имя', validators=[Optional()])
    last_name = StringField('Фамилия', validators=[Optional()])
    gender = SelectField('Пол', choices=[('male', 'М'), ('female', 'Ж')])
    about = TextAreaField('О себе', validators=[Optional()])
    date_of_birth = DateTimeField('Дата рождения в формате ДД.ММ.ГГГГ', format='%d.%m.%Y', validators=[Optional()])
    avatar = FileField('Аватар', validators=[Optional()])

