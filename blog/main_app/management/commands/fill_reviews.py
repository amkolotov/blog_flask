import random

from app import db
from auth_app.models import UserProfile, User
from main_app.models import Review, Article


def fill_reviews_from_file():
    users = (
        {'username': 'john', 'avatar': 'ava-1.jpeg'},
        {'username': 'alex', 'avatar': 'ava-2.jpg'},
        {'username': 'kate', 'avatar': 'ava-3.jpg'},
    )
    fake_reviews = (
        'Хорошая статья',
        'Соответствует названию',
        'На троечку',
        'Полностью оправдала ожидания',
        'Не актуальная тема',
        'Хорошо написана'
    )

    for item in users:
        user = User.query.filter_by(username=item['username']).first()
        profile = UserProfile.query.filter_by(user=user).first()
        if profile:
            db.session.delete(profile)
            db.session.commit()
        avatar = f'avatars/{item["avatar"]}'

        profile = UserProfile(
            user=user,
            avatar=avatar
        )
        db.session.add(profile)
        db.session.commit()

    Review.query.delete()

    articles = Article.query.all()

    users = list(User.query.all())

    for article in articles:
        random.shuffle(users)
        review_id = None
        for i in range(len(users)):
            if i % 2 == 0:
                review = Review(
                    article=article,
                    user=users[i],
                    text=random.choice(fake_reviews)
                )
                db.session.add(review)
                db.session.commit()
                review_id = review.id
            else:
                review = Review(
                    article=article,
                    user=users[i],
                    parent_id=review_id,
                    text=random.choice(fake_reviews)
                )
                db.session.add(review)
                db.session.commit()





