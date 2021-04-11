import os

PAGINATE_BY = 4


class Configuration(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED = True
    SECRET_KEY = 'aoajsbjmdkclahdkdkdl'

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADED_IMAGES_DEST = basedir + '/static/images/'

    SECURITY_PASSWORD_SALT = 'blog-salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_REGISTERABLE = True
    REGISTER_USER_TEMPLATE = 'security/register_user.html'
    SECURITY_SEND_REGISTER_EMAIL = False
