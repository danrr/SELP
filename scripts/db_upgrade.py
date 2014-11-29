#!env/bin/python
from migrate.versioning import api
from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from tests.test_config import SQLALCHEMY_DATABASE_URI as TEST_SQLALCHEMY_DATABASE_URI,\
    SQLALCHEMY_MIGRATE_REPO as TEST_SQLALCHEMY_MIGRATE_REPO


def upgrade_db(db_uri, migrate_repo):
    api.upgrade(db_uri, migrate_repo)
    v = api.db_version(db_uri, migrate_repo)
    print('Current database version: ' + str(v))


#app db
upgrade_db(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

#test db
upgrade_db(TEST_SQLALCHEMY_DATABASE_URI, TEST_SQLALCHEMY_MIGRATE_REPO)
