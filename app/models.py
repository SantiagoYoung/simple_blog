#!/usr/bin/python
# coding=utf-8

from datetime import datetime
import bleach

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from markdown import markdown
from jieba.analyse.analyzer import ChineseAnalyzer

from . import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(64), default='Poem and far')
    blog_description = db.Column(db.String(64), default=u'Always Me')
    blog_cover = db.Column(db.String(64), default='https://ooo.0o0.ooo/2017/05/02/59084eb8a3e22.jpg')
    posts_per_page = db.Column(db.Integer, default=5)
    author_detail = db.Column(db.Text, default=u'you will never die.')

    @property
    def password(self):
        raise AttributeError('u cannot see')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __unicode__(self):
        return "<User %r>" % self.email


belong_to = db.Table('belong_to',
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                     )

class Post(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['title']
    __analyzer__ = ChineseAnalyzer()
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    cover = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    summary = db.Column(db.Text)
    publish = db.Column(db.Boolean, default=True, index=True)
    url_name = db.Column(db.String(64), index=True, unique=True)

    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)

    tags = db.relationship('Tag',
                           secondary=belong_to,
                           backref=db.backref('posts', lazy='dynamic'),
                           lazy='dynamic')

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __unicode__(self):
        return self.title

db.event.listen(Post.body, 'set', Post.on_changed_body)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    cover = db.Column(db.String(64), default='')
    name = db.Column(db.String(64), unique=True)
    url_name = db.Column(db.String(64), index=True, unique=True)

    def __unicode__(self):
        return self.name

@login_manager.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))
