from app import db
from flask_security import UserMixin, RoleMixin


users_roles = db.Table('users_roles',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


class User(db.Model, UserMixin):
    """Модель пользователя"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Boolean()

    articles = db.relationship('Article', backref='author')
    profile = db.relationship('UserProfile', backref='user', uselist=False)
    reviews = db.relationship('Review', backref='user')

    roles = db.relationship('Role', secondary=users_roles, backref=db.backref('roles', lazy='dynamic'))

    def __repr__(self):
        return self.username


class Role(db.Model, RoleMixin):
    """Модель ролей пользователей"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(255))


class UserProfile(db.Model):
    """Профиль пользователя"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    gender = db.Column(db.String(1))
    about = db.Column(db.Text())
    date_of_birth = db.Column(db.DateTime)
    avatar = db.Column(db.String(256))

    def __repr__(self):
        return f'Profile - {self.user}'
