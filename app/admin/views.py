#coding=utf-8
from . import admin
from .forms import LoginForm, SearchForm, SettingForm, EditorForm, TagForm
from ..models import User, Post, Tag
from app import db
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, login_user, logout_user, current_user

from .utils import str_to_tag

@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@admin.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@login_required
@admin.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@login_required
@admin.route('/settings', methods=['GET', 'POST'])
def setting():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.blog_title = form.blog_title.data
        current_user.blog_description = form.blog_description.data
        current_user.blog_cover = form.blog_cover
        current_user.posts_per_page = form.posts_per_page
        current_user.author_detail = form.author_detail
        db.session.add(current_user)
        flash('Updated')
        return redirect(url_for('admin.setting'))
    form.blog_title.data = current_user.blog_title
    form.blog_description.data = current_user.blog_description
    form.blog_cover.data = current_user.blog_cover
    form.posts_per_page.data = current_user.posts_per_page
    form.author_detail.data = current_user.author_detail
    return render_template('setting.html', form=form)

@login_required
@admin.route('/new_post', methods=['GET', 'POST'])
def new_post():
    form = EditorForm()
    if form.validate_on_submit():
        if Post.query.filter_by(url_name=form.url_name.data).first():
            flash('url_name already exist')
            return render_template('new_post.html', form=form)
        tag_temp = str_to_tag(form)
        post = Post(title=form.title.data,
                    cover=form.cover.data,
                    body=form.editor.data,
                    summary=form.summary.data,
                    publish=form.publish.data,
                    url_name=form.url_name.data,
                    publish_date=form.publish_date.data,
                    tags=tag_temp)
        db.session.add(post)
        db.session.commit()
        flash('Add article success')
        return redirect(url_for('admin.editor', form=form, url_name=form.url_name.data))
    return render_template('new_post.html', form=form)


@login_required
@admin.route('/manage', methods=['GET', 'POST'])
def manage_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.publish_date.desc()).paginate(
        page, per_page=current_app.config['MANAGE_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('manage_posts.html', posts=posts, pagination=pagination)

@login_required
@admin.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = Post.query.whoosh_search(form.search.data).all()
    return render_template('search.html', results=results)

@login_required
@admin.route('/editor/<url_name>', methods=['GET', 'POST'])
def editor(url_name):
    post = Post.query.filter_by(url_name=url_name).first_or_404()
    form = EditorForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.cover = form.cover.data
        post.body = form.editor.data
        post.summary = form.summary.data
        post.publish = form.publish.data
        post.url_name = form.url_name.data
        post.publish_date = form.publish_date.data

        tag_temp = str_to_tag(form)
        post.tags = tag_temp
        flash('article has updated')
        return redirect(url_for('admin.editor', url_name=post.url_name))
    form.title.data = post.title
    form.cover.data = post.cover
    form.editor.data = post.body
    form.summary.data = post.summary
    form.publish.data = post.publish
    form.url_name.data = post.url_name
    form.publish_date.data = post.publish_date
    form.tags.data = ' '.join([tag.name for tag in post.tags])
    return render_template('editor.html', form=form, post=post)


@login_required
@admin.route('/manage/delete/post', methods=['GET', 'POST'])
def delete_post():
    url_name = request.args.get('url_name')
    post = Post.query.filter_by(url_name=url_name).first_or_404()
    db.session.delete(post)
    db.session.commit()
    flash('Delete Success')
    return redirect(url_for('admin.manage_posts'))


@login_required
@admin.route('/tags', methods=['GET', 'POST'])
def manage_tags():
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.paginate(
        page, per_page=8, error_out=False
    )
    tags = pagination.items
    return render_template('manage_tags.html', tags=tags, pagination=pagination)

@login_required
@admin.route('/tags/<url_name>', methods=['GET', 'POST'])
def modify_tag(url_name):
    tag = Tag.query.filter_by(url_name=url_name).first_or_404()
    form = TagForm()
    if form.validate_on_submit():
        tag.name = form.name.data
        tag.url_name = form.url_name.data
        tag.cover = form.cover.data
        flash(u'Tag have updated')
        return redirect(url_for('admin.modify_tag', url_name=tag.url_name))
    form.name.data = tag.name
    form.url_name.data = tag.url_name
    form.cover.data = tag.cover
    return render_template('modify_tag.html', form=form, tag=tag)


@login_required
@admin.route('/new_tag', methods=['GET', 'POST'])
def new_tag():
    form = TagForm()
    if form.validate_on_submit():
        if Tag.query.filter_by(url_name=form.url_name.data).first():
            flash('Tag already exist')
            return render_template('new_tag.html', form=form)
        tag = Tag(name=form.name.data,
                  cover=form.cover.data,
                  url_name=form.url_name.data)
        db.session.add(tag)
        db.session.commit()
        flash('Tag updated')
        return redirect(url_for('admin.new_tag'))
    return render_template('new_tag.html', form=form)

@login_required
@admin.route('/tags/delete', methods=['GET', 'POST'])
def delete_tag():
    url_name = request.args.get('url_name')
    tag = Tag.query.filter_by(url_name=url_name).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('Tag deleted')
    return redirect(url_for('amdin.manage_tags'))




























