# coding=utf-8

from app import create_app, db
from app.models import User


app = create_app()

with app.app_context():
    db.create_all()
    u = User()
    u.email = 'viber@gmail.com'
    u.password = 'neon'
    db.session.add(u)
    db.session.commit()


