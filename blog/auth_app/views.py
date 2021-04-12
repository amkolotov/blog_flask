from flask import Blueprint, request, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from ..app import images, db
from .forms import UserProfileForm
from ..auth_app.models import UserProfile

auth_app = Blueprint('auth_app', __name__, template_folder='templates')


@auth_app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Заполнение профиля пользователя"""
    profile = UserProfile.query.filter_by(user=current_user).first()
    form = UserProfileForm(formdata=request.form, obj=profile)

    if request.method == 'POST' and form.validate():
        if not profile:
            try:
                filename = images.save(request.files['avatar'], 'avatars')
            except:
                filename = 'avatars/default_avatar.jpg'

            try:
                user_profile = UserProfile(
                    user=current_user,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    gender=form.gender.data,
                    about=form.about.data,
                    date_of_birth=form.date_of_birth.data,
                    avatar=filename,
                )
                db.session.add(user_profile)
                db.session.commit()

            except Exception as e:
                print('Error saving profile', e)

            return redirect(url_for('auth_app.profile'))

        profile.user = current_user
        profile.first_name = form.first_name.data
        profile.last_name = form.last_name.data
        profile.gender = form.gender.data
        profile.about = form.about.data
        profile.date_of_birth = form.date_of_birth.data

        if request.files['avatar']:
            filename = images.save(request.files['avatar'], 'avatars')
            profile.avatar = filename

        db.session.commit()

        return redirect(url_for('auth_app.profile'))

    return render_template('auth_app/profile.html', form=form, profile=profile)
