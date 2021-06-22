from app import app
from flask import render_template, request, url_for, flash, make_response, session
from flask_login import login_required, login_user, current_user, logout_user
from .models import User, Post, Tag, db

@app.route('/')
def index():
    return render_template('index.html')