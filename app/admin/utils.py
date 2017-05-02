#coding=utf-8
from app import db
from ..models import Tag

def str_to_tag(form):
    tag_temp = []
    tag_list = form.tags.data.split()
    for tag_name in tag_list:
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            tag = Tag(name=tag_name,
                      url_name=tag_name)
            db.session.add(tag)
            db.session.commit()
        tag_temp.append(Tag.query.filter_by(name=tag_name).first())
    return tag_temp