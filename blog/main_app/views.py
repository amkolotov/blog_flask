import random

from flask import Blueprint, render_template, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from ..app import app, db
from ..auth_app.models import User
from ..config import PAGINATE_BY
from ..main_app.forms import ReviewForm
from ..main_app.models import Article, Category, Tag, articles_tags, Review

main_app = Blueprint('main_app', __name__, template_folder='templates')


def get_page(req):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    return page


@app.errorhandler(404)
def page_not_fount(e):
    return render_template('404.html')


@main_app.context_processor
def inject_reading():
    """Статьи, в раздел читают сейчас"""
    reading = random.sample(list(Article.query.filter_by(draft=False)), k=8)
    return dict(reading=reading)


@main_app.route('/')
def index():
    """Главная страница"""
    return redirect(url_for('main_app.article_list', category_id=0))


@main_app.route('/articles/<int:category_id>')
def article_list(category_id):
    """Вывод списка статей категории"""
    page = get_page(request)

    if category_id == 0:
        articles = Article.query.filter_by(draft=False).order_by(Article.updated.desc())
        category = {'name': 'Все'}
        page_obj = articles.paginate(page=page, per_page=PAGINATE_BY)
        return render_template('main_app/articles_list.html', page_obj=page_obj, category=category)
    articles = Article.query.filter_by(draft=False, category_id=category_id)
    category = Category.query.filter_by(draft=False, id=category_id).first_or_404()

    page_obj = articles.paginate(page=page, per_page=PAGINATE_BY)

    return render_template('main_app/articles_list.html', page_obj=page_obj, category=category)


@main_app.route('/<int:article_id>')
def article_detail(article_id):
    """Вывод статьи"""
    article = Article.query.filter_by(id=article_id).first_or_404()
    form = ReviewForm()
    return render_template('main_app/article_detail.html', article=article, form=form)


@main_app.route('/tag/<int:tag_id>')
def tag_articles(tag_id):
    """Вывод списка статей тега"""
    page = get_page(request)

    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    articles = Article.query.join(articles_tags, (Article.id == articles_tags.c.article_id))\
        .filter(articles_tags.c.tag_id == tag_id)

    page_obj = articles.paginate(page=page, per_page=PAGINATE_BY)

    return render_template('main_app/articles_list.html', page_obj=page_obj, tag=tag)


@main_app.route('/author/<int:author_id>')
def author_articles(author_id):
    """Вывод списка статей автора"""
    page = get_page(request)

    author = User.query.filter_by(id=author_id).first_or_404()
    articles = Article.query.filter_by(author_id=author_id, draft=False)

    page_obj = articles.paginate(page=page, per_page=PAGINATE_BY)

    return render_template('main_app/articles_list.html', page_obj=page_obj, author=author)


@main_app.route('/search')
def search():
    """Обработка поискового запроса"""
    search = request.args.get('search')
    if search:
        category = Category.query.filter(Category.name.ilike(f'%{search}%')).filter_by(draft=False).first()
        if category:
            return redirect(url_for('main_app.article_list', category_id=category.id))
        tag = Tag.query.filter(Tag.name.ilike(f'%{search}%')).first()
        if tag:
            return redirect(url_for('main_app.tag_articles', tag_id=tag.id))
        author = User.query.filter(User.username.ilike(f'%{search}%')).first()
        if author:
            return redirect(url_for('main_app.author_articles', author_id=author.id))
        article = Article.query.filter(Article.title.ilike(f'%{search}%')).filter_by(draft=False).first()
        if article:
            return redirect(url_for('main_app.article_detail', article_id=article.id))

    return redirect(url_for('main_app.index'))


@main_app.route('/add_review/<int:article_id>', methods=['GET', 'POST'])
@login_required
def add_review(article_id):
    """Добавление отзыва к статье"""
    article = Article.query.filter_by(id=article_id).first_or_404()
    form = ReviewForm(formdata=request.form, obj=article)
    if request.method == 'POST' and form.validate():
        try:
            review = Review(
                article=article,
                user=current_user,
                text=form.text.data
            )
            if request.form['parent']:
                review.parent_id = request.form['parent']

            db.session.add(review)
            db.session.commit()

        except:
            print('Error saving review')

    return redirect(url_for('main_app.article_detail', article_id=article_id))

