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
    create_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<id:{self.id} username:{self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    img_path = db.Column(db.Text(), nullable=False, unique=True)
    views = db.Column(db.Integer(), default=0)
    userid = db.Column(db.Integer(), nullable=False)
    likes = db.Column(db.Integer(), default=0)
    main_teg = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'id:{self.id} mTeg:{self.main_teg}'
