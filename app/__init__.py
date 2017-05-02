#coding=utf-8

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
import flask_whooshalchemyplus

#实例化插件
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.login'

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

# 创建app
def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    flask_whooshalchemyplus.init_app(app)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
