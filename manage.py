#coding=utf-8
'''
命令管理
'''

from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
from app.models import User, Post, Tag, belong_to

#创建app
app = create_app()
manage = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag, belong_to=belong_to)

#创建命令
manage.add_command('shell', Shell(make_context=make_shell_context))
manage.add_command('db', MigrateCommand)
manage.add_command('runserver', Server('127.0.0.1', port=8000, use_debugger=True))


if __name__ == '__main__':
    manage.run()
