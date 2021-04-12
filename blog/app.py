from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads

from .config import Configuration
from .main_app.admin import AdminView, HomeAdminView, ArticleAdminView

app = Flask(__name__)

app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

from .main_app.models import Article, Category, Tag, Review
from .auth_app.models import User, Role, UserProfile

admin = Admin(app, 'Blog', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(ArticleAdminView(Article, db.session))
admin.add_view(AdminView(Category, db.session))
admin.add_view(AdminView(Tag, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(UserProfile, db.session))
admin.add_view(AdminView(Review, db.session))

from .auth_app.forms import ExtendedRegisterForm

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)
