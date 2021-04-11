import json
import os

from app import db
from auth_app.models import User
from main_app.models import Category, Tag, Article

JSON_PATH = 'main_app/db_json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name)) as file:
        return json.load(file)


def fill_db_from_json():
    try:
        db.session.query(User).delete()
        db.session.commit()

        users = load_from_json('users.json')

        for item in users:
            user = User(**item)
            db.session.add(user)
        db.session.commit()

    except Exception as err:
        print(err)
        db.session.rollback()

    try:
        db.session.query(Category).delete()
        db.session.commit()

        categories = load_from_json('categories.json')

        for item in categories:
            category = Category(**item)
            db.session.add(category)
        db.session.commit()

    except Exception as err:
        print(err)
        db.session.rollback()

    try:
        db.session.query(Tag).delete()
        db.session.commit()

        tags = load_from_json('tags.json')

        for item in tags:
            tag = Tag(**item)
            db.session.add(tag)
        db.session.commit()

    except Exception as err:
        print(err)
        db.session.rollback()

    try:
        db.session.query(Tag).delete()
        db.session.commit()

        tags = load_from_json('tags.json')

        for item in tags:
            tag = Tag(**item)
            db.session.add(tag)
        db.session.commit()

    except Exception as err:
        print(err)
        db.session.rollback()

    try:
        db.session.query(Article).delete()
        db.session.commit()

        articles = load_from_json('articles.json')

        for item in articles:

            category_name = item['category']
            _category = Category.query.filter_by(name=category_name).first()
            item['category'] = _category

            author_name = item['author']
            _author = User.query.filter_by(username=author_name).first()
            item['author'] = _author

            article = Article(
                title=item['title'],
                category=item['category'],
                poster=item['poster'],
                author=item['author'],
                short_desc=item['short_desc'],
                text=item['text'],
            )

            for tag in item['tags']:
                _tag = Tag.query.filter_by(name=tag).first()
                article.tags.append(_tag)

            db.session.add(article)

        db.session.commit()

    except Exception as err:
        print(err)
        db.session.rollback()




