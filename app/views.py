from app import app
from flask import render_template, request, url_for, flash, make_response, session, redirect
from flask_login import login_required, login_user, current_user, logout_user
from .models import User, Post, Tag, db
from .forms import LoginForm, RegistrationForm, UploadForm
from datetime import datetime
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


@app.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    def check_tag(tag) -> Tag:
        res = db.session.query(Tag).filter(Tag.name == tag).first()
        if res is None:
            new_tag = Tag(name=tag)
            return new_tag
        return res
    form = UploadForm()
    if form.validate_on_submit():
        main_tag = form.main_tag.data.replace(' ', '')
        main_tag = main_tag.replace('#', '').lower()
        other_tags = ''.join(form.other_tags.data.split(' ')).split('#')
        img = form.file.data
        format_dict = {
            'jpeg': 'jpg',
            'png': 'png'
        }
        format = format_dict.get(img.headers['Content-Type'].split('/')[1])
        file_path = 'app'+url_for('static', filename=f'posts_imgs/{current_user.id}{datetime.today().strftime("%S%M%H%d%m%y")}.{format}')
        with open(file_path, 'wb') as new_image:
            new_image.write(img.read())
        post = Post(img_path=file_path, user_id=current_user.id, main_tag=main_tag)

        tag = check_tag(main_tag)
        post.tags.append(tag)
        db.session.add(tag)

        for tag in other_tags:
            if tag == '':
                continue
            tag = tag.lower()
            tag = check_tag(tag)
            post.tags.append(tag)
            db.session.add(tag)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('upload'))

    return render_template('upload.html', form=form)

@app.route("/image/")
def image():
    return render_template('image.html')

