import os
from app import app, db
from app.models import User, Post, Tag

if __name__ == "__main__":
    app.run(debug=True)
    # db.create_all()