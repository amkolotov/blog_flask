from datetime import datetime

from ..app import db, app

articles_tags = db.Table('articles_tags',
                         db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                         db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                         )


class Category(db.Model):
    """Категории статей"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(512))
    draft = db.Column(db.Boolean, default=False)

    articles = db.relationship('Article', backref='category')

    def __repr__(self):
        return self.name


class Tag(db.Model):
    """Теги"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return self.name


class Article(db.Model):
    """Статья"""
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(256))
    poster = db.Column(db.String(256))
    short_desc = db.Column(db.String(512))
    text = db.Column(db.Text())
    draft = db.Column(db.Boolean, default=False)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    tags = db.relationship('Tag', secondary=articles_tags, backref='articles', lazy='dynamic')
    reviews = db.relationship('Review', backref='article')

    def __repr__(self):
        return f'<Article: {self.title}>'

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.ALLOWED_EXTENSIONS

    def get_parent_reviews(self):
        return Review.query.filter_by(article_id=self.id).filter(Review.parent_id == None)


class Review(db.Model):
    """Отзывы пользователей о статье"""
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=True)
    text = db.Column(db.Text())

    parent = db.relationship(lambda: Review, remote_side=id, backref='children')

    def __repr__(self):
        return f'Review:{self.id} - {self.user.username} - {self.article}'
