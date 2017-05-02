#coding=utf-8
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField, \
                    TextAreaField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, URL



class LoginForm(Form):
    email = StringField('Email address', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SettingForm(Form):
    blog_title = StringField('Title', validators=[DataRequired()])
    blog_description = StringField('Description', validators=[DataRequired()])
    blog_cover = StringField('Cover', validators=[DataRequired(), URL()])
    posts_per_page = IntegerField('number of article', validators=[DataRequired()])
    author_detail = TextAreaField('Author info', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditorForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    cover = StringField('Cover')
    url_name = StringField('URl name', validators=[DataRequired()])
    editor = TextAreaField('Content', validators=[DataRequired()])
    summary = TextAreaField('summary')
    publish = BooleanField('Publish')
    publish_date = DateField('Publish Date')
    tags = StringField('Tags')
    submit = SubmitField('Save')


class TagForm(Form):
    cover = StringField('Cover')
    name = StringField('Name')
    url_name = StringField('Tag URl')
    submit = SubmitField('Save')


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])