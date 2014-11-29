import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
TESTING = True
WTF_CSRF_ENABLED = False