from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from flask import request
from werkzeug.urls import url_parse
from app import db
from datetime import datetime
from pytz import timezone
from geolocator import Geolocator


@app.route('/')
@app.route('/index')
def index():
    users = User.query.order_by(User.username.desc()).all()
    return render_template('index.html', title='Главная', users=users)


@app.route('/map/')
@login_required
def map_layout():
    return render_template('map_layout.html')


# User profile
@app.route('/profile/<user_id>')
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = EmptyForm()
    if user.coords:
        lat, lng = user.coords.split(';')
    else:
        lat, lng = None, None
    return render_template('profile.html', user=user, form=form, lat=lat, lng=lng)


# Edit profile
@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.city = form.city.data
        current_user.age = form.age.data
        current_user.link = form.link.data
        current_user.address = form.address.data
        current_user.coords = Geolocator(form.address.data).str_coords()
        db.session.commit()
        flash('Изменения сохранены.')
        return redirect(url_for('profile', user_id=current_user.id))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.city.data = current_user.city
        form.age.data = current_user.age
        form.address.data = current_user.address
        form.link.data = current_user.link
    return render_template('edit_profile.html', title='Изменить профиль',
                           form=form)

# User login
@app.route('/auth',  methods=['GET', 'POST'])
def auth():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный пароль или логин')
            return redirect(url_for('auth'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth.html', title='Войти', form=form)


# Registration
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!')
        return redirect(url_for('auth'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Update user last seen
@app.before_request
def before_request():
    if current_user.is_authenticated:
        tz = timezone('Europe/Moscow')
        time = datetime.now(tz)
        current_user.last_seen = time
        db.session.commit()


@app.route('/follow/<id>', methods=['POST'])
@login_required
def follow(id):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=id).first()
        if user is None:
            flash('Пользователь {} не найден.'.format(user.username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('Невозможно подписаться на свой аккаунт!')
            return redirect(url_for('user', id=id))
        current_user.follow(user)
        db.session.commit()
        flash('Вы подписались на поьзователя {}!'.format(user.username))
        return redirect(url_for('profile', user_id=id))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<id>', methods=['POST'])
@login_required
def unfollow(id):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=id).first()
        if user is None:
            flash('Пользователь {} не найден.'.format(user.username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('Невозможно отписаться от себя!')
            return redirect(url_for('user', id=id))
        current_user.unfollow(user)
        db.session.commit()
        flash('Вы не подписаны на {}.'.format(id))
        return redirect(url_for('profile', user_id=id))
    else:
        return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html', title="Не найдено: Поиск друзей"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('server_error.html'), 500

