from app import app
from flask import render_template, request, url_for, flash, make_response, session, redirect
from flask_login import login_required, login_user, current_user, logout_user
from .models import User, Post, Tag, db
from .forms import LoginForm, RegistrationForm
current_user: User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        print("да")
        login = form.login.data

        if "@" in login:
            user = db.session.query(User).filter(User.email == login).first()
        else:
            user = db.session.query(User).filter(User.username == login).first()

        if user is None:
            flash("Неверно указано имя пользователя или email")
            return redirect(url_for('login'))

        if not user.check_password(form.password.data):
            flash('Введен не верный пароль')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form, title="Войти")


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if db.session.query(User).filter(User.username == form.username.data).first():
            flash('Пользователь с таким именем уже существует.')
            return redirect(url_for('registration'))
        if db.session.query(User).filter(User.email == form.email.data).first():
            flash('Почта занята.')
            return redirect(url_for('registration'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.role='ordinary'
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('registration.html', form=form)