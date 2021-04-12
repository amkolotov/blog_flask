from .app import app, db
from .auth_app import models
from .main_app import models
from .main_app.models import Category
from .main_app.views import main_app
from .account_app.views import account_app
from .auth_app.views import auth_app


@app.context_processor
def inject_categories():
    """Список категорий"""
    categories = Category.query.filter_by(draft=False)
    return dict(categories=categories)


app.register_blueprint(main_app, url_prefix='')
app.register_blueprint(account_app, url_prefix='/account')
app.register_blueprint(auth_app, url_prefix='/auth')

if __name__ == '__main__':
    app.run()
