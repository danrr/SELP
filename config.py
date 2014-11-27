import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = """d\xc8\xfb:)~\x1c\x04\x8c\x87\x84Dxm\xa5\\\x94\xea\xc4wY4\xdc\xf2"""
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')