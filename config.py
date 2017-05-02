#coding=utf-8
'''
配置文件
'''
import os

#文件根目录
basedir = os.path.abspath(os.path.dirname(__file__))

#密匙
SECRET_KEY = 'NEON-VIBER'
CSRF_ENABLED = True

#数据库地址
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

#文章每页显示数量
MANAGE_POSTS_PER_PAGE = 8
#搜索显示数量
MAX_SEARCH_RESULTS = 50


WHOOSH_BASE = os.path.join(basedir, 'search.db')
