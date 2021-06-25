from app import app
from flask import render_template, request, url_for, flash, make_response, session, redirect, abort
from flask_login import login_required, login_user, current_user, logout_user
from .models import User, Post, Tag, db
from .forms import LoginForm, RegistrationForm, UploadForm, SearchForm
from datetime import datetime
from random import randrange
import json
current_user: User

@app.route('/')
def index():
    search_form = SearchForm()

    return render_template('index.html', search_form=search_form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    search_form = SearchForm()
    form = LoginForm()
    if form.validate_on_submit():
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
        avatar_path = f'standard_avatars/{randrange(1, 10)}.png'
        user = User(username=form.username.data, email=form.email.data, avatar_path=avatar_path)
        user.set_password(form.password.data)
        user.role='ordinary'
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('registration.html', form=form)


@app.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload(def_name=None):
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
        file_path = file_path.split('/')[2:]
        file_path = '/'.join(file_path)
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

        return redirect(url_for('user_page', id=current_user.id))

    return render_template('upload.html', form=form, def_name=def_name)

@app.route("/post/<id>/")
def post_page(id):
    search_form = SearchForm()
    image = db.session.query(Post).filter(Post.id == id).first()
    if image is None:
        abort(404)

    image.views += 1;
    db.session.commit()
    username = db.session.query(User).filter(User.id == image.user_id).first().username
    return render_template('post_page.html', img=image, username=username, search_form=search_form)

@app.route('/user/<id>/')
def user_page(id):
    search_form = SearchForm()
    user = db.session.query(User).filter(User.id == id).first()
    if user is None:
        abort(404)
    followed = len(user.followed.all())
    followers = len(user.followers.all())
    return render_template('user_page.html', followed=followed, followers=followers, search_form=search_form)

@app.route('/get_hints/',methods=['GET', 'POST'])
def get_hints():
    if request.method == 'POST':
        hints = []
        string = ''.join(request.get_json().split(' ')).split('#')
        for word in string:
            tags_ = db.session.query(Tag.name, Tag.id).all()
            tags = []
            for tag in tags_:
                if word.lower() in tag[0]:
                    tags.append(tag)
            if tags is not None:
                hints += [{"name": el[0], 'id': el[1]}for el in tags]
            if len(hints) == 5:
                break
        if len(hints) < 5:
            for word in string:
                for i in reversed(range(len(word.lower()))):
                    tags_ = db.session.query(Tag.name, Tag.id).all()
                    tags = []
                    for tag in tags_:
                        if word[:i+1].lower() in tag[0]:
                            if {"name": tag[0], 'id': tag[1]} not in hints and tag not in tags:
                                tags.append(tag)
                    if tags is not None:
                        hints += [{"name": el[0], 'id': el[1]}for el in tags]
                    if len(hints) == 5:
                        break
        return json.dumps(hints, ensure_ascii=False)
    return None

@app.route('/tag_page/<id>/')
def tag_page(id):
    search_form = SearchForm()
    tag = db.session.query(Tag).filter(Tag.id == id).first()
    if tag is None:
        abort(404)
    tag.views += 1;
    db.session.commit()
    posts_count = len(tag.posts)
    return render_template('tag_page.html', search_form=search_form, tag=tag, posts_count=posts_count)

@app.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        string = form.search
        string = ''.join(form.search.data.split(' ')).split('#')
        for word in string:
            tags_ = db.session.query(Tag.name, Tag.id).all()
            tags = []
            for tag in tags_:
                 if word.lower() in tag[0]:
                     return redirect(url_for('tag_page', id=tag[1]))
    return redirect(url_for('index'))


@app.route('/delete/<id>')
def delete(id):
    post = db.session.query(Post).filter(Post.id == id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user_page', id=current_user.id))




