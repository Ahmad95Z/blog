from email.policy import default
from turtle import backward
from blog import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(users_id):
    return User.query.get(int(users_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    isAdmin = db.Column(db.Boolean(), default=False, nullable=False)
    posts= db.relationship('Post',backref='author',lazy=True)
    def __repr__(self) -> str:
        return self.email


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.String(),nullable=False)
    date_posted = db.Column(db.DateTime(),nullable=False,default=datetime.now)
    image = db.Column(db.String(),nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
    comments = db.relationship('Comment',backref='post',lazy=True)
    def __repr__(self) -> str:
        return self.title

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(), nullable=False)
    date_posted = db.Column(
        db.DateTime(), nullable=False, default=datetime.now)
    message = db.Column(db.String(), nullable=False)
    post_id = db.Column(db.Integer(), db.ForeignKey(
        'posts.id'), nullable=False)

    def __repr__(self) -> str:
        return self.subject