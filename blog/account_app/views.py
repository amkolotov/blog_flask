from flask import Blueprint, request, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import images, db
from account_app.forms import ArticleForm, ArticleEditForm
from main_app.models import Category, Article, Tag

account_app = Blueprint('account_app', __name__, template_folder='templates')


@account_app.route('/')
@login_required
def my_articles():
    """Вывод статей автора"""
    articles = Article.query.filter_by(author=current_user).order_by('draft')
    return render_template('account_app/my_articles.html', object_list=articles)


@account_app.route('/create', methods=['GET', 'POST'])
@login_required
def create_article():
    """Написание статьи"""
    form = ArticleForm()
    if request.method == 'POST' and form.validate():
        try:
            filename = images.save(request.files['poster'], 'posters')
            category = Category.query.filter_by(id=form.category_id.data).first()

            article = Article(
                category=category,
                author=current_user,
                title=form.title.data,
                poster=filename,
                short_desc=form.short_desc.data,
                text=form.text.data,
                draft=form.draft.data,
            )

            for tag_name in form.tags.data:
                tag = Tag.query.filter_by(name=tag_name).first()
                article.tags.append(tag)

            db.session.add(article)
            db.session.commit()
        except:
            print('Error saving form')

        return redirect(url_for('account_app.my_articles'))

    return render_template('account_app/article_create.html', form=form)


@account_app.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    """Редактирование статьи"""
    article = Article.query.filter_by(id=article_id).first_or_404()

    if current_user == article.author:

        form = ArticleEditForm(formdata=request.form, obj=article)

        if request.method == 'POST' and form.validate():

            category = Category.query.filter_by(id=form.category_id.data).first()
            article.category = category
            article.title = form.title.data

            if request.files['poster']:
                filename = images.save(request.files['poster'], 'posters')
                article.poster = filename

            article.short_desc = form.short_desc.data
            article.text = form.text.data
            article.draft = form.draft.data

            tags = []
            for tag_name in form.tags.data:
                tag = Tag.query.filter_by(name=tag_name).first()
                tags.append(tag)
            article.tags = tags

            db.session.commit()

            return redirect(url_for('account_app.my_articles', article_id=article.id))

        return render_template('account_app/article_edit.html', form=form, article=article)

    return redirect(url_for('main_app.index'))
