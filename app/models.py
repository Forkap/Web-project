from app import db, login_manager
from datetime import datetime
from flask_login import (LoginManager, UserMixin, login_required, login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.Text(), nullable=False)
    password_hash = db.Column(db.Text(), nullable=False)
    posts = db.relationship('Post', backref='user', cascade='all,delete-orphan')
    create_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<id:{self.id} username:{self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                     )

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    img_path = db.Column(db.Text(), nullable=False, unique=True)
    views = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    likes = db.Column(db.Integer(), default=0)
    main_tag = db.Column(db.Text(), db.ForeignKey('tags.name'), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<id: {self.id} mTag: {self.main_tag}>'


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer(), default=0)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', secondary=post_tags, backref='tags')

    def get_post_count(self):
        return len(self.posts)

    def __repr__(self):
        return f'<{self.id}:{self.name}>'


