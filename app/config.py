import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = """d\xc8\xfb:)~\x1c\x04\x8c\x87\x84Dxm\xa5\\\x94\xea\xc4wY4\xdc\xf2"""
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

imgur_client_id = 'c82b0dfcd28ce0d'
imgur_client_secret = '321511b8f8dae2b5d9aa89eb3afcbbff392356a4'

WHOOSH_BASE = os.path.join(basedir, 'search.db')

SHOW_IN_ONE_GO = 5  # number of posts or submissions methods that return lists of them should return by default